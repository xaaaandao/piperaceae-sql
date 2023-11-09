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

8- update_genus_species.py

update_path_to_images.py

* to run sp_scrapy.py
  * pip install scrapy
  * python sp_scrapy.py
  * o scrapy preenche as colunas list_src e list_title da tabela data selected george

- falta:
  - update country_state
  - 