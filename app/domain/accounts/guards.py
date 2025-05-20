from fastapi.security.oauth2 import OAuth2PasswordBearer

from ..consts import URL_ACCOUNT_TOKEN


def required_superuser(): ...


oauth2_schema = OAuth2PasswordBearer(
    tokenUrl=URL_ACCOUNT_TOKEN,
)
