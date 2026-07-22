import re # 正则表达式
from typing import Annotated
from pydantic import BaseModel, field_validator, AfterValidator,StringConstraints


# 邮箱验证规则
def _strip_required_email(v: str) -> str:
    v = (v or "").strip()
    if not v:
        raise ValueError("请输入正确的邮箱")
    return v
def _validate_register_email(v: str) -> str:
    v = _strip_required_email(v)  # 先复用基础规则；若文案要「电子邮箱不可以为空」可单独写
    if len(v) < 8 or len(v) > 64:
        raise ValueError("电子邮箱长度需在8到64个字符之间")
    if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
        raise ValueError("电子邮箱不符合规范")
    return v

# 昵称类型 - 使用注解
Nickname = Annotated[
    str,
    # StringConstraints - 字符串约束
    # strip_whitespace=True - 去空格
    # min_length=2 - 最小长度2
    # max_length=10 - 最大长度10
    StringConstraints(strip_whitespace=True, min_length=2, max_length=10),
]

# 登录 / 找回密码等：只要求有邮箱
Email = Annotated[str, AfterValidator(_strip_required_email)]

# 注册：完整校验
RegisterEmail = Annotated[str, AfterValidator(_validate_register_email)]

class RegisterForm(BaseModel):
    email: Email
    password: str
    nickname: Nickname

    # # field_validator - 会自动调用 validate_email，与handlers.py中的validation_exception_handler对应
    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, v: str) -> str:
    #     # 去空格
    #     v = (v or "").strip()
    #     if not v:
    #         # raise - 抛出异常
    #         raise ValueError("电子邮箱不可以为空")
    #     if len(v) < 8 or len(v) > 64:
    #         raise ValueError("电子邮箱长度需在8到64个字符之间")
    #     # 对应 WTForms 的 Email(message='电子邮箱不符合规范')
    #     if not re.fullmatch(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", v):
    #         raise ValueError("电子邮箱不符合规范")
    #     return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("密码不可以为空，请输入你的密码")
        if len(v) < 6 or len(v) > 32:
            raise ValueError("密码长度需在6到32个字符之间")
        return v

    # @field_validator("nickname")
    # @classmethod
    # def validate_nickname(cls, v: str) -> str:
    #     v = (v or "").strip()
    #     if not v:
    #         raise ValueError("昵称不可以为空")
    #     if len(v) < 2 or len(v) > 10:
    #         raise ValueError("昵称至少需要两个字符，最多10个字符")
    #     return v

class LoginForm(BaseModel):
    email: Email
    password: str

    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, v: str) -> str:
    #     # 去空格
    #     v = (v or "").strip()
    #     if not v:
    #         raise ValueError('请输入正确的邮箱')
    #     return v

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        v = (v or "").strip()
        if not v:
            raise ValueError("密码不可以为空，请输入你的密码")
        return v   

class EmailForm(BaseModel):
    email: Email

    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, v: str) -> str:
    #     # 去空格
    #     v = (v or "").strip()
    #     if not v:
    #         raise ValueError('请输入正确的邮箱')
    #     return v