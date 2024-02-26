import configparser
import os


def fetch_database_params(config_path=None):
    if not config_path:
        # default to the project root directory if no specific path is provided
        current_dir = os.path.abspath(os.path.dirname(__file__))
        root_dir = os.path.dirname(current_dir)
        config_path = os.path.join(root_dir, "config.ini")

    config = configparser.ConfigParser()
    if not config.read(config_path):
        raise FileNotFoundError(f"Could not find or read the config.ini file at location: {config_path}")

    db_conn_params = {
        "dbname": config["database"]["dbname"],
        "user": config["database"]["user"],
        "password": config["database"]["password"],
        "host": config["database"]["host"],
        "port": config["database"]["port"],
    }

    return db_conn_params
