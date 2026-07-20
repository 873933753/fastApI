from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.libs.exceptions import AppError

def register_exception_handlers(app: FastAPI) -> None:
    # 应用错误处理 - 自定义异常
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
    # 参数校验失败处理
    # RequestValidationError 是 FastAPI 内置的异常类，用于处理请求参数校验失败的情况
    # 当请求参数校验失败时，会抛出 RequestValidationError 异常
    # 使用的地方：app/forms/auth.py
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=422,
            content={
                "code": 42200,
                "message": _first_validation_message(exc),
                "data": None,
            },
        )

# 获取第一个参数校验失败的消息
# 只取第一条错误,多个字段同时出错时，只返回第一个 message。对注册表单通常够用
# 私有方法 - 只用于内部使用
def _first_validation_message(exc: RequestValidationError) -> str:
    errors = exc.errors()
    if not errors:
        return "参数校验失败"
    msg = errors[0].get("msg", "参数校验失败")
    # 去掉 Pydantic 自带的 "Value error, " 前缀
    if msg.startswith("Value error, "):
        msg = msg[len("Value error, "):]
    return msg