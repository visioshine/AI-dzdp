from backend.database import SessionLocal, engine
from backend import models

# 创建数据库表（如果不存在）
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 查询所有商家
merchants = db.query(models.Merchant).all()

print("当前数据库中的商家:")
for merchant in merchants:
    print(f"ID: {merchant.id}, 名称: {merchant.name}, 分类: {merchant.category}, 评分: {merchant.rating}, 评价数: {merchant.reviews_count}")

print(f"\n总商家数: {len(merchants)}")

db.close()