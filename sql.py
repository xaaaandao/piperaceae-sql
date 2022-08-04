import re
import sqlalchemy

from dataframe import get_columns_table
from tables import get_base, DataSP
from unaccent import unaccent


def create_table_if_not_exists(cfg, engine, table_name):
    if not sqlalchemy.inspect(engine).has_table(table_name, schema=cfg["database"]):
        get_base().metadata.create_all(engine)


def find_and_update(data, list_seq, list_of_columns_valid, new_column, session, value=None):
    for columns in list_of_columns_valid:
        for data_formatted in (remove_white_spaces(data), remove_hyphen(data)):
            if len(data_formatted) > 0:
                q = session.query(DataSP.seq).filter(sqlalchemy.and_(
                    *[sqlalchemy.func.lower(unaccent(getattr(DataSP, columns))).ilike(f"%{s.lower()}%") for s in
                      data_formatted])).all()
            else:
                q = session.query(DataSP.seq).filter(
                    sqlalchemy.func.lower(unaccent(getattr(DataSP, columns))).ilike(f"%{data_formatted}%")).all()
            if len(q) > 0:
                list_seq.append({"seq": remove_set(q), "column": columns, "new_column": new_column,
                                 "value_searched": value if value else data})


def column_is_string_or_varchar_or_text(column):
    return str(column.type).lower() in ("string", "varchar", "text")


def get_columns_text(table):
    return list([column.key for column in get_columns_table(table) if column_is_string_or_varchar_or_text(column)])


def remove_white_spaces(string):
    return remove_word_started_lowercase(string).split(" ")


def remove_hyphen(string):
    return remove_word_started_lowercase(string).split("-")


def remove_word_started_lowercase(string):
    return re.sub(r"\b[a-z]+\s*", "", string)


def remove_set(data):
    return list([s for s, in data])
