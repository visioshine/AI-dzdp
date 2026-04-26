#!/usr/bin/env python3

"""
更新特定产品的图片URL
1. 替换星光大道KTV的图片
2. 替换所有沐足类产品的图片为美女按摩的图片
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import models
from backend.database import SessionLocal, engine

# 创建会话
db = SessionLocal()

print("正在更新特定产品的图片URL...")

# 1. 更新星光大道KTV的图片
ktv_name = "星光大道KTV"
ktv_merchant = db.query(models.Merchant).filter(models.Merchant.name == ktv_name).first()
if ktv_merchant:
    ktv_merchant.image_url = "https://picsum.photos/id/210/800/450"  # 新的KTV图片
    db.commit()
    print(f"成功更新 '{ktv_name}' 的图片")
else:
    print(f"未找到商家 '{ktv_name}'")

# 2. 更新所有沐足类产品的图片为美女按摩的图片
foot_massage_merchants = ["皇家沐足会所", "华夏足道", "御足堂"]
foot_massage_images = [
    "https://picsum.photos/id/321/800/450",  # 美女按摩图片1
    "https://picsum.photos/id/322/800/450",  # 美女按摩图片2
    "https://picsum.photos/id/323/800/450"   # 美女按摩图片3
]

for i, merchant_name in enumerate(foot_massage_merchants):
    merchant = db.query(models.Merchant).filter(models.Merchant.name == merchant_name).first()
    if merchant:
        merchant.image_url = foot_massage_images[i % len(foot_massage_images)]
        db.commit()
        print(f"成功更新 '{merchant_name}' 的图片为美女按摩图片")
    else:
        print(f"未找到商家 '{merchant_name}'")

# 关闭会话
db.close()

print("特定产品图片URL更新完成！")
