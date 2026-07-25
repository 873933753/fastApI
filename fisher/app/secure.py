import os
from dotenv import load_dotenv

# 加载 .env 中的环境变量（AppKey、DATABASE_URL 等）
load_dotenv()

# 运行环境：dev / staging / prod
APP_ENV = os.getenv("APP_ENV", "dev").lower()
IS_PROD = APP_ENV == "prod"

# 数据库连接串，从 .env 读取
DATABASE_URL = os.getenv("DATABASE_URL")
# SQLAlchemy echo：控制台打印 SQL，开发可设 true，生产保持 false
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() in ("1", "true", "yes")

# jwt配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES"))

# 邮箱配置
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME =  os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_SENDER = f"Hanber <{MAIL_USERNAME}>"

# redis配置
REDIS_URL = os.getenv("REDIS_URL")