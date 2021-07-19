# -*- encoding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler
from os import path
import json
import connexion
from flask import current_app
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('base', 'home'):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def create_app(app_config, data_logger):
    """ Create the Flask-Sqlalchemy app 
    Args:
    app_config (dict): flask app config data
    data_logger (obj): DataLogger class instance

    Returns:
    app.app (dict): the flask-sqlalchemy app instance
    """    

    # read the Connexion swagger yaml specification_dir from the core plugin entry point
    specification_dir = data_logger.core_ep.specification_dir
    app = connexion.App(__name__, specification_dir = specification_dir)
    # read the Connexion swagger yaml specification filename from the core plugin entry point
    specification_filename = data_logger.core_ep.specification_filename
    #app.add_api('DataLogger-OAS.apic.yaml')
    app.add_api(specification_filename)
    # set Flask static_folder  to be used with Connexion from the gui plugin entry point 
    static_url_path = data_logger.gui_ep.static_url_path
    #app.app.static_url_path = '/base/static'
    app.app.static_url_path = static_url_path
  # remove old static map
    url_map = app.app.url_map
    try:
        for rule in url_map.iter_rules('static'):
            url_map._rules.remove(rule)
    except ValueError:
        # no static view was created yet
        pass

    # register new; the same view function is used
    app.app.add_url_rule(app.app.static_url_path + '/<path:filename>',endpoint='static', view_func=app.app.send_static_file)

     # read plugin configuration JSON file
    #p_config = read_plugin_config()
    # initialize FeatureExtractor
    ###fe = FeatureExtractor(p_config)
    # set flask app parameters
    app.app.config.from_object(app_config)
    # plugin configuration from data_logger.json
    #app.app.config['P_CONFIG'] = p_config 
    # data_logger instance with plugins already loaded
    ### current_app.config['FE'] = fe
    register_extensions(app.app)
    # get the output plugin template folder
    ### plugin_folder = fe.ep_output.template_path(p_config)
    ## construct the blueprint with configurable plugin_folder for the dashboard views
    #tmp = dashboard_bp(plugin_folder)
    #app.register_blueprint(tmp)
    ## construct the blueprint for the users views
    #tmp = user_bp(plugin_folder)
    #app.register_blueprint(tmp)


    # register the blueprints
    register_blueprints(app.app)
    
    print("\n#1\n")
    #init_db(app.app)
    # If it is the first time the app is run, create the database and perform data seeding
    @app.app.before_first_request
    def ini_db():
        # TODO: AFTER TESTING, REMOVE FROM HERE
        print("Dropping database")
        db.drop_all()
        print("done.")
        from models.user import User
        from models.process import Process
        print("Creating database")
        db.create_all()
        print("Seeding database with test user")
        from models.seeds.user import seed
        seed(app.app, db)
        # TODO: REMOVE UP TO HERE
        # reflect the tables
        db.Model.metadata.reflect(bind=db.engine)
        Base = automap_base()
        Base.prepare(db.engine, reflect=True)
        #print("tables=", db.metadata.tables)
    #    @app.before_first_request
    #    def initialize_database():
    #        pass
    #    @app.teardown_request
    #    def shutdown_session(exception=None):
    #        db.session.remove()

    
    return app.app
