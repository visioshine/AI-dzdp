from backend.database import SessionLocal, engine
from backend import models, auth
from datetime import datetime

# 创建数据库表（如果不存在）
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 创建visioshine用户
username = "visioshine"
email = "641077621@qq.com"
password = "password123"  # 默认密码，可以登录后修改
phone = "13800138000"  # 示例手机号

# 检查用户是否已经存在
user = db.query(models.User).filter(
    (models.User.username == username) | 
    (models.User.email == email)
).first()

if user:
    print(f"用户已存在: 用户名={user.username}, 邮箱={user.email}")
else:
    # 创建新用户
    hashed_password = auth.get_password_hash(password)
    user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password,
        phone=phone,
        avatar="https://api.dicebear.com/7.x/avataaars/svg?seed=visioshine",
        created_at=datetime.utcnow()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"用户创建成功: 用户名={user.username}, 邮箱={user.email}, 密码={password} (可以登录后修改)")

db.close()