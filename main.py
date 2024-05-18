import datetime
import logging

from database.database import connect, create_table
from dataset.datasets import load_datasetv1, load_datasetv2
from george import insert_data_george
from identifier import insert_trusted_identifier
from database.models import get_base
from local.county import insert_counties, update_county_old_to_county
from local.local import update_local
from local.state import update_state_old_to_state
from species_link import insert_data_specieslink
from level import update_level, update_level_valid, update_level_old_to_level

datefmt = '%d-%m-%Y+%H-%M-%S'
dateandtime = datetime.datetime.now().strftime(datefmt)
bold_red = "\x1b[31;1m"
green = "\x1b[32m"
reset = "\x1b[0m"
format = '%(asctime)s [%(module)s - L:%(lineno)d - %(levelname)s] %(message)s'
format_info = green + format + reset
format_error = bold_red + format + reset
logging.basicConfig(format=format_info, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.INFO)
logging.basicConfig(format=format_error, datefmt='[%d/%m/%Y %H:%M:%S]', level=logging.ERROR)


def main():
    engine, session = connect(echo=False)
    base = get_base()

    create_table(base, engine)
    insert_counties(session)
    insert_data_specieslink(session)
    insert_data_george(session)
    insert_trusted_identifier(session)
    # insert_images_invalid(session)
    update_level(session)
    update_level_valid(session)
    update_local(session)
    update_level_old_to_level(session)  # ok
    update_county_old_to_county(session)
    update_state_old_to_state(session)

    load_datasetv1(session)
    load_datasetv2(session)

    engine.dispose()
    session.close()


if __name__ == '__main__':
    main()
