import os
import pathlib
import shutil


def copy_all_images(dst, list_images, query):
    path = os.path.join(dst, 'todos')
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    l = dict()
    for q in query:
        species = q[0]
        barcode = q[1]
        result = sorted([f for f in list_images if barcode in str(f.stem)])
        if len(result) > 0:
            if not species in l.keys():
                l[species] = []

            # if not os.path.exists(os.path.join(path, barcode[0])):
            #     pathlib.Path(os.path.join(path, barcode[0])).mkdir(parents=True, exist_ok=True)
            #
            result = [result[0]]
            for r in result:
                l[species].append(r.name)
            # break
    return l
    print(l)


def separate_images_per_threshold(dst):
    path = os.path.join(dst, 'todos')
    list_dir = [path for path in pathlib.Path(path).glob('*') if path.is_dir()]

    for threshold in ['5', '10', '20']:
        pathlib.Path(os.path.join(dst, threshold)).mkdir(exist_ok=True, parents=True)

    for d in list_dir:
        if len(os.listdir(d)) >= 5:
            shutil.copytree(d, os.path.join(dst, '5', d.name))
        if len(os.listdir(d)) >= 10:
            shutil.copytree(d, os.path.join(dst, '10', d.name))
        if len(os.listdir(d)) >= 20:
            shutil.copytree(d, os.path.join(dst, '20', d.name))

    for threshold in ['5', '10', '20']:
        list_info = []
        for i, path in enumerate(pathlib.Path(dst, threshold).glob('*'), 1):
            list_info.append('\"%s\";\"f%d\";\"%d\"\n' % (path.name, i, len(os.listdir(path))))
            dst_img = str(path.resolve()).replace(str(path.name), 'f%s' % str(i))
            os.rename(path, dst_img)

        file = open('%s/%s/label2.txt' % (dst, threshold), mode='w')
        for info in list_info:
            file.write(info)
        file.close()
