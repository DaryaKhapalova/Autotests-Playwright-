import os

BASE_URL = os.getenv('BASE_URL')
if BASE_URL is None:
    raise ValueError("BASE_URL is not set in the environment variables")

DEFAULT_CUSTOMER_NO = os.getenv('DEFAULT_CUSTOMER_NO')
if DEFAULT_CUSTOMER_NO is None:
    raise ValueError("DEFAULT_CUSTOMER_NO is not set in the environment variables")

DEFAULT_LOGIN = os.getenv('DEFAULT_LOGIN')
if DEFAULT_LOGIN is None:
    raise ValueError("DEFAULT_LOGIN is not set in the environment variables")

DEFAULT_PASSWORD = os.getenv('DEFAULT_PASSWORD')
if DEFAULT_PASSWORD is None:
    raise ValueError("DEFAULT_PASSWORD is not set in the environment variables")

ignore_https_errors=True
