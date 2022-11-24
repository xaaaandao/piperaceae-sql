import os
import sys
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from images import copy_all_images, separate_images_per_threshold

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import *
from file import *
from tables import *


def main():
    session: Session
    engine, session = connect()

    path_fotos = '/home/xandao/Documentos/dataset-52k-sp-2021/fotos'
    list_images = list([file for file in pathlib.Path(path_fotos).rglob('*') if file.is_file()])
    result = session.query(DataSP.identified_by).filter(DataSP.george).distinct().all()

    print(len(list_images), len(result))

    list_idenified = list_ilike(DataSP.identified_by, ['%{}%'.format(r[0]) for r in result])

    list_regioes = [
        {'norte': list_ilike(DataSP.state_province, get_list_state_of_norte())},
        {'nordeste': list_ilike(DataSP.state_province, get_list_state_of_nordeste())},
        {'centro_oeste': list_ilike(DataSP.state_province, get_list_state_of_centro_oeste())},
        {'sudeste': list_ilike(DataSP.state_province, get_list_of_sudeste())},
        {'sul': list_ilike(DataSP.state_province, get_list_of_sul())},
    ]

    query = session.query(DataSP.specific_epithet, DataSP.barcode).filter(DataSP.genus is not None,
                                                                          DataSP.specific_epithet is not None,
                                                                          and_(or_(*list_identified),
                                                                               or_(*list_regioes))).all()

    copy_all_images(list_images, query)
    separate_images_per_threshold()


def get_list_of_sul():
    return ['Paran_', 'Santa Catarina', 'Rio Grande do Sul']


def get_list_of_sudeste():
    return ['Esp_rito Santo', 'Minas Gerais', 'Rio de Janeiro', 'S_o Paulo']


def get_list_state_of_centro_oeste():
    return ['Goi_s', 'Mato Grosso', 'Mato Grosso do Sul']


def get_list_state_of_nordeste():
    return ['Alagoas', 'Bahia', 'Cear_', 'Maranh_o', 'Para_ba', 'Pernambuco', 'Piau_', 'Rio Grande do Norte', 'Sergipe']


def get_list_state_of_norte():
    return ['Acre', 'Amap_', 'Amazonas', 'Par_', 'Rond_nia', 'Roraima', 'Tocantins']


def list_ilike(attribute, list_of_values):
    return [attribute.ilike('%{}%'.format(value)) for value in list_of_values]


if __name__ == '__main__':
    main()
