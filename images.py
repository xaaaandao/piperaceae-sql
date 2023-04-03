import itertools
import numpy as np
import os
import pandas as pd
import sqlalchemy as sa
import shutil

from IPython.display import display
from models import DataTrustedIdentifier, Image


def get_list_of_images_invalid():
    return {
        'barcode': ['NY01421545_01', 'INPA0248526', 'INPA0248523', 'INPA0248528', 'NY01421926_01', 'NY01421575_01', 'HUFSJ001689_v00', 'HUFSJ001133_v00', 'HUFSJ002198_v00', 'HUFSJ003255_v00', 'HVASF000487_v01',  'HUFSJ001689_v01', 'INPA0019084_nd', 'INPA0022379_nd', 'INPA0032742_nd', 'INPA0023115', 'NL-U1484137', 'NY01397568_01', 'INPA0012286', 'INPA0146998'],
        'reason': ['horizontal', 'horizontal', 'horizontal', 'horizontal', 'horizontal', 'horizontal', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'label', 'label', 'label', 'letter', 'letter', 'letter', 'letter', 'incomplete']
    }


def select_images(color, image_size, list_count_samples, list_level, list_images_invalid, list_path_images_final, list_seq_final, minimum_image, session, query):
    for q in query:
        qzao = session.query(Image.seq_id, sa.func.array_agg(Image.path_segmented).label('list_path_segmented')) \
            .filter(sa.and_(Image.seq_id.in_(q.list_seq),
                            Image.color_mode.__eq__(color.upper()),
                            Image.height.__eq__(image_size),
                            Image.width.__eq__(image_size),
                            sa.not_(Image.filename.in_(list_images_invalid)),
                            sa.not_(Image.filename.ilike('%_v0%')),
                            sa.not_(Image.filename.like('%_e%')),
                            sa.not_(Image.filename.like('%_nd%')),
                            )) \
            .group_by(Image.seq_id) \
            .all()

        list_one_image_per_seq = []
        list_seq_one_image = []
        for qzinho in qzao:
            list_seq_one_image.append(qzinho.seq_id)
            list_one_image_per_seq.append(sorted(qzinho.list_path_segmented)[0])

        if len(list_one_image_per_seq) >= minimum_image:
            list_count_samples.append(len(list_one_image_per_seq))
            list_level.append(q.specific_epithet_trusted)
            list_path_images_final.append(list_one_image_per_seq)
            list_seq_final.append(list_seq_one_image)


def save_info_dataset(color, image_size, level, list_count_samples, list_level, minimum_image, region, out):
    total=np.sum([c for c in list_count_samples])
    index=['dst', 'color', 'image_size', 'minimum_image', 'level_name', 'levels', 'total', 'average']
    data=[out, color, image_size, minimum_image, level.name, len(list_level), total, round(total/len(list_level), 2)]

    if region:
        index.insert(5, 'region')
        data.insert(5, region)

    df = pd.DataFrame(data, index=index)
    display(df)
    filename = os.path.join(out, 'info_dataset.csv')
    df.to_csv(filename, sep=';', index=index, header=None, lineterminator='\n', doublequote=True)


def save_metadata(color, image_size, level, list_count_samples, list_f, list_level, list_path_images_final, list_seq_final, minimum_image, out, session, region=None):
    save_info_per_level(list_count_samples, list_f, list_level, list_path_images_final, list_seq_final, region, out)
    save_info_per_sample(list_seq_final, region, out, session)
    save_info_dataset(color, image_size, level, list_count_samples, list_level, minimum_image, region, out)


def save_info_per_sample(list_seq_final, region, out, session):
    list_seq = list(itertools.chain(*list_seq_final))
    query = session.query(DataTrustedIdentifier) \
        .filter(DataTrustedIdentifier.seq.in_(list_seq)) \
        .all()
    data = [(q.seq, q.genus, q.specific_epithet, q.genus_trusted, q.specific_epithet_trusted, q.country_trusted, q.country, q.county, q.state_province, q.list_src) for q in
            query]
    columns = ['seq', 'genus', 'specific_epithet', 'genus_trusted', 'specific_epithet_trusted', 'country_trusted', 'country' ,'county', 'state_province', 'urls']
    df = pd.DataFrame(data, columns=columns)
    display(df.head(3))
    filename = os.path.join(out, 'info_samples.csv')
    df.to_csv(filename, sep=';', index=None, lineterminator='\n', doublequote=True)


def save_info_per_level(list_count_samples, list_f, list_level, list_path_images_final, list_seq_final, region, out):
    df = pd.DataFrame({
        'levels': list_level,
        'count': list_count_samples,
        'dst': list_f,
        'paths': list_path_images_final,
        'seq': list_seq_final,
    })
    print('total of levels: %d total of images: %d' % (len(list_level), df['count'].sum()))
    display(df.head(3))
    filename = os.path.join(out, 'info_levels.csv')
    df.to_csv(filename, sep=';', index=None, lineterminator='\n', doublequote=True)


def copy_images(list_level, list_path_images_final, out):
    list_f=[]
    if not os.path.exists(out):
        os.makedirs(out)

    for i, ff in enumerate(zip(list_level, list_path_images_final), start=1):
        level = ff[0]
        list_images = ff[1]

        out_level = os.path.join(out, 'f%d' % i)
        list_f.append(out_level)
        if not os.path.exists(out_level):
            os.makedirs(out_level)

        for i, image in enumerate(list_images, start=1):
            shutil.copy(image.replace('w_pred_mask', 'jpeg'), out_level)
    return list_f