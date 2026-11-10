from contextlib import asynccontextmanager
from uuid import uuid4
import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from app.api.v1.router import router
from app.core.config import get_settings
from app.core.database import get_engine
from app.shared.response import failure


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    get_engine().dispose()


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title='PuppleTrouble · 玩犊紫', version='0.1.0', lifespan=lifespan)

    @application.middleware('http')
    async def request_context(request: Request, call_next):
        request.state.request_id = str(uuid4())
        try:
            response = await call_next(request)
        except Exception:
            logging.getLogger(__name__).exception('请求处理失败，request_id=%s', request.state.request_id)
            response = JSONResponse(status_code=500, content=failure(request, 'INTERNAL_ERROR', '服务暂时不可用'))
        response.headers['X-Request-ID'] = request.state.request_id
        return response

    @application.exception_handler(HTTPException)
    async def http_error(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content=failure(request, f'HTTP_{exc.status_code}', str(exc.detail)), headers=exc.headers)

    @application.exception_handler(RequestValidationError)
    async def validation_error(request: Request, exc: RequestValidationError):
        # 不回显输入，以免异常响应泄露密码或令牌。
        fields = [{'field': '.'.join(map(str, item['loc'])), 'type': item['type']} for item in exc.errors()]
        return JSONResponse(status_code=422, content=failure(request, 'VALIDATION_ERROR', '请求字段不符合要求', {'fields': fields}))

    application.include_router(router)
    # CORS 包在错误处理外层，使失败响应也可被允许的 Web 来源读取。
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=False,
        allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS'],
        allow_headers=['Authorization', 'Content-Type', 'Idempotency-Key'],
        expose_headers=['X-Request-ID'],
    )
    return application


app = create_app()
