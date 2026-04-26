#!/usr/bin/env python3

"""
简单更新特定产品的图片URL
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend import models
from backend.database import SessionLocal, engine

# 创建会话
db = SessionLocal()

print("正在更新图片...")

# 1. 更新星光大道KTV的图片
try:
    ktv_merchant = db.query(models.Merchant).filter(models.Merchant.name == "星光大道KTV").first()
    if ktv_merchant:
        ktv_merchant.image_url = "https://picsum.photos/id/210/800/450"
        db.commit()
        print("✅ 更新星光大道KTV图片成功")
    else:
        print("❌ 未找到星光大道KTV")
except Exception as e:
    print(f"❌ 更新星光大道KTV时出错: {e}")
    db.rollback()

# 2. 更新皇家沐足会所的图片
try:
    merchant = db.query(models.Merchant).filter(models.Merchant.name == "皇家沐足会所").first()
    if merchant:
        merchant.image_url = "https://picsum.photos/id/321/800/450"
        db.commit()
        print("✅ 更新皇家沐足会所图片成功")
    else:
        print("❌ 未找到皇家沐足会所")
except Exception as e:
    print(f"❌ 更新皇家沐足会所时出错: {e}")
    db.rollback()

# 3. 更新华夏足道的图片
try:
    merchant = db.query(models.Merchant).filter(models.Merchant.name == "华夏足道").first()
    if merchant:
        merchant.image_url = "https://picsum.photos/id/322/800/450"
        db.commit()
        print("✅ 更新华夏足道图片成功")
    else:
        print("❌ 未找到华夏足道")
except Exception as e:
    print(f"❌ 更新华夏足道时出错: {e}")
    db.rollback()

# 4. 更新御足堂的图片
try:
    merchant = db.query(models.Merchant).filter(models.Merchant.name == "御足堂").first()
    if merchant:
        merchant.image_url = "https://picsum.photos/id/323/800/450"
        db.commit()
        print("✅ 更新御足堂图片成功")
    else:
        print("❌ 未找到御足堂")
except Exception as e:
    print(f"❌ 更新御足堂时出错: {e}")
    db.rollback()

# 关闭会话
db.close()

print("图片更新完成！")
