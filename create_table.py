import os
import sqlalchemy as sa

import database as db

from models import *


def show_tables(engine):
    return sa.inspect(engine).get_table_names()


def table_exists(engine, table_name):
    return True if table_name in show_tables(engine) else False


def create_tables(engine):
    tables = [DataIdentifiersSelectedGeorge, DataSP, DataIdentifiersSelectedGeorge, County, Image, TrustedIdentifier]
    for t in tables:
        if not table_exists(engine, t.__tablename__):
            base = get_base()
            base.metadata.tables[t.__tablename__].create(bind=engine)
            print('create table: %s' % t.__tablename__)
        else:
            print('table %s already exists' % t.__tablename__)
