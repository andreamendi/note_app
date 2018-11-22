class DevelopmentConfig(object):
    SECRET_KEY = 'secret12345'
    DEBUG = True
    #MySQL conecttion
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '@'
    MYSQL_DB = 'note_app'
    MYSQL_CURSORCLASS = 'DictCursor'