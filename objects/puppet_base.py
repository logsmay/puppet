import configparser
import os

import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, Session

from models.puppet_model import PuppetModel


class PuppetBase(object):
    def __init__(self):
        _basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        self.db_config = configparser.ConfigParser()
        self.db_config.read(os.path.join(_basedir, 'config', 'credentials', 'db.ini'))
        self.db_session = {}

        # ################# #
        # MASTER DATA STORE #
        # ################# #
        _engine = create_engine('mysql+mysqldb://%s:%s@%s/%s' % (
            self.db_config['PUPPET']['Username'],
            self.db_config['PUPPET']['Password'],
            self.db_config['PUPPET']['Host'],
            self.db_config['PUPPET']['Database']
        ), echo=True)

        # Bind the engine to the metadata of the PuppetBase class so that the
        # declaratives can be accessed through a DBSession instance
        PuppetModel.metadata.bind = _engine

        _db_session = scoped_session(sessionmaker(bind=_engine))
        self.db_session['puppet'] = _db_session()

        # ################## #
        # SESSION DATA CACHE #
        # ################## #
        self.db_session['session-cache'] = redis.StrictRedis(
            host=self.db_config['SESSION-CACHE']['Host'],
            port=self.db_config['SESSION-CACHE']['Port'],
            db=self.db_config['SESSION-CACHE']['Database'],
            socket_connect_timeout=3,

        )

    def get_db(self, db_name) -> Session:
        if db_name in self.db_session:
            return self.db_session[db_name]
        else:
            raise Exception('Database not found')
