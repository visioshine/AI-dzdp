#!/usr/bin/env python3

"""
在休闲娱乐版块添加3个沐足产品和2个KTV产品
"""

import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import datetime
from backend import models
from backend.database import SessionLocal, engine

# 创建会话
db = SessionLocal()

# 定义新的休闲娱乐产品
LEISURE_PRODUCTS = [
    # 3个沐足产品
    {
        "name": "皇家沐足会所",
        "category": "休闲娱乐",
        "description": "专业的足底按摩和SPA服务，环境舒适，技师专业。",
        "address": "北京市朝阳区建国路99号",
        "phone": "010-12345678",
        "image_url": "https://picsum.photos/id/201/800/450"  # 沐足图片
    },
    {
        "name": "华夏足道",
        "category": "休闲娱乐",
        "description": "传统中医足疗，缓解疲劳，促进血液循环。",
        "address": "北京市海淀区中关村大街2号",
        "phone": "010-23456789",
        "image_url": "https://picsum.photos/id/202/800/450"  # 沐足图片
    },
    {
        "name": "御足堂",
        "category": "休闲娱乐",
        "description": "高端沐足服务，提供各种养生项目和茶水点心。",
        "address": "北京市西城区西长安街2号",
        "phone": "010-34567890",
        "image_url": "https://picsum.photos/id/203/800/450"  # 沐足图片
    },
    # 2个KTV产品
    {
        "name": "金色年华KTV",
        "category": "休闲娱乐",
        "description": "豪华KTV包厢，先进的音响设备，丰富的歌曲库。",
        "address": "北京市东城区王府井大街99号",
        "phone": "010-45678901",
        "image_url": "https://picsum.photos/id/204/800/450"  # KTV图片
    },
    {
        "name": "星光大道KTV",
        "category": "休闲娱乐",
        "description": "时尚的KTV环境，适合朋友聚会和生日派对。",
        "address": "北京市朝阳区三里屯路19号",
        "phone": "010-56789012",
        "image_url": "https://picsum.photos/id/205/800/450"  # KTV图片
    }
]

print("正在添加休闲娱乐产品...")

# 添加新产品到数据库
for product_data in LEISURE_PRODUCTS:
    # 检查是否已存在同名商家
    existing_merchant = db.query(models.Merchant).filter(models.Merchant.name == product_data["name"]).first()
    if existing_merchant:
        print(f"商家 '{product_data['name']}' 已存在，跳过")
        continue
    
    # 创建新商家
    merchant = models.Merchant(
        name=product_data["name"],
        category=product_data["category"],
        description=product_data["description"],
        address=product_data["address"],
        phone=product_data["phone"],
        image_url=product_data["image_url"],
        rating=round(random.uniform(3.5, 4.8), 1),  # 随机评分
        reviews_count=random.randint(5, 80),  # 随机评论数
        created_at=datetime.utcnow()
    )
    
    db.add(merchant)
    db.commit()
    print(f"成功添加商家: {product_data['name']}")

# 关闭会话
db.close()

print("休闲娱乐产品添加完成！")
