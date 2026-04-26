#!/usr/bin/env python3

"""
更新数据库中商家的图片URL为稳定可访问的图片
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import models
from backend.database import SessionLocal, engine

# 创建会话
db = SessionLocal()

# 定义稳定的图片URL（使用Picsum Photos服务）
merchant_images = {
    "快乐餐厅": "https://picsum.photos/id/1080/800/450",  # 餐厅图片
    "电影时光影城": "https://picsum.photos/id/1025/800/450",  # 电影院图片
    "健身俱乐部": "https://picsum.photos/id/1062/800/450",  # 健身中心图片
    "咖啡时光": "https://picsum.photos/id/1060/800/450",  # 咖啡店图片
    "书城": "https://picsum.photos/id/119/800/450"  # 书店图片
}

print("正在更新商家图片URL为稳定可访问的图片...")

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
