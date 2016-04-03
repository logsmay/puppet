import configparser
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from models.puppet_model import PuppetModel, Account


class PuppetBase(object):
    def __init__(self):
        _basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.db_config = configparser.ConfigParser()
        self.db_config.read(os.path.join(_basedir, 'config', 'credentials', 'db.ini'))
        self.db_session = {}

        _engine = create_engine('mysql+mysqldb://%s:%s@%s/%s' % (
            self.db_config['PUPPET']['Username'],
            self.db_config['PUPPET']['Password'],
            self.db_config['PUPPET']['Host'],
            self.db_config['PUPPET']['Database']
        ), echo=True)

        # Bind the engine to the metadata of the PuppetBase class so that the
        # declaratives can be accessed through a DBSession instance
        PuppetModel.metadata.bind = _engine

        _db_session = sessionmaker(bind=_engine)
        self.db_session['puppet'] = _db_session()

    def get_db(self, db_name) -> Session:
        if db_name in self.db_session:
            return self.db_session[db_name]
        else:
            raise Exception('Database not found')