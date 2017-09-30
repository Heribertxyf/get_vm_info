# -*- coding: utf-8 -*-
""" get_vm_info init file"""

from __future__ import unicode_literals, absolute_import
import os
from logbook import Logger, FileHandler, set_datetime_format

from flask import Flask
from flask_admin import Admin

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_BASE_DIR = os.path.join(BASE_DIR, 'logs')
DATA_DIR = os.path.join(BASE_DIR, 'data')
UPLOAD_DIR = os.path.join(DATA_DIR, 'upload')
DOWNLOAD_DIR = os.path.join(DATA_DIR, 'download')
VMINFO_URL = 'http://10.13.2.133:6101/v1/resop/vm/vm_info/'
GET_CUSTOMER_BYNO_URL = 'http://10.13.2.235:6003/customer/getCustomerByNo'


def logger_config(logger_name, log_path):
    """
        根据logger名称和文件位置，封装logger
    :logger_name: string, logger name
    :log_path: log file path with LOG_BASE_DIR e.g:xxx.log
    :return: logger
    """
    log_dir = os.path.join(LOG_BASE_DIR, log_path)
    handler = FileHandler(log_dir)
    handler.push_application()
    logger = Logger(logger_name)
    set_datetime_format('local')
    return logger


class Config(object):
    EMAIL_HOST = ''
    EMAIL_PORT = ''
    EMAIL_USER = ''
    EMAIL_PASSWORD = ''

    def __init__(self):
        pass


class ProductionConfig(Config):
    DEBUG = False
    DB_ENGINE = 'mysql'
    DB_HOST = '10.128.100.45'
    DB_NAME = 'get_vm_info'
    DB_USER = 'cdsops'
    DB_PASSWORD = '2EgfoX1BMwQy'
    DB_PORT = 3306


class DevelopmentConfig(object):
    DEBUG = True
    DB_ENGINE = 'mysql'
    DB_HOST = '127.0.0.1'
    DB_NAME = 'get_vm_info'
    DB_USER = 'xujpxm'
    DB_PASSWORD = '123456'
    DB_PORT = 3306


ENV_CONFIG = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

DB_CONFIG = ENV_CONFIG.get(os.environ.get('ENV_CONFIG', 'development'))
SQLALCHEMY_DATABASE_URI = '%s://%s:%s@%s:%s/%s' % (DB_CONFIG.DB_ENGINE, DB_CONFIG.DB_USER,
                                                   DB_CONFIG.DB_PASSWORD, DB_CONFIG.DB_HOST, DB_CONFIG.DB_PORT, DB_CONFIG.DB_NAME)

from get_vm_info.views import upload
from get_vm_info.models import db
from get_vm_info.admin import admin

get_vm_info_app = Flask(__name__)
get_vm_info_app.config['UPLOAD_FOLDER'] = UPLOAD_DIR
get_vm_info_app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
get_vm_info_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
get_vm_info_app.config['SECRET_KEY'] = os.urandom(24)
db.init_app(get_vm_info_app)
get_vm_info_app.register_blueprint(upload)
admin.init_app(get_vm_info_app)
