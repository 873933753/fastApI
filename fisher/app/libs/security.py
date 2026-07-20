import bcrypt

# 密码加密
def hash_password(plain: str) -> str:
    # gensalt() 生成随机盐；hashpw 返回 bytes，入库存 str
    hashed = bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")
    
# 密码验证
def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        plain.encode("utf-8"),
        hashed.encode("utf-8"),
    )