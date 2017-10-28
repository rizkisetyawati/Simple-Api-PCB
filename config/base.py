class Configuration:
    # konfigurasi keamanan
    SECURITY_REGISTERABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_TRACKABLE = True
    CSRF_ENABLED = True
    SECRET_KEY = 'ProudOfYourCode'
    CSRF_SESSION_KEY = 'YourCode'

    # konfigurasi database : http://flask-sqlalchemy.pocoo.org/2.3/config/#configuration-keys
    SQLALCHEMY_DATABASE_URI = 'mysql://root:sriwijaya2@localhost/zz'

    DEBUG = True  # debug false untuk produksi dan debug=true untuk pengembangan
