import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))
DEFAULT_PASSWD = os.path.abspath(os.path.join(BASEDIR,"../users.yml"))


class Config:

    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "notasecret")
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    APP_TITLE = os.environ.get("FLASK_APP_TITLE", "Weddingwebsite")

    PASSWD = os.environ.get("FLASK_PASSWD", DEFAULT_PASSWD)
    if not os.path.isfile(PASSWD):
        open(PASSWD, 'a').close()
        os.chmod(PASSWD, 440)

    RSVP_PATH = os.path.join(os.environ.get("FLASK_RSVP", "rsvp"))
    if not os.path.isdir(RSVP_PATH):
        os.mkdir(RSVP_PATH)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
