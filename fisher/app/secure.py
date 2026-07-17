import os
from dotenv import load_dotenv

# 加载 .env 中的环境变量（AppKey、DATABASE_URL 等）
load_dotenv()

# 数据库连接串，从 .env 读取
DATABASE_URL = os.getenv("DATABASE_URL")
