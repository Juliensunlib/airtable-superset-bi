import os

# Configuration de base
SECRET_KEY = os.environ.get('SUPERSET_SECRET_KEY', 'votre_clé_secrète_ici')
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql+psycopg2://superset:superset@postgres:5432/superset')
REDIS_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')

# Désactiver les exemples par défaut
SUPERSET_WEBSERVER_TIMEOUT = 300
SUPERSET_DASHBOARD_POSITION_DATA_LIMIT = 10000
SQLLAB_TIMEOUT = 300
FEATURE_FLAGS = {
    'DASHBOARD_NATIVE_FILTERS': True,
    'DASHBOARD_CROSS_FILTERS': True,
    'ENABLE_TEMPLATE_PROCESSING': True,
}
