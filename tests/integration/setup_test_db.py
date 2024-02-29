import psycopg2
from psycopg2 import pool

from application.config import fetch_database_params
from application.db_procedures import initialize_tables


admin_db_conn_params = fetch_database_params()
admin_db_conn_params["dbname"] = "postgres"

def initialize_test_db():
    # DROP DATABASE and CREATE DATABASE cannot run inside a transaction block. (by default, psycopg2 operations are part of transaction in the context of a connection)
    # you need to run DROP DATABASE and CREATE DATABASE outside of a transaction block in order to execute them.
    # thus you need to manually manage the connection (without of wrapping it in a `with`; which automatically wraps stuff in transaction).
    # to manually manage the connection: first open it, set autocommit=True before any commands are executed, then manually close it afterward.
    # by setting autocommit to True before executing any cursor operations, you ensure that commands are executed immediately (as opposed to part of a transaction).
    conn = psycopg2.connect(**admin_db_conn_params)
    conn.autocommit = True

    with conn.cursor() as cur:
        cur.execute("DROP DATABASE IF EXISTS test_auction_db")
        cur.execute("CREATE DATABASE test_auction_db")

    conn.close()


test_db_conn_params = fetch_database_params("../fixtures/test_db_config.ini")

def initialize_test_db_tables():
    initialize_tables(save_database=False, db_conn=test_db_conn_params)


def init_connection_pool():
    return pool.SimpleConnectionPool(1,10, **test_db_conn_params)
