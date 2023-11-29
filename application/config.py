import configparser
import os.path

# calculate current directory
config_dir = os.path.abspath(os.path.dirname(__file__))

# construct path to config.ini
ini_config_path = os.path.join(config_dir, 'config.py')

config = configparser.ConfigParser()
config.read(ini_config_path)

db_conn_params = {
    "dbname": config['database']['dbname'],
    "user": config['database']['user'],
    "password": config['database']['password'],
    "host": config['database']['host'],
    "port": config['database']['port']
}
