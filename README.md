# piperaceae-sql

``
$ pip install -r requirements.txt
``

1- in postgresql: 

``
    CREATE DATABASE db_name OWNER user;
    CREATE EXTENSION unaccent;
``

data_sp (contains 50k+)

2- create_table.py

3- insert_county.py

4- insert_metadata.py (metadata specieslink)

6- trusted_identifiers.py
- this file insert data of identifiers selected by George

7- update_country_state_county.py


update_path_to_images.py

- falta:
  - gerar uma lista com os identificadores confiáveis
  - insere os data selected by george
  - update country_state
  - update_genus...
  - 