import itertools
import os
import pandas as pd
import shutil

from IPython.display import display
from models import DataTrustedIdentifier


def get_list_of_images_invalid():
    return {
        'barcode': ['INPA0248526', 'INPA0248523', 'INPA0248528', 'NY01421926_01', 'NY01421575_01', 'HUFSJ001689_v00', 'HUFSJ001133_v00', 'HUFSJ002198_v00', 'HUFSJ003255_v00', 'HVASF000487_v01',  'HUFSJ001689_v01', 'INPA0019084_nd', 'INPA0022379_nd', 'INPA0032742_nd', 'INPA0023115', 'NL-U1484137', 'NY01397568_01', 'INPA0012286', 'INPA0146998'],
        'reason': ['horizontal', 'horizontal', 'horizontal', 'horizontal', 'horizontal', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'label', 'label', 'label', 'letter', 'letter', 'letter', 'letter', 'incomplete']
    }


def save_metadata(list_count_samples, list_f, list_level, list_path_images_final, list_seq_final, out, session):
    df = pd.DataFrame({
        'levels': list_level,
        'paths': list_path_images_final,
        'count': list_count_samples,
        'seq': list_seq_final,
        'dst': list_f,
    })
    print('total of levels: %d total of images: %d' % (len(list_level), df['count'].sum()))
    display(df.head(4))
    filename=os.path.join(out, 'info_dataset.csv')
    df.to_csv(filename, sep=';', index=None, lineterminator='\n', doublequote=True)

    list_seq = list(itertools.chain(*list_seq_final))
    query = session.query(DataTrustedIdentifier)\
                    .filter(DataTrustedIdentifier.seq.in_(list_seq))\
                    .all()
    data = [(q.seq, q.genus, q.specific_epithet, q.genus_trusted, q.specific_epithet_trusted, q.list_src) for q in query]
    columns = ['seq', 'genus', 'specific_epithet', 'genus_trusted', 'specific_epithet_trusted', 'urls']
    df = pd.DataFrame(data, columns=columns)
    display(df.head(4))
    filename=os.path.join(out, 'info_samples.csv')
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
            shutil.copy(image, out_level)
    return list_f