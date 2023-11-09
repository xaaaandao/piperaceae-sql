import os
import pathlib

import database as db

from models import Image, DataIdentifierSelectedGeorge


def add_seq_each_image(session):
    query = session.query(DataIdentifierSelectedGeorge) \
        .filter(DataIdentifierSelectedGeorge.list_title.is_not(None)) \
        .all()

    for i, q in enumerate(query):
        print('%d/%d' % (i, len(query)))
        try:
            session.query(Image) \
                .filter(Image.filename.in_(q.list_title)) \
                .update(values={'seq_id': q.seq}, synchronize_session=False)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


def main():
    engine, session = db.connect()

    list_color_image = ['RGB', 'grayscale']
    list_image_size = ['256', '400', '512']
    path_base = '/media/none/c2f58d30-ff2c-47f7-95af-91ad6fd69760/dataset/dataset-segmented-sp'

    for color in list_color_image:
        for image_size in list_image_size:
            path_fotos = os.path.join(path_base, color, image_size, 'jpeg')
            path_fotos_segmented = os.path.join(path_base, color, image_size, 'w_pred_mask')
            list_images = [img for img in pathlib.Path(path_fotos).rglob('*.jpeg') if img.is_file()]
            list_images_segmented = [img for img in pathlib.Path(path_fotos_segmented).rglob('*.jpeg') if img.is_file()]
            insert_image(color, image_size, list_images, list_images_segmented, session)

            # each image add a seq
            add_seq_each_image(session)

    session.close()
    engine.dispose()


def insert_image(color, image_size, list_images, list_images_segmented, session):
    for i, image in enumerate(zip(list_images, list_images_segmented)):
        image_original = image[0]
        image_segmented = image[1]
        print('color: %s image_size: %s (%d/%d)' % (color, image_size, i, len(list_images)))
        image = Image(path=str(image_original), path_segmented=str(image_segmented), filename=str(image_original.stem),
                      height=int(image_size), width=int(image_size), color_mode=color.upper())
        try:
            session.add(image)
            session.commit()
        except Exception as e:
            print(e)
            session.flush()


if __name__ == '__main__':
    main()
