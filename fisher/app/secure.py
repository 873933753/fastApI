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