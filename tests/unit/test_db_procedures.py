import pytest

from unittest.mock import patch, MagicMock

from application.db_procedures import *


def test_initialize_tables():
    with (patch('application.db_procedures.psycopg2.connect') as mock_conn):
        mock_cur = MagicMock()
        mock_cur.__enter__.return_value.fetchall.return_value = []  # mock empty database
        mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cur  # mock connection to empty use empty database

        with patch('application.db_procedures.create_auction_table') as mock_create_auction_table, \
            patch('application.db_procedures.create_bids_table') as mock_create_bids_table:
            initialize_tables(save_database=False)
            mock_cur.__enter__.return_value.execute.assert_called_with("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'""")

            mock_conn.return_value.__enter__.return_value.cursor.return_value = mock_cur


            mock_create_auction_table.assert_called_once()
            mock_create_bids_table.assert_called_once()






# save_database=False, no tables are fetched, create_auction_table() & create_bids_table() executes; no errors are thrown [OK]
# save_database=False, tables are found, check print() statement, assert&mock execute DROP table, create_auction_table() & create_bids_table() executes; no errors are thrown



# def test_get_all_items(mock_db_response):
#     with patch('application.db_procedures.psycopg2.connect') as mock_connect:
#         mock_cursor = mock_connect.return_value.cursor.return_value
#         mock_cursor.fetchall.return_value = mock_db_response
#
#         result = get_all_items()
#
#         assert result == mock_db_response
#
# def test_insert_item():
#     with patch('application.db_procedures.psycopg2.connect') as mock_connect:
#         mock_cursor = mock_connect.return_value.cursor.return_value
#
#         # Assume insert_item() is the function to test
#         insert_item('Item 3', 'Description of item 3')
#
#       --------
#         mock_cursor.execute.assert_called_with(
#             "INSERT INTO items (name, description) VALUES (%s, %s)",
#             ('Item 3', 'Description of item 3')
#         )
#       --------












