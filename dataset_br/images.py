import os
import shutil
import tqdm


def get_list_of_images_invalid():
    return {
        'barcode': ['INPA0248526', 'INPA0248523', 'INPA0248528', 'NY01421575_01', 'HUFSJ001689_v00', 'HUFSJ001133_v00', 'HUFSJ002198_v00', 'HUFSJ003255_v00', 'HVASF000487_v01', 'INPA0019084_nd', 'INPA0022379_nd', 'INPA0032742_nd', 'INPA0023115', 'NL-U1484137', 'INPA0012286', 'INPA0146998'],
        'reason': ['horizontal', 'horizontal', 'horizontal', 'horizontal', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'not exsicate', 'label', 'label', 'label', 'letter', 'letter', 'letter', 'incomplete']
    }


#%%
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


def copy_images(color, image_size, list_level_name, list_path_images, minimum_image, path_out):
    path_out = os.path.join(path_out, color.upper(), image_size, str(minimum_image))
    print(path_out)
    if not os.path.exists(path_out):
        os.makedirs(path_out)

    for i, species_and_paths in enumerate(zip(list_level_name, list_path_images), start=1):
        species = species_and_paths[0]
        list_p = species_and_paths[1]
        path_final = os.path.join(path_out, 'f%d' % i)

        if not os.path.exists(path_final):
            os.makedirs(path_final)

        for p in list_p:
            shutil.copy(p, path_final)