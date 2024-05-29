import os
import pandas as pd
import sqlalchemy as sa

from database import connect, close
from models import Dataset, get_base


def main():
    engine, session = connect()
    base = get_base()
    if not sa.inspect(engine).has_table(Dataset.__tablename__):
        base.metadata.tables[Dataset.__tablename__].create(bind=engine)

    if session.query(Dataset).count() == 0:
        raise ValueError('table %s is empty' % Dataset.__tablename__)

    datasets = ['br_dataset' , 'pr_dataset']#, 'regions_dataset']
    regions = ['North', 'Northeast', 'Middlewest', 'South', 'Southeast']
    minimums = ['5', '10', '20']
    for dataset in datasets:
        for minimum in minimums:
            clause = sa.and_(Dataset.name.__eq__(dataset),
                             Dataset.minimum.__eq__(minimum),
                             Dataset.version.__eq__(1))

            columns = sa.func.array_agg(Dataset.seq)
            query = session.query(columns) \
                .filter(clause) \
                .group_by(Dataset.genus_trusted, Dataset.specific_epithet_trusted) \
                .having(sa.func.count() >= minimum) \
                .all()


    close(engine, session)

if __name__ == '__main__':
    main()
