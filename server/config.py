DEBUG = False
TESTING = False
TEMPLATES_AUTO_RELOAD = DEBUG

LISTEN_HOST = "127.0.0.1"
LISTEN_PORT = "5000"

SECRET_KEY = "38rufm3q8uft38gjqh-g31g3j0"
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://dashie@localhost/pyairwaves"
# SQLALCHEMY_DATABASE_URI = 'sqlite:///ahrl.db'
# SQLALCHEMY_DATABASE_URI = 'mysql://dashie:saucisse@localhost/ahrl'
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_RECORD_QUERIES = True

SECURITY_CONFIRMABLE = False
SECURITY_REGISTERABLE = False  # deactivate registration
SECURITY_RECOVERABLE = True
SECURITY_TRACKABLE = False
SECURITY_CHANGEABLE = True
SECURITY_PASSWORD_HASH = "bcrypt"
SECURITY_PASSWORD_SALT = "omgponies"
# SECURITY_URL_PREFIX = '/sec'

SECURITY_SEND_REGISTER_EMAIL = False
SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
SECURITY_SEND_PASSWORD_RESET_NOTICE_EMAIL = False

BOOTSTRAP_USE_MINIFIED = True
BOOTSTRAP_SERVE_LOCAL = True
BOOTSTRAP_CDN_FORCE_SSL = True
BOOTSTRAP_QUERYSTRING_REVVING = True

DEBUG_TB_PROFILER_ENABLED = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

BABEL_DEFAULT_LOCALE = "en"
BABEL_DEFAULT_TIMEZONE = "UTC"

# Sentry
SENTRY_USER_ATTRS = ["name", "email"]
SENTRY_DSN = ""

# Redis configuration for socket.io
SOCKETIO_MESSAGE_QUEUE = "redis://127.0.0.1:6379/3"
SOCKETIO_CORS_ALLOWED_ORIGINS = "*"
# SOCKETIO_CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5000"]

# URL to FAA Archive
FAA_ARCHIVE_URL = "https://registry.faa.gov/database/ReleasableAircraft.zip"
FAA_DL_TEMP_PATH = "/tmp/faaingest/"

UPDATE_DB_TEMP_PATH = "/tmp/updatedb_pyairwaves/"

# Hostname on where this server is running
PYAW_HOSTNAME = "potato"

# Sources for ADS-B and AIS, PLEASE NOTE that currently only one source is handled for each !
# Port for ADSB (dump1090) needs to be 30003 (SBS BaseStation)
# Port for AIS (rtl-ais) needs to be 10110
ADSB_SOURCE = {"host": "192.168.10.122", "port": 30003, "name": "patate", "reconnect_delay": 5, "thread_timeout": 30}
# AIS_SOURCE = {"host": "patate", "port": 10110, "name": "patate", "reconnect_delay": 5, "thread_timeout": 30}
AIS_SOURCE = {
    "host": "ais.adrasec76.org",
    "port": 10120,
    "name": "adrasec76",
    "reconnect_delay": 5,
    "thread_timeout": 30,
}
# AIS_SOURCE = {"host": "patate", "port": 10110, "name": "adrasec76", "reconnect_delay": 5, "thread_timeout": 30}
