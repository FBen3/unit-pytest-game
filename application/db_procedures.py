import psycopg2

from application.config import db_conn_params


def process_bidding(bid_time, bidder, item, amount):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as curr:
            curr.execute("""
                   INSERT INTO bids (item, amount, bid_time, bidder) 
                   VALUES (%s, %s, %s, %s);
               """, (item, amount, bid_time, bidder))

def process_listing(opening_time, seller, item, reserve_price, closing_time):
    ##### catch error in test: psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "auction_pkey"
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as curr:
            curr.execute("""
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
                amount      NUMERIC(4, 2)   NOT NULL,
                bid_time    INTEGER         NOT NULL,
                bidder      INTEGER         NOT NULL,
                FOREIGN KEY (item) REFERENCES auction(item)
            );
        """)

def create_auction_table(connection):
    print("\t- Creating auction table")

    with connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE auction (
                item            VARCHAR(30)     PRIMARY KEY NOT NULL,
                seller          INTEGER                     NOT NULL,
                reserve_price   NUMERIC(4, 2)               NOT NULL,
                opening_time    INTEGER                     NOT NULL,
                closing_time    INTEGER                     NOT NULL,
                status          VARCHAR(6)
            );
        """)
