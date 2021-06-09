from typing import List

from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1/ProjectName"
    # SECRET_KEY 记得保密生产环境 不要直接写在代码里面
    SECRET_KEY: str = "(-ASp+_)-0848hnvVG-iqKyJSD&*&^-H3C9mqEqSl8KN-YRzRE"

    # jwt加密算法
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    BACKEND_CORS_ORIGINS: List[str] = ['*']

    # mysql 配置
    MYSQL_DIALECT = 'mysql'  # 要用的什么数据库
    MYSQL_DRIVER = 'pymysql'  # 连接数据库驱动
    MYSQL_USERNAME = ''  # 用户名
    MYSQL_PASSWORD = ''  # 密码
    MYSQL_HOST = ''  # 服务器
    MYSQL_PORT = '3306'  # 端口
    MYSQL_DATABASE = ''  # 数据库名
    MYSQL_SQLALCHEMY_DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(
        MYSQL_DIALECT, MYSQL_DRIVER, MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DATABASE)

    # redis配置
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PASSWORD: str = "111"
    REDIS_DB: int = 0
    CELERY_REDIS_DB: int = 1
    REDIS_PORT: int = 6379
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}?encoding=utf-8"
    CELERY_REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}/{CELERY_REDIS_DB}"


settings = Settings()
