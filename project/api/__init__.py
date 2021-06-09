import logging
import traceback

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError, ValidationError
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import api_v1_router
from api.utils import response_code
from api.utils.custom_exception import PostParamsError, UserTokenError, UserNotFound, GetParamsError
from database.models import init_db
from database.session import get_redis_pool
from setting import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    init_db()
    app = FastAPI(openapi_url=f"{settings.API_V1_STR}/openapi.json",
                  docs_url=f"{settings.API_V1_STR}/docs",
                  redoc_url=f"{settings.API_V1_STR}/redoc", )
    # 跨域设置
    register_cors(app)

    # 注册路由
    register_router(app)

    # 注册捕获全局异常
    register_exception(app)

    # 请求拦截
    register_middleware(app)

    # 挂载redis
    register_redis(app)

    # 加载数据库定时任务
    # register_cron()

    if settings.DEBUG:
        # 注册静态文件
        register_static_file(app)

    return app


def register_redis(app: FastAPI) -> None:
    """
        把redis挂载到app对象上面
        :param app:
        :return:
    """

    @app.on_event('startup')
    async def startup_event():
        app.state.redis = await get_redis_pool()

    @app.on_event('shutdown')
    async def shutdown_event():
        app.state.redis.close()
        await app.state.redis.wait_closed()


def register_router(app: FastAPI) -> None:
    """
    注册路由
    :param app:
    :return:
    """
    # 项目API
    app.include_router(
        api_v1_router,
        prefix=settings.API_V1_STR  # 前缀
    )


def register_cors(app: FastAPI) -> None:
    """
    支持跨域
    :param app:
    :return:
    """
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost.tiangolo.com",
                           "https://localhost.tiangolo.com",
                           "http://localhost",
                           "http://localhost:8080"],
            allow_credentials=True,  # Credentials (Authorization headers, Cookies, etc)
            allow_methods=["*"],  # Specific HTTP methods (POST, PUT) or all of them with the wildcard "*".
            allow_headers=["*"],  # Specific HTTP headers or all of them with the wildcard "*".
        )


def register_exception(app: FastAPI):
    """
    全局异常捕获
    注意 别手误多敲一个s
    exception_handler
    exception_handlers
    两者有区别
        如果只捕获一个异常 启动会报错
        @exception_handlers(UserNotFound)
    TypeError: 'dict' object is not callable
    :param app:
    :return:
    """

    # 自定义异常 捕获
    @app.exception_handler(UserNotFound)
    async def user_not_found_exception_handler(request: Request, exc: UserNotFound):
        """
        用户认证未找到
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"token未知用户\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.resp_5001(message=exc.err_desc)

    @app.exception_handler(UserTokenError)
    async def user_token_exception_handler(request: Request, exc: UserTokenError):
        """
        用户token异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"用户认证异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.resp_5000(message=exc.err_desc)

    @app.exception_handler(PostParamsError)
    async def query_params_exception_handler(request: Request, exc: PostParamsError):
        """
        内部查询操作时，其他参数异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数查询异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.resp_400(message=exc.err_desc)

    @app.exception_handler(ValidationError)
    async def inner_validation_exception_handler(request: Request, exc: ValidationError):
        """
        内部参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"内部参数验证错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return response_code.resp_500(message=exc.errors())

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        """
        请求参数验证异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(
            f"请求参数格式错误\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return response_code.resp_422(message=exc.errors())

    # 捕获全部异常
    @app.exception_handler(Exception)
    async def all_exception_handler(request: Request, exc: Exception):
        """
        全局所有异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"全局异常\n{request.method}URL:{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")
        return response_code.resp_500(message="Server Error")

    # 本项目新建
    @app.exception_handler(GetParamsError)
    async def get_query_params_exception_handler(request: Request, exc: GetParamsError):
        """
        内部查询操作时，其他参数异常
        :param request:
        :param exc:
        :return:
        """
        logger.error(f"参数查询异常\nURL:{request.method}{request.url}\nHeaders:{request.headers}\n{traceback.format_exc()}")

        return response_code.resp_400(message=exc.err_desc)


def register_middleware(app: FastAPI) -> None:
    """
    请求响应拦截 hook
    https://fastapi.tiangolo.com/tutorial/middleware/
    :param app:
    :return:
    """

    @app.middleware("http")
    async def logger_request(request: Request, call_next):
        # https://stackoverflow.com/questions/60098005/fastapi-starlette-get-client-real-ip
        # logger.info(f"访问记录:{request.method} url:{request.url}\nheaders:{request.headers}\nIP:{request.client.host}")

        response = await call_next(request)

        return response


def register_static_file(app: FastAPI) -> None:
    """
    静态文件交互 生产使用 nginx
    这里是开发是方便本地
    :param app:
    :return:
    """
    from fastapi.staticfiles import StaticFiles
    app.mount("/static_folder", StaticFiles(directory="static_folder"), name="static_folder")
