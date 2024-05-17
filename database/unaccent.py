from sqlalchemy.sql.functions import ReturnTypeFromArgs

'''
  Necessary to use unaccent in postgresql
  First execute command in postgresql: CREATE EXTENSION unaccent;
'''


class unaccent(ReturnTypeFromArgs):
    pass
