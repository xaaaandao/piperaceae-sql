def insert(data, session):
    try:
        session.add(data)
        session.commit()
    except Exception:
        session.flush()


def inserts(datas, session):
    try:
        session.add_all(datas)
        session.commit()
    except Exception:
        session.flush()


def is_query_empty(query):
    return query == 0
