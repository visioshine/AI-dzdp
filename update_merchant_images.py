#!/usr/bin/env python3

"""
更新数据库中商家的图片URL
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import models
from backend.database import SessionLocal, engine

# 创建会话
db = SessionLocal()

# 定义新的图片URL
merchant_images = {
    "快乐餐厅": "https://source.unsplash.com/random/?restaurant,chinese",
    "电影时光影城": "https://source.unsplash.com/random/?movie,theater",
    "健身俱乐部": "https://source.unsplash.com/random/?fitness,center",
    "咖啡时光": "https://source.unsplash.com/random/?coffee,shop",
    "书城": "https://source.unsplash.com/random/?bookstore,books"
}

print("正在更新商家图片URL...")

# 更新每个商家的图片URL
for merchant_name, image_url in merchant_images.items():
    merchant = db.query(models.Merchant).filter(models.Merchant.name == merchant_name).first()
    if merchant:
        merchant.image_url = image_url
        db.commit()
        print(f"成功更新商家 '{merchant_name}' 的图片URL")
    else:
        print(f"未找到商家 '{merchant_name}'")

# 关闭会话
db.close()

print("图片URL更新完成！")
