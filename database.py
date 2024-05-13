import inspect
import logging
import sys

import sqlalchemy
import sqlalchemy as sa


def connect():
    url_object = sa.URL.create(
        "postgresql+psycopg2",
        username="xandao",
        password="madu",  # plain (unescaped) text
        host="localhost",
        database="herbario05",
    )

    try:
        engine = sa.create_engine(url_object, echo=True, pool_pre_ping=True)
        session = sa.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        if engine.connect():
            return engine, session()
    except Exception as e:
        logging.error(e)


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
