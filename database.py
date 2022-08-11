import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm
import sqlalchemy.schema

def connect(cfg):
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
        print(f"problems with host {cfg['host']} ({e})")


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



