from backend.database import SessionLocal, engine
from backend import models

# 创建数据库表（如果不存在）
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 查询所有用户
users = db.query(models.User).all()

print("当前数据库中的用户:")
for user in users:
    print(f"ID: {user.id}, 用户名: {user.username}, 邮箱: {user.email}, 手机号: {user.phone}, 注册时间: {user.created_at}")

# 专门查询visioshine用户
visioshine_user = db.query(models.User).filter(models.User.username == "visioshine").first()
if visioshine_user:
    print(f"\n找到visioshine用户: ID={visioshine_user.id}, 邮箱={visioshine_user.email}")
else:
    print("\n未找到visioshine用户")

db.close()