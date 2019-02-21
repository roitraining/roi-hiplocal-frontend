class Base():
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hiplocal"
    PROJECT = "roi-hiplocal"

class DevelopmentConfig(Base):
    DEBUG = True
    DEVELOPMENT = True
    BUCKET = "roi-hiplocal"
    PROJECT = "roi-hiplocal"
    API = "http://localhost:8085"

class AppEngineConfig(Base):
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hiplocal"
    PROJECT = "roi-hiplocal"
    API = "https://backend-dot-roi-hiplocal.appspot.com/"

class KubernetesConfig(Base):
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hiplocal"
    PROJECT = "roi-hiplocal"
    API = "http://hip-local-api-svc:8085"
