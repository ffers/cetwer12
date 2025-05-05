import os

ENV = os.getenv("ENV", "dev")  # дефолтне значення
IS_DEV = ENV == "dev"
IS_PROD = ENV == "prod"
IS_TEST = ENV == "test"
