import psycopg2


### move this out after ###
db_conn_params = {
    "dbname": "auction_db",
    "user": "benf",
    "password": "superusrpass",
    "host": "localhost",
    "port": "5432"
}


def process_listing(opening_time, seller, item, reserve_price, closing_time):
    ##### catch error in test: psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "auction_pkey"
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as curr:
            curr.execute("""
                INSERT INTO auction (item, seller, reserve_price, opening_time, closing_time, status) 
                VALUES (%s, %s, %s, %s, %s, 'UNSOLD');
            """, (item, seller, reserve_price, opening_time, closing_time))

def process_bidding(bid_time, bidder, item, amount):
    with psycopg2.connect(**db_conn_params) as conn:
        with conn.cursor() as curr:
            curr.execute("""
                   INSERT INTO bids (item, amount, bid_time, bidder) 
                   VALUES (%s, %s, %s, %s);
               """, (item, amount, bid_time, bidder))


