# ----
# Validation of Configuration Loading: Ensure that your application can correctly read and parse the configuration file.
# This includes handling missing files, incorrect formats, or missing sections/keys gracefully.
#
# Correct Application of Configuration Values: Tests can verify that configuration values are correctly applied within
# your application, for example, by checking if the database connection parameters are correctly set. ?????????????????????????? [integration] ??????? ask
#
# Unit Tests (unit/): If you're testing the functionality of config.py in isolation,
# such as its ability to read and parse different configurations or handle errors without
# actually interacting with a real config.ini file (e.g., by mocking file reading operations),
# these tests belong in the unit/ directory.
# ----

from unittest.mock import mock_open, patch

import pytest

from application.config import db_conn_params


# validation of config loading: ensure that config.py can correctly read & parse the config.ini
# pay attention to: handling missing files, incorrect formats, or missing sections/keys


@patch('configparser.ConfigParser.read')
@patch('builtins.open', mock_open(read_data=3))
def test_config_ini_is_correctly_read_and_parsed():
    pass








