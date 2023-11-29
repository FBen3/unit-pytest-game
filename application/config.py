import configparser
import os

# calculate current directory
current_dir = os.path.abspath(os.path.dirname(__file__))

# calculate project root
root_dir = os.path.dirname(current_dir)

# construct path to config.ini
ini_config_path = os.path.join(root_dir, 'config.ini')

config = configparser.ConfigParser()
config.read(ini_config_path)

db_conn_params = {
    "dbname": config['database']['dbname'],
    "user": config['database']['user'],
    "password": config['database']['password'],
    "host": config['database']['host'],
    "port": config['database']['port']
}
