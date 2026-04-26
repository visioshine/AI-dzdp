from backend.database import SessionLocal, engine
from backend import models
from datetime import datetime
import random

# 创建数据库表（如果不存在）
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 检查是否已有商家数据
if db.query(models.Merchant).count() > 0:
    print("数据库中已有商家数据，无需重复添加")
    db.close()
    exit()

# 模拟商家数据
MERCHANTS = [
    {
        "name": "快乐餐厅",
        "category": "美食",
        "description": "提供各种中式美食，环境优雅，服务周到。",
        "address": "北京市朝阳区建国路88号",
        "phone": "010-88888888",
        "image_url": "https://console.enterprise.trae.cn/api/ide/v1/text_to_image?prompt=A%20delicious%20Chinese%20restaurant%20interior%20with%20warm%20lighting&image_size=landscape_16_9",


    },
    {
        "name": "电影时光影城",
        "category": "电影",
        "description": "最新的3D电影技术，舒适的观影环境。",
        "address": "北京市海淀区中关村大街1号",
        "phone": "010-66666666",
        "image_url": "https://console.enterprise.trae.cn/api/ide/v1/text_to_image?prompt=Modern%20movie%20theater%20with%20comfortable%20seats&image_size=landscape_16_9",


    },
    {
        "name": "健身俱乐部",
        "category": "运动健康",
        "description": "专业的健身器材，多种健身课程可选。",
        "address": "北京市西城区西长安街1号",
        "phone": "010-77777777",
        "image_url": "https://console.enterprise.trae.cn/api/ide/v1/text_to_image?prompt=Modern%20fitness%20center%20with%20gym%20equipment&image_size=landscape_16_9",


    },
    {
        "name": "咖啡时光",
        "category": "休闲娱乐",
        "description": "正宗意大利咖啡，舒适的阅读环境。",
        "address": "北京市东城区王府井大街88号",
        "phone": "010-55555555",
        "image_url": "https://console.enterprise.trae.cn/api/ide/v1/text_to_image?prompt=Cozy%20coffee%20shop%20with%20warm%20atmosphere&image_size=landscape_16_9",


    },
    {
        "name": "书城",
        "category": "文化生活",
        "description": "各类书籍齐全，安静的阅读空间。",
        "address": "北京市海淀区中关村南大街3号",
        "phone": "010-99999999",
        "image_url": "https://console.enterprise.trae.cn/api/ide/v1/text_to_image?prompt=Large%20bookstore%20with%20many%20bookshelves&image_size=landscape_16_9",


    }
]

# 添加商家数据到数据库
print("正在添加商家数据...")
for merchant_data in MERCHANTS:
    merchant = models.Merchant(
        name=merchant_data["name"],
        category=merchant_data["category"],
        description=merchant_data["description"],
        address=merchant_data["address"],
        phone=merchant_data["phone"],
        image_url=merchant_data["image_url"],
        rating=round(random.uniform(3.5, 4.8), 1),
        reviews_count=random.randint(10, 100),
        created_at=datetime.utcnow()
    )
    db.add(merchant)

db.commit()
print(f"成功添加 {len(MERCHANTS)} 个商家")

db.close()