import os

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

from tables import get_base

user = os.environ['POSTGRE_USER']
password = os.environ['POSTGRE_PASSWORD']
cfg = {
    'host': '192.168.0.144',
    'user': user,
    'password': password,
    'port': '5432',
    'database': 'herbario'
}


def connect():
    try:
        engine = sqlalchemy.create_engine(
            f"postgresql+psycopg2://{cfg['user']}:{cfg['password']}@{cfg['host']}:{cfg['port']}/{cfg['database']}", echo=True,
            pool_pre_ping=True)
        Session = sqlalchemy.orm.sessionmaker(bind=engine)
        Session.configure(bind=engine)
        session = Session()
        if engine.connect():
            return engine, session
    except Exception as e:
        print(f"problems with host %s (%s)" % (cfg['host'], e))


def make_operation(session):
    try:
        session.commit()
        session.flush()
    except Exception as e:
        session.rollback()
        print(e)
        raise
# finally:
#     session.close()


def list_ilike(attribute, list_of_values):
    return [attribute.ilike(value) for value in list_of_values]


def create_table_if_not_exists(cfg, engine, table_name):
    if not engine.has_table(table_name, schema=cfg['database']):
        get_base().metadata.create_all(engine)
