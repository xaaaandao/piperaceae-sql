import os
import pandas as pd
import sqlalchemy as sa

from database import connect, close, inserts, insert
from models import Dataset, get_base


def main():
    engine, session = connect()
    base = get_base()
    if not sa.inspect(engine).has_table(Dataset.__tablename__):
        base.metadata.tables[Dataset.__tablename__].create(bind=engine)

    if session.query(Dataset).count() > 0:
        return

    minimums = ['5', '10', '20']
    for dataset in ['br_dataset', 'pr_dataset']:
        for minimum in minimums:
            filename = os.path.join(dataset, minimum, 'info_samples.csv')
            df = pd.read_csv(filename, index_col=False, header=0, sep=';', low_memory=False)
            for _, row in df.iterrows():
                d = create_dataset(minimum, dataset, row, 1)
                insert(d, session)

    regions = ['North', 'Northeast', 'Middlewest', 'South', 'Southeast']
    for region in regions:
        for minimum in minimums:
            filename = os.path.join('regions_dataset', region, minimum, 'info_samples.csv')
            df = pd.read_csv(filename, index_col=False, header=0, sep=';', low_memory=False)

            for _, row in df.iterrows():
                d = create_dataset(minimum, 'regions_dataset', row, 1, region=region)
                insert(d, session)

    close(engine, session)


def dataset_is_br_pr(minimum: int, name: str, row, version: int) -> Dataset:
    return Dataset(seq=row['seq'],
                   genus=row['genus'],
                   specific_epithet=row['specific_epithet'],
                   genus_trusted=row['genus_trusted'],
                   specific_epithet_trusted=row['specific_epithet_trusted'],
                   country=row['country'],
                   country_trusted=row['country_trusted'],
                   county=row['county'],
                   state_province=row['state_province'],
                   name=name,
                   minimum=minimum,
                   version=version)


def create_dataset(minimum: int, name: str, row, version: int, region: str = None) -> Dataset:
    return dataset_is_region(minimum, name, region, row, version) if region else dataset_is_br_pr(minimum, name, row, version)


def dataset_is_region(minimum: int, name: str, region: str, row, version: int) -> Dataset:
    return Dataset(seq=row['seq'],
                   genus=row['genus'],
                   specific_epithet=row['specific_epithet'],
                   genus_trusted=row['genus_trusted'],
                   specific_epithet_trusted=row['specific_epithet_trusted'],
                   country=row['country'],
                   country_trusted=row['country_trusted'],
                   county=row['county'],
                   state_province=row['state_province'],
                   name=name,
                   region=region,
                   minimum=minimum,
                   version=version)


if __name__ == '__main__':
    main()
