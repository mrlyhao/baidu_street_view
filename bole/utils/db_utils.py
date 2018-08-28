"""
数据库相关操作和配置
"""
from pymongo import MongoClient
from mongoengine import connect


class DBConfig(object):

    def __init__(self):
        self.test_server_host = "39.104.57.134"
        self.prod_server_host = "39.104.103.57"
        self.D_MONGO_CONFIG = {
            "test": {
                "xc_ogn_test": {
                    "host": self.test_server_host,
                    "port": 8200,
                    "username": "sj_test",
                    "password": "test4321"
                },
                "xc_cln_test": {
                    "host": self.test_server_host,
                    "port": 8201,
                    "username": "sj_test",
                    "password": "test4321"
                },
                "xc_base_test": {
                    "host": self.test_server_host,
                    "port": 8204,
                    "username": "sj_test",
                    "password": "test4321"
                },
                "xc_test": {
                    "host": self.test_server_host,
                    "port": 8203,
                    "username": "hd_test",
                    "password": "Veily2018"
                }
            },
            "prod": {
                "xc_ogn": {
                    "host": self.prod_server_host,
                    "port": 8205,
                    "username": "sj_prod",
                    "password": "prod4321"
                },
                "xc_cln": {
                    "host": self.prod_server_host,
                    "port": 8205,
                    "username": "sj_lyh",
                    "password": "lyh7645"
                },
                "xc_base": {
                    "host": self.prod_server_host,
                    "port": 8205,
                    "username": "sj_prod",
                    "password": "prod4321"
                },
                "xc_prod": {
                    "host": self.prod_server_host,
                    "port": 8204,
                    "username": "hd_prod",
                    "password": "Veily2018"
                }
            }
        }

    def mongo_connect(self, connect_type="auth", env="test", name="xc_ogn_test", alias="xc_ogn_test"):
        try:
            if env in self.D_MONGO_CONFIG.keys():
                if name in self.D_MONGO_CONFIG[env].keys():
                    cfg = self.D_MONGO_CONFIG[env][name]
                    if connect_type == "auth":
                        client = MongoClient(
                            host=cfg["host"],
                            port=cfg["port"],
                            username=cfg["username"],
                            password=cfg["password"],
                            authSource=name
                        )
                        db = client[name]
                        return db
                    elif connect_type == "odm":
                        connect(
                            alias="default",
                            db="xc_ogn_test",
                            host=self.test_server_host,
                            port=8200,
                            username="sj_test",
                            password="test4321"
                        )
                        connect(
                            alias=alias,
                            db=name,
                            host=cfg["host"],
                            port=cfg["port"],
                            username=cfg["username"],
                            password=cfg["password"]
                        )
                    else:
                        raise LookupError(f"{connect_type} is not in available connect type!")
                else:
                    raise LookupError(f"{name} is not in available name!")
            else:
                raise LookupError(f"{env} is not in available env!")
        except Exception as e:
            print(e)
