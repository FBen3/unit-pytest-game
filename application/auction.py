import os

import psycopg2

from application.item import Item


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
                    item_owner  INTEGER         NOT NULL,
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
                            cur.execute(f'DROP TABLE {table[0]} CASCADE;')
                        print(f"\t- Deleted tables: {tables}")
                        conn.commit()

                self.create_auction_table(conn)
                self.create_bids_table(conn)

        except psycopg2.DatabaseError as e:
            print(f"An error occurred while initializing DB tables: {e}")
            raise e

        except Exception as e:
            print(f"Some error occurred: {e}")
            raise e


    # these 3 functions will reference functions from db_procedures.py where all the database read/write logic will be
    def start(self, input_path, step=None):
        pass

    def report(self):
        pass

    def close(self):
        pass


if __name__ == "__main__":
    auction = Auction()


























    # def process_listing(self, listing: Item):
    #     if listing.item in self.auction_records:
    #         raise KeyError("Item is already being sold!")
    #     else:
    #         self.auction_records[listing.item] = listing
    #         self.closing_records.setdefault(listing.auction_end_time, [])
    #         self.closing_records[listing.auction_end_time].append(listing.item)
    #
    # def process_bidding(self, bidding: list):
    #     item = bidding[3]
    #     item_start_time = self.auction_records[item].auction_start_time
    #     item_close_time = self.auction_records[item].auction_end_time
    #     bid_time = int(bidding[0])
    #     bidding_user = int(bidding[1])
    #     bid_amount = float(bidding[4])
    #
    #     if (item_start_time < bid_time < item_close_time) and (bid_amount > 0):
    #         self.auction_records[item].submit_bid(
    #             bidding_user, bid_time, bid_amount
    #         )
    #
    # def process_input(self, line: str):
    #     split_line = line.split("|")
    #
    #     # do not process heartbeat messages
    #     if len(split_line) > 1:
    #         if split_line[2] == "SELL":
    #             # exclude 'SELL' string
    #             del split_line[2]
    #             self.process_listing(Item(*split_line))
    #         elif split_line[2] == "BID":
    #             self.process_bidding(split_line)
    #         else:
    #             raise ValueError("Could not find input action")
    #
    # def start(self):
    #     if len(self.input_file) != 1:
    #         raise IndexError("Please specify 1 argument")
    #     else:
    #         path_argument = self.input_file[0]
    #         if os.path.isfile(path_argument):
    #             file_name = os.path.basename(path_argument)
    #             _, extension = file_name.split(".")
    #             if extension == "txt":
    #                 with open(path_argument, "r") as reader:
    #                     for line in reader:
    #                         self.process_input(line.strip())
    #             else:
    #                 raise TypeError("Input must be a text file")
    #         else:
    #             raise FileNotFoundError("Could not find file")
    #
    # def close(self):
    #     for time in self.closing_records:
    #         for item in self.closing_records[time]:
    #             self.auction_records[item].winner()
