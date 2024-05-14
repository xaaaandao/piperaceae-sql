import inspect
import logging
import sys

import sqlalchemy
import sqlalchemy as sa

# from models import Level, Local, Identifier, County


def connect():
    url_object = sa.URL.create(
        "postgresql+psycopg2",
        username="xandao",
        password="madu",  # plain (unescaped) text
        host="localhost",
        database="herbario_new",
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
    base.metadata.create_all(engine)
    # # cls[0] -> name, cls[1] -> obj
    # classes = [cls for cls in inspect.getmembers(sys.modules['models'], inspect.isclass) if
    #            'base' not in cls[0].lower()]
    #
    # insp = sqlalchemy.inspect(engine)
    # tables = insp.get_table_names()
    # tables_name = [c[1].__table__.name for c in classes]
    # # print(sorted(tables_name, key=lambda x: ('association' in x.lower(), x)))
    # #
    # for t in sorted(tables_name, key=lambda x: ('_' in x.lower(), x)):
    #     if t not in tables:
    #         base.metadata.tables[t].create(bind=engine)
    #         logging.info('Created table %s' % t)

    # if datasp_level_association.name not in tables:
    #     base.metadata.tables[datasp_level_association.name].create(bind=engine)

    # for c in [Level, DataSP, Local, Identifier, County, DataSPLevel]:
    #     if c.__table__.name not in tables:
    #         table_name = c.__table__.name
    #         base.metadata.tables[table_name].create(bind=engine)
    #         logging.info('Created table %s' % table_name)
