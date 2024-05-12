import inspect
import logging
import sys

import sqlalchemy


def get_columns_table(table):
    return table.__table__.columns


def show_tables(engine):
    return sqlalchemy.inspect(engine).get_table_names()


def table_exists(engine, table_name):
    return True if table_name in show_tables(engine) else False


def connect(echo=True,
            host='localhost',
            port='5432',
            database='herbario'):
    try:
        url = 'postgresql+psycopg2://%s:%s@%s:%s/%s' % ('xandao', 'madu', host, port, database)
        engine = sqlalchemy.create_engine(url, echo=echo, pool_pre_ping=True)
        session = sqlalchemy.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        if engine.connect():
            return engine, session()
    except Exception as e:
        print(e)


def is_query_empty(count):
    return count == 0


def create_table(base, engine):
    # cls[0] -> name, cls[1] -> obj
    classes = [cls for cls in inspect.getmembers(sys.modules['models'], inspect.isclass) if
               'base' not in cls[0].lower()]

    insp = sqlalchemy.inspect(engine)
    tables = insp.get_table_names()
    for c in classes:
        if c[1].__table__.name not in tables:
            table_name = c[1].__table__.name
            base.metadata.tables[table_name].create(bind=engine)
            logging.info('Created table %s' % table_name)
