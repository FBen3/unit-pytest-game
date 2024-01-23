import psycopg2

from application.config import db_conn_params


def bid_check(bidder, bid_time, item, amount):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    a.closing_time,
                    a.status,
                    MAX(b.amount) AS highest_bid_by_user
                FROM
                    auction a
                LEFT JOIN
                    bids b ON a.item = b.item AND b.bidder = %s
                WHERE
                    a.item = %s
                GROUP BY
                    a.reserve_price, a.closing_time, a.status;
            """, (bidder, item))

            closing_time, status, highest_bid  = cur.fetchone()

    if status == "UNSOLD" and int(bid_time) < closing_time:
        if highest_bid and highest_bid < amount:
            return False
        return True # accept any initial amount

    return False

def process_bidding(bid_time, bidder, item, bid_amount):
    if bid_check(bidder, bid_time, item, bid_amount):
        with psycopg2.connect(**db_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                       INSERT INTO bids (item, amount, bid_time, bidder) 
                       VALUES (%s, %s, %s, %s);
                   """, (item, bid_amount, bid_time, bidder))
    else:
        raise PermissionError("Bid does not meet requirements")

def process_listing(opening_time, seller, item, reserve_price, closing_time):
    ##### catch error in test: psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "auction_key"
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
                VALUES (%s, %s, %s, %s, %s, 'UNSOLD');
            """, (item, seller, reserve_price, opening_time, closing_time))

def create_bids_table(connection):
    print("\t- Creating bids table")

    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE bids (
                id          SERIAL          PRIMARY KEY,
                item        VARCHAR(30)     NOT NULL,
                amount      NUMERIC(5, 2)   NOT NULL,
                bid_time    INTEGER         NOT NULL,
                bidder      INTEGER         NOT NULL,
                FOREIGN KEY (item) REFERENCES auction(item)
            );""")

def create_auction_table(connection):
    print("\t- Creating auction table")

    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE auction (
                item            VARCHAR(30)     PRIMARY KEY NOT NULL,
                seller          INTEGER                     NOT NULL,
                reserve_price   NUMERIC(5, 2)               NOT NULL,
                opening_time    INTEGER                     NOT NULL,
                closing_time    INTEGER                     NOT NULL,
                status          VARCHAR(6)
            );""")

def initialize_tables(save_database: bool):
    print("Initiating database setup:")
    if not save_database:
        try:
            # connect to database (open & close connections automatically)
            with psycopg2.connect(**db_conn_params) as conn:
                # manage database resources (cursor object)
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'""")
                    tables = cur.fetchall()

                    if tables:
                        print("\t- Found existing tables")
                        for table in tables:
                            cur.execute(f"DROP TABLE {table[0]} CASCADE;")
                        print(f"\t- Deleted tables: {tables}")

                create_auction_table(conn)
                create_bids_table(conn)

        except psycopg2.DatabaseError as e:
            print(f"An error occured while initializing DB tables: {e}")
            raise e

        except Exception as e:
            print(f"Some error occured: {e}")
            raise e
    else:
        print(f"\t- Using existing database")
