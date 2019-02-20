class Base():
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hip-local"
    PROJECT = "roi-hip-local"

class DevelopmentConfig(Base):
    DEBUG = True
    DEVELOPMENT = True
    BUCKET = "roi-hip-local"
    PROJECT = "roi-hip-local"
    API = "http://localhost:8085"

class AppEngineConfig(Base):
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hip-local"
    PROJECT = "roi-hip-local"
    API = "https://backend-dot-roi-hip-local.appspot.com/"

class KubernetesConfig(Base):
    DEBUG = False
    TESTING = False
    BUCKET = "roi-hip-local"
    PROJECT = "roi-hip-local"
    API = "http://hip-local-api-svc:8085"
