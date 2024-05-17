def insert_images_invalid(session, filename="./csv/images_invalid.csv"):
    count = session.query(ImagesInvalid).count()
    if not is_query_empty(count):
        logging.info('count of images_invalid is %d' % count)
        return

    df = pd.read_csv(filename, sep=';', low_memory=False, skipinitialspace=True, header=0, index_col=False,
                     encoding='utf-8')

    for idx, row in df.iterrows():
        insert(ImagesInvalid(row['barcode'], row['reason']))
      
