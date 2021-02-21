# -*- encoding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
from app.blueprints.dashboard import dashboard_bp
from app.blueprints.user import user_bp
import json
import connexion

db = SQLAlchemy()
login_manager = LoginManager()

def read_plugin_config(vis_config_file=None):
    """ Read the plugin configuration JSON file from a path, if its None, uses a default configuration """
    if vis_config_file != None:
        file_path = vis_config_file
    else:
        file_path = path.dirname(path.abspath(__file__)) + "//data_logger.json"
    with open(file_path) as f:
        data = json.load(f)
    return data

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)
        

# If it is the first time the app is run, create the database and perform data seeding
def configure_database(app):
    print("Configuring database")
#    #@app.before_first_request
#    def initialize_database():
#        print("Creating database")
#        from models.user import User
#        db.create_all()
#        print("Seeding database")
#        from models.user_seed import user_seed
#        user_seed(app, db)

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()
    
def create_db(app):
    db = SQLAlchemy()
    db.init_app(app)
    return db


def create_app(config):
    # app = Flask(__name__, static_folder='base/static')
    app = connexion.App(__name__, specification_dir='./')

    # Read the swagger.yml file to configure the endpoints
    app.add_api('DataLogger-OAS.apic.yaml')

    # set Flast static_folder  to be used with connexion
    app.static_url_path = '/base/static'

    ## remove old static map
    #url_map = app.url_map
    #try:
    #    for rule in url_map.iter_rules('static'):
    #        url_map._rules.remove(rule)
    #except ValueError:
    #    # no static view was created yet
    #    pass

    ## register new; the same view function is used
    #app.add_url_rule(
    #    app.static_url_path + '/<path:filename>',
    #    endpoint='static', view_func=app.send_static_file()) 

     # read plugin configuration JSON file
    p_config = read_plugin_config()
    # initialize FeatureExtractor
    ###fe = FeatureExtractor(p_config)
    # set flask app parameters
    ### app.config.from_object(config)
    # plugin configuration from data_logger.json
    app.config['P_CONFIG'] = p_config 
    # data_logger instance with plugins already loaded
    app.config['FE'] = fe
    register_extensions(app)
    # get the output plugin template folder
    plugin_folder = fe.ep_output.template_path(p_config)
    ## construct the blueprint with configurable plugin_folder for the dashboard views
    #tmp = dashboard_bp(plugin_folder)
    #app.register_blueprint(tmp)
    ## construct the blueprint for the users views
    #tmp = user_bp(plugin_folder)
    #app.register_blueprint(tmp)


    # register the blueprints
    register_blueprints(app)
    configure_database(app)
    
    return app
