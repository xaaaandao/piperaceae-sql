import os
import sqlalchemy as sa

import database as db

from models import *


def show_tables(engine):
    return sa.inspect(engine).get_table_names()


def table_exists(engine, table_name):
    return True if table_name in show_tables(engine) else False


def main():
    engine, session = db.connect()

    list_tables = [DataIdentifiersSelectedGeorge, DataSP, DataIdentifiersSelectedGeorge, County, Image, TrustedIdentifier]
    for t in list_tables:
        if not table_exists(engine, t.__tablename__):
            base = get_base()
            base.metadata.tables[t.__tablename__].create(bind=engine)
            print('create table: %s' % t.__tablename__)
        else:
            print('table %s already exists' % t.__tablename__)

    session.close()
    engine.dispose()


if __name__ == '__main__':
    main()