from decimal import Decimal

import psycopg2

from application.config import db_conn_params


def update_status(item):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE auction SET status = 'SOLD' WHERE item = %s", (item,))


def all_unexpired_items(time):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT item FROM auction WHERE status = 'UNSOLD' AND closing_time <= %s", (time,))
            all_auctioned_items = [row[0] for row in cur.fetchall()]

    return all_auctioned_items


def calculate_price_paid_for_item(highest_bid, second_highest_bid, reserve_price, total_bid_count, **kwargs):
    if total_bid_count == 0:
        return 0

    if highest_bid < reserve_price:
        return 0

    if total_bid_count == 1:
        return reserve_price

    return second_highest_bid


def calculate_final_item_stats(item):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT 
                    a.item,
                    a.closing_time,
                    a.reserve_price,
                    a.status,
                    bid_details.max_bidder,
                    bid_details.max_amount,
                    bid_stats.min_amount,
                    bid_stats.total_bid_count,
                    second_highest_bid.second_max_amount
                FROM 
                    auction a
                JOIN (
                    SELECT 
                        b1.item,
                        b1.bidder as max_bidder,
                        b1.amount as max_amount
                    FROM 
                        bids b1
                    JOIN (
                        SELECT 
                            item, 
                            MAX(amount) as max_amount
                        FROM 
                            bids
                        WHERE 
                            item = %s
                        GROUP BY 
                            item
                    ) max_bids ON b1.item = max_bids.item AND b1.amount = max_bids.max_amount
                    WHERE 
                        b1.item = %s
                    ORDER BY 
                        b1.bid_time ASC
                    LIMIT 1
                ) bid_details ON a.item = bid_details.item
                JOIN (
                    SELECT 
                        item,
                        MIN(amount) as min_amount,
                        COUNT(id) as total_bid_count
                    FROM 
                        bids
                    WHERE 
                        item = %s
                    GROUP BY 
                        item
                ) bid_stats ON a.item = bid_stats.item
                LEFT JOIN (
                    SELECT 
                        item,
                        amount AS second_max_amount
                    FROM (
                        SELECT 
                            item,
                            amount,
                            ROW_NUMBER() OVER (PARTITION BY item ORDER BY amount DESC) as bid_rank
                        FROM 
                            bids
                        WHERE 
                            item = %s
                    ) ranked_bids
                    WHERE 
                        bid_rank = 2
                ) second_highest_bid ON a.item = second_highest_bid.item
                WHERE 
                    a.item = %s;
            """, (item, item, item, item, item))

            stats = cur.fetchone()

            stats_dict = {
                "item": stats[0],
                "bidder": stats[4],
                "highest_bid": float(stats[5]),
                "second_highest_bid": float(stats[8]) if stats[8] else None,
                "lowest_bid": float(stats[6]),
                "total_bid_count": stats[7],
                "reserve_price": stats[2],
                "closing_time": stats[1],
                "status": stats[3]
            }

            return stats_dict


def bid_check(bidder, bid_time, item, amount):
    ##### catch error in test: if closing_time is after clock time
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
        if highest_bid and Decimal(amount) < highest_bid:
            return False
        return True # accept any initial amount

    return False


def process_bidding(bid_time, bidder, item, bid_amount):
    if bid_check(bidder, bid_time, item, bid_amount): # invalid bids are not recorded
        with psycopg2.connect(**db_conn_params) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                       INSERT INTO bids (item, amount, bid_time, bidder) 
                       VALUES (%s, %s, %s, %s);
                   """, (item, bid_amount, bid_time, bidder))


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
            with psycopg2.connect(**db_conn_params) as conn: # connect to database (open & close connections automatically)
                with conn.cursor() as cur: # manage database resources (cursor object)
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
            print(f"An error occurred while initializing DB tables: {e}")
            raise e

        except Exception as e:
            print(f"Some error occurred: {e}")
            raise e
    else:
        print(f"\t- Using existing database")
