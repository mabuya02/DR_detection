import os, random, string

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))
    ASSETS_ROOT = os.getenv('ASSETS_ROOT', '/static/assets')
    MEDIA_FOLDER = os.getenv('MEDIA_FOLDER', 'apps/static/assets/images/media/retinal_images')
    GRAD_CAM_FOLDER = os.getenv('GRAD_CAM_FOLDER', 'apps/static/assets/images/media/grad_cam')
 
    SECRET_KEY  = os.getenv('SECRET_KEY', None)
    if not SECRET_KEY:
        SECRET_KEY = ''.join(random.choice( string.ascii_lowercase  ) for i in range( 32 ))

    SOCIAL_AUTH_GITHUB  = False

    GITHUB_ID      = os.getenv('GITHUB_ID'    , None)
    GITHUB_SECRET  = os.getenv('GITHUB_SECRET', None)
       
    if GITHUB_ID and GITHUB_SECRET:
         SOCIAL_AUTH_GITHUB  = True        

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DB_ENGINE   = os.getenv('DB_ENGINE'   , None)
    DB_USERNAME = os.getenv('DB_USERNAME' , None)
    DB_PASS     = os.getenv('DB_PASS'     , None)
    DB_HOST     = os.getenv('DB_HOST'     , None)
    DB_PORT     = os.getenv('DB_PORT'     , None)
    DB_NAME     = os.getenv('DB_NAME'     , None)

    USE_SQLITE  = True 
    if DB_ENGINE and DB_NAME and DB_USERNAME:
        try:
            if DB_ENGINE == 'postgresql':
                SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(
                    DB_USERNAME,
                    DB_PASS,
                    DB_HOST,
                    DB_PORT,
                    DB_NAME
                )
                USE_SQLITE = False
            elif DB_ENGINE == 'mysql':
                SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}:{}/{}'.format(
                    DB_USERNAME,
                    DB_PASS,
                    DB_HOST,
                    DB_PORT,
                    DB_NAME
                )
                USE_SQLITE = False

        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))
            print('> Fallback to SQLite')

    if USE_SQLITE:
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
        
   


class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600

class DebugConfig(Config):
    DEBUG = True

config_dict = {
    'Production': ProductionConfig,
    'Debug'     : DebugConfig
}
