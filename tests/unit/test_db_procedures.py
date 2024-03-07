import pytest

from unittest.mock import patch, MagicMock, call

from application.db_procedures import (
    initialize_tables,
    create_auction_table,
    process_listing,
    bid_check
)


def test_initialize_tables_empty_db():
    with patch('application.db_procedures.psycopg2.connect') as mock_conn:
        mock_cur = MagicMock()
        mock_cur.__enter__.return_value.fetchall.return_value = []  # mock empty database
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cur  # mock connection to use empty database

        with patch('application.db_procedures.create_auction_table') as mock_create_auction_table, \
            patch('application.db_procedures.create_bids_table') as mock_create_bids_table:
            initialize_tables(save_database=False)
            mock_cur.__enter__.return_value.execute.assert_called_with("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'""")  # checks that the LAST call was made with these arguments

            mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cur


            mock_create_auction_table.assert_called_once()  # checks that the func was called exactly once, (doesn't verify the arguments, only the call count)
            mock_create_bids_table.assert_called_once()


def test_initialize_tables_occupied_db(capsys):
    with patch('application.db_procedures.psycopg2.connect') as mock_conn:
        mock_cur = MagicMock()
        mock_cur.__enter__.return_value.fetchall.return_value = [("auction",), ("bids",)]
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cur

        with patch('application.db_procedures.create_auction_table') as mock_create_auction_table, \
            patch('application.db_procedures.create_bids_table') as mock_create_bids_table:
            initialize_tables(save_database=False)

            sql_drop_calls = [
                call("DROP TABLE auction CASCADE;"),
                call("DROP TABLE bids CASCADE;")
            ]
            mock_cur.__enter__.return_value.execute.assert_has_calls(calls=sql_drop_calls, any_order=True)  # simulate & assert the order of SQL calls

            mock_create_auction_table.assert_called_once()  # note & remember that because this function is patched (above, in the `with`), it doesn't actually execute; `assert_called_once()` only asserts whether it would be called
            mock_create_bids_table.assert_called_once()  # asserts call but doesn't actually execute

            captured_output, err = capsys.readouterr()

            expected_output_lines = [
                "Initiating database setup:",
                "\t- Found existing tables",
                "\t- Deleted tables: [('auction',), ('bids',)]",
            ]
            ##################################
            # While it's okay you wanted to test & see outputs here, this is more of an integration thing.
            # If you did wanted to test the print() statements in create_auction_table() and mock_create_bids_table() you would have to use side_effect().
            # However, especially in unit tests, focus on behavior & outcomes, over results (end-to-end output).
            # Typically, unit tests should focus more on the behavior and outcomes of your functions rather than their internal implementation details, such as whether they print specific messages. Verifying that create_auction_table() and create_bids_table() are called is usually sufficient for unit testing purposes. If you specifically need to test the output of these functions, consider integration tests that run the actual functions rather than mocking them, in an environment where side effects (like database modifications) are controlled or isolated.
            # In summary, for your current unit test setup, focusing on whether create_auction_table() and create_bids_table() are called is typically sufficient, and it's common for the actual body of mocked functions NOT to execute here.
            ##################################

            for line in expected_output_lines:
                assert line in captured_output


def test_create_auction_table():
    mock_conn = MagicMock()
    create_auction_table(mock_conn)

    mock_conn.cursor.return_value.__enter__.return_value.execute.assert_called_once_with("""
            CREATE TABLE auction (
                item            VARCHAR(30)     PRIMARY KEY NOT NULL,
                seller          INTEGER                     NOT NULL,
                reserve_price   NUMERIC(5, 2)               NOT NULL,
                opening_time    INTEGER                     NOT NULL,
                closing_time    INTEGER                     NOT NULL,
                status          VARCHAR(6)
            );""")  # checks that the mock was called exactly once, and with the specified arguments


def test_process_listing():
    auction_listing_line = ["10", "1", "toaster_1", "10.00", "20"]

    with patch('application.db_procedures.psycopg2.connect') as mock_conn:
        process_listing(*auction_listing_line)

        mock_conn.return_value.cursor.return_value.__enter__.return_value.execute.assert_called_once_with(
            """
            INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
            VALUES (%s, %s, %s, %s, %s, 'UNSOLD');
        """, ("toaster_1", "1", "10.00", "10", "20")
            )


def test_bid_check_after_closing_time():
    auction_bid_line = ["5", "21", "tea_pot_1", "9.50"]

    with patch('application.db_procedures.psycopg2.connect') as mock_conn:
        mock_conn.return_value.cursor.return_value.__enter__.return_value.fetchone.return_value = [20, "UNSOLD", 8.50]
        result = bid_check(*auction_bid_line)

        assert result == False
