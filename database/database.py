import logging

import sqlalchemy as sa


def connect(echo=True):
    url_object = sa.URL.create(
        'postgresql+psycopg2',
        username='xandao',
        password='madu',  # plain (unescaped) text
        host='localhost',
        database='datasetv02',
        query={'client_encoding': 'utf8'}
    )

    try:
        engine = sa.create_engine(url_object, echo=echo, pool_pre_ping=True)
        session = sa.orm.sessionmaker(bind=engine)
        session.configure(bind=engine)
        if engine.connect():
            return engine, session()
    except Exception as e:
        logging.error(e)


def create_table(base, engine):
    base.metadata.create_all(engine)
