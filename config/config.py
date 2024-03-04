import os


class Config:

    db_url = None
    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Stores Rest API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_DATABASE_URI = db_url or os.getenv(
        "DATABASE_URL", "sqlite:///data.db"
    )  # this is for dev

    def __init__(self, db_url=None):
        self.db_url = db_url
