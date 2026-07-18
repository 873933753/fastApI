from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.libs.exceptions import AppError

# 注册异常处理函数
def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request, exc: AppError):
        return JSONResponse(
            status_code=exc.http_status,
            content={
                'code': exc.code,
                'message': exc.message,
                'data': None,
            },
        )
