import os

import psycopg2

from application.db_procedures import *


### move this out after ###
db_conn_params = {
    "dbname": "auction_db",
    "user": "benf",
    "password": "superusrpass",
    "host": "localhost",
    "port": "5432"
}


class Auction:


    def __init__(self):
        self.initialize_tables()

    @staticmethod
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

    @staticmethod
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

    def initialize_tables(self):
        print("Initiating database setup:")
        try:
            # connect to database (open & close connections automatically)
            with psycopg2.connect(**db_conn_params) as conn:
                # manage database resources (cursor object)
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name
                        FROM information_schema.tables
                        WHERE table_schema = 'public'
                    """)
                    tables = cur.fetchall()

                    if tables:
                        print("\t- Found existing tables")
                        for table in tables:
                            cur.execute(f"DROP TABLE {table[0]} CASCADE;")
                        print(f"\t- Deleted tables: {tables}")

                self.create_auction_table(conn)
                self.create_bids_table(conn)

        except psycopg2.DatabaseError as e:
            print(f"An error occurred while initializing DB tables: {e}")
            raise e

        except Exception as e:
            print(f"Some error occurred: {e}")
            raise e

    @staticmethod
    def process_input(line: str):
        split_line = line.split("|")

        # do not process heartbeat messages
        if len(split_line) > 1:
            if split_line[2] == "SELL":
                # exclude 'SELL' string
                del split_line[2]
                try:
                    process_listing(*split_line)
                except Exception as e:
                    print(f"Listing error: {e}")
                    raise e
            elif split_line[2] == "BID":
                del split_line[2]
                try:
                    process_bidding(*split_line)
                except Exception as e:
                    print(f"Bidding error: {e}")
                    raise e
            else:
                raise ValueError("Could not find input action")

    def start(self, input_path):
        if len(input_path) != 1:
            raise IndexError("Please specify 1 argument")
        else:
            path_argument = input_path[0]
            if os.path.isfile(path_argument):
                file_name = os.path.basename(path_argument)
                _, extension = file_name.split(".")
                if extension == "txt":
                    with open(path_argument, "r") as reader:
                        for line in reader:
                            self.process_input(line.strip())

                else:
                    raise TypeError("Input must be a text file")
            else:
                raise FileNotFoundError("Could not find file")

    def report(self):
        pass

    def close(self):
        pass


if __name__ == "__main__":
    auction = Auction()
    auction.start(['../my_test.txt'])


