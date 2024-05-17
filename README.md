# piperaceae-sql

## Database
```
$ psql --version
psql (PostgreSQL) 14.11 (Ubuntu 14.11-0ubuntu0.22.04.1)
```

### Configure database
```
$ sudo su - postgres
$ psql
$ CREATE USER TO;
$ CREATE DATABASE database_name OWNER TO user;
$ CREATE EXTENSION unaccent;
```

## Python
```
$ conda --version
conda 24.1.0
$ python --version
Python 3.11.5
```

### Requirements
```
$ pip install requirements.txt
$ pip install psycopg2-binary
```

## CSV
* `genus_species.csv`: contains old genus and new genus equivalent; 
* `george_data.csv`: contains samples selected by george;
* `images_invalid.csv`: contains the barcode with images invalid; 
* `original.csv`: contains all samples founded in speciesLink;
* `trusted_identifiers.csv`: contains the identifiers name selected by george.
