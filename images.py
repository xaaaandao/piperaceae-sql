import database as db
import os
import pandas as pd
import shutil

from IPython.display import display


def get_list_of_images_invalid():
    return {
        'barcode': ['INPA0248526', 'INPA0248523', 'INPA0248528', 'NY01421575_01', 'HUFSJ001689_v00', 'HUFSJ001133_v00',
                    'HUFSJ002198_v00', 'HUFSJ003255_v00', 'HVASF000487_v01', 'INPA0019084_nd', 'INPA0022379_nd',
                    'INPA0032742_nd', 'INPA0023115', 'NL-U1484137', 'INPA0012286', 'INPA0146998'],
        'reason': ['horizontal', 'horizontal', 'horizontal', 'horizontal', 'not exsicate', 'not exsicate',
                   'not exsicate', 'not exsicate', 'not exsicate', 'label', 'label', 'label', 'letter', 'letter',
                   'letter', 'incomplete']
    }


# %%
def remove_images_invalid(list_level_name, list_images_invalid, list_path_images):
    list_path_correct = []
    list_count_path = []
    for i, p in enumerate(list_path_images):
        matching = [path for path in p if not any(barcode in path for barcode in list_images_invalid['barcode'])]

        if len(p) != len(matching):
            print('specie: %s before: %d after: %d' % (list_level_name[i], len(p), len(matching)))
            diff = list(set(p) ^ set(matching))
            print('diff: %s' % str(diff))

        list_path_correct.append(matching)
        list_count_path.append(len(matching))

    return list_count_path, list_path_images


def copy_images(list_level_name, list_path_images, path_out):
    list_path_dst = []

    for i, species_and_paths in enumerate(zip(list_level_name, list_path_images), start=1):
        species = species_and_paths[0]
        list_p = species_and_paths[1]
        path_final = os.path.join(path_out, 'f%d' % i)

        if not os.path.exists(path_final):
            os.makedirs(path_final)

        for p in list_p:
            shutil.copy(p, path_final)

        list_path_dst.append(path_final)

    return list_path_dst


def save_metadata(color, image_size, list_level_name, list_path_images, list_count_path, list_path_dst, minimum_image,
                  path_out, session):
    df = pd.DataFrame({
        'species': list_level_name,
        'paths': list_path_images,
        'count': list_count_path,
        'dst': list_path_dst
    })
    display('color: %s image_size: %s minimum_image: %d' % (color, image_size, minimum_image))
    display('len(list_level_name): %d len(paths_images): %d' % (len(list_level_name), df['count'].sum()))
    filename_csv = os.path.join(path_out, 'dataset_informations.csv')
    display('save csv in %s' % filename_csv)
    df.to_csv(filename_csv, sep=';', na_rep=None, encoding='utf-8', lineterminator='\n', index=None)
    display(df.head(3))
    display('total of images %d' % df['count'].sum())

    df = db.get_informations_images(list_path_images, session)
    filename_csv = os.path.join(path_out, 'image_informations.csv')
    df.to_csv(filename_csv, sep=';', na_rep=None, encoding='utf-8', lineterminator='\n', index=None)
    display('image informations')
    display('save csv in %s' % filename_csv)
    display(df.head(3))


def separate_and_copy_images(condition, level, list_color, list_images_invalid, list_minimum_image, list_image_size,
                             path_out, session):
    for color in list_color:
        for image_size in list_image_size:
            for minimum_image in list_minimum_image:
                records = db.get_records_group_by_level(condition, level, minimum_image, session)
                list_level_name, list_path_images = db.filter_records(color, image_size, minimum_image, records, session)

                if len(list_path_images) > 0:
                    list_count_path, list_path_images = remove_images_invalid(list_level_name, list_images_invalid,
                                                                              list_path_images)

                    path_out = os.path.join(path_out, color.upper(), image_size, str(minimum_image))

                    if not os.path.exists(path_out):
                        os.makedirs(path_out)

                    list_path_dst = copy_images(list_level_name, list_path_images, path_out)

                    save_metadata(color, image_size, list_level_name, list_path_images, list_count_path, list_path_dst,
                                  minimum_image, path_out, session)


def get_url_image(barcode, herbarium, height=5000, width=5000):
    return 'https://specieslink.net/search/util/osd-dezoomify?imagecode=%s&path=herbaria/%s/%s&width=%s&height=%s' % (
    barcode, herbarium, barcode, str(width), str(height))
