import os
from dotenv import load_dotenv

# 加载 .env 中的环境变量（AppKey、DATABASE_URL 等）
load_dotenv()

# 数据库连接串，从 .env 读取
DATABASE_URL = os.getenv("DATABASE_URL")

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