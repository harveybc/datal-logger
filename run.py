# -*- encoding: utf-8 -*-
""" DataLogger: Run script.
    Description: Initializes the plugin system and starts the application.
    This script is called by the command 'flask run' in the startup scripts 'data_logger.sh' and 'data_logger.bat', 
    where FLASK_APP env variable is set to 'run.py'(this script).
"""

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
from json import load as json_load
from app.app import create_app
from app.data_logger import DataLogger

# load the plugin config files
print(" * Loading plugin configuration files")
try:
    with open("config_store.json", "r") as conf_file:
        store_plugin_conf = json_load(conf_file)
    with open("config_core.json", "r") as conf_file:
        core_plugin_conf = json_load(conf_file)
    with open("config_gui.json", "r") as conf_file:
        gui_plugin_conf = json_load(conf_file)
except Exception as e:
    print(e)
    exit(e)
# initialize plugin system
print(" * Creating data_logger instance...")
data_logger = DataLogger(store_plugin_conf, core_plugin_conf, gui_plugin_conf)
# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True)
# setup config mode
get_config_mode = 'Debug' if DEBUG else 'Production'
# load config from the config_dict according to the set config mode.
try:
    # load the config_dict from the store plugin entry point (instance of the selected store plugin's class)
    config_dict = data_logger.store_ep.get_config_dict()
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')
app = create_app( app_config, data_logger)

