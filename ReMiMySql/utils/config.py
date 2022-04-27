# -*- coding: utf-8 -*-
import os


def vars_config(app):
    print('Config App')
    app.config['SQLALCHEMY_DATABASE_URI'] = app.config['SQLALCHEMY_DATABASE_URI'].format(
        os.getenv('DB_USER', 'remi'),
        os.getenv('DB_PASSWORD', 'Mi_Secreto0'),
        os.getenv('DB_HOST', 'localhost'),
        os.getenv('DB_PORT', '3306'),
        os.getenv('DB_NAME', 'remi')
    )
    env = os.getenv('FLASK_ENV', 'production')
    if env == 'production':
        app.config['SQLALCHEMY_ECHO'] = False
        print('Run in production mode')
    else:
        print('FLASK_ENV', os.getenv('FLASK_ENV'))
    return app
