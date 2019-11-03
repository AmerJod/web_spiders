import os


class Config(object):
    # shard configurations will be here
    pass


class ProductionConfig(Config):

    REDIS_CONN = {"host": "redis", "port": 6379}

    POSTGRES_CONN = {
        "POSTGRES_URL": "0.0.0.0:54320",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PW": "pwd123456",
        "POSTGRES_DB": "db_postgres",
    }


class DevelopmentConfig(Config):

    REDIS_CONN = {"host": "redis", "port": 6379}

    POSTGRES_CONN = {
        "POSTGRES_URL": "0.0.0.0:54320",
        "POSTGRES_USER": "postgres",
        "POSTGRES_PW": "pwd123456",
        "POSTGRES_DB": "db_postgres",
    }


def get_config(testing=False):
    spiders_evn = os.getenv("SPIDERS_EVN", "false")

    if not spiders_evn:
        print("No value set for SPIDERS_EVN, Development config loaded")
        return ProductionConfig()
    elif spiders_evn == "production":
        print("Production config loaded")
        return ProductionConfig()
    elif spiders_evn == "development":
        print("Development config loaded")
        return DevelopmentConfig()
    else:
        print("No value match for SPIDERS_EVN, Production config loaded")
        return ProductionConfig()
