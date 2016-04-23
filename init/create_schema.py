import configparser
import os

from sqlalchemy import create_engine

from models.puppet_model import PuppetModel


class CreateSchema(object):
    def __init__(self):
        _basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.db_config = configparser.ConfigParser()
        self.db_config.read(os.path.join(_basedir, 'config', 'credentials', 'db.ini'))

        _engine = create_engine('mysql+mysqldb://%s:%s@%s/%s' % (
            self.db_config['PUPPET']['Username'],
            self.db_config['PUPPET']['Password'],
            self.db_config['PUPPET']['Host'],
            self.db_config['PUPPET']['Database']
        ), echo=True)

        PuppetModel.metadata.create_all(_engine)


CreateSchema()
