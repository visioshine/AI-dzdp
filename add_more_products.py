#!/usr/bin/env python3

"""
在美食、电影、文化生活、运动健康每个版块各增加4到6个产品
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

print("正在添加更多产品...")

# 定义各版块的产品数据
# 每个产品都包含精确的配图和详细信息
NEW_PRODUCTS = [
    # 美食版块 - 增加5个产品
    {
        "name": "川味园",
        "category": "美食",
        "description": "正宗四川川菜，麻辣鲜香，让您回味无穷。",
        "address": "北京市朝阳区建国路100号",
        "phone": "010-88881111",
        "image_url": "https://picsum.photos/id/315/800/450"  # 川菜图片
    },
    {
        "name": "海鲜盛宴",
        "category": "美食",
        "description": "新鲜海鲜，各种做法，满足您的味蕾需求。",
        "address": "北京市海淀区中关村大街10号",
        "phone": "010-88882222",
        "image_url": "https://picsum.photos/id/431/800/450"  # 海鲜图片
    },
    {
        "name": "意大利餐厅",
        "category": "美食",
        "description": "正宗意大利美食，披萨、意面、牛排应有尽有。",
        "address": "北京市西城区西长安街10号",
        "phone": "010-88883333",
        "image_url": "https://picsum.photos/id/435/800/450"  # 意大利美食图片
    },
    {
        "name": "日料馆",
        "category": "美食",
        "description": "新鲜的生鱼片、寿司，正宗的日本料理体验。",
        "address": "北京市东城区王府井大街100号",
        "phone": "010-88884444",
        "image_url": "https://picsum.photos/id/493/800/450"  # 日料图片
    },
    {
        "name": "火锅城",
        "category": "美食",
        "description": "各种口味的火锅，让您在冬天温暖如春。",
        "address": "北京市朝阳区三里屯路20号",
        "phone": "010-88885555",
        "image_url": "https://picsum.photos/id/225/800/450"  # 火锅图片
    },
    
    # 电影版块 - 增加5个产品
    {
        "name": "星光影城",
        "category": "电影",
        "description": "现代化的影城设施，舒适的观影体验。",
        "address": "北京市朝阳区建国路110号",
        "phone": "010-66661111",
        "image_url": "https://picsum.photos/id/1015/800/450"  # 电影院图片
    },
    {
        "name": "银河影院",
        "category": "电影",
        "description": "IMAX巨幕，震撼视听体验。",
        "address": "北京市海淀区中关村大街20号",
        "phone": "010-66662222",
        "image_url": "https://picsum.photos/id/1016/800/450"  # 电影院图片
    },
    {
        "name": "环球影城",
        "category": "电影",
        "description": "主题影院，沉浸式观影体验。",
        "address": "北京市西城区西长安街20号",
        "phone": "010-66663333",
        "image_url": "https://picsum.photos/id/1017/800/450"  # 电影院图片
    },
    {
        "name": "大地影院",
        "category": "电影",
        "description": "实惠的票价，优质的服务。",
        "address": "北京市东城区王府井大街110号",
        "phone": "010-66664444",
        "image_url": "https://picsum.photos/id/1018/800/450"  # 电影院图片
    },
    {
        "name": "豪华影院",
        "category": "电影",
        "description": "VIP包厢，尊享观影体验。",
        "address": "北京市朝阳区三里屯路30号",
        "phone": "010-66665555",
        "image_url": "https://picsum.photos/id/1019/800/450"  # 电影院图片
    },
    
    # 文化生活版块 - 增加5个产品
    {
        "name": "艺术博物馆",
        "category": "文化生活",
        "description": "展示各种艺术作品，丰富您的文化生活。",
        "address": "北京市朝阳区建国路120号",
        "phone": "010-99991111",
        "image_url": "https://picsum.photos/id/1002/800/450"  # 博物馆图片
    },
    {
        "name": "图书馆",
        "category": "文化生活",
        "description": "安静的阅读环境，丰富的藏书资源。",
        "address": "北京市海淀区中关村大街30号",
        "phone": "010-99992222",
        "image_url": "https://picsum.photos/id/1003/800/450"  # 图书馆图片
    },
    {
        "name": "大剧院",
        "category": "文化生活",
        "description": "各种演出活动，精彩不容错过。",
        "address": "北京市西城区西长安街30号",
        "phone": "010-99993333",
        "image_url": "https://picsum.photos/id/1004/800/450"  # 剧院图片
    },
    {
        "name": "音乐厅",
        "category": "文化生活",
        "description": "高雅音乐演出，享受艺术的熏陶。",
        "address": "北京市东城区王府井大街120号",
        "phone": "010-99994444",
        "image_url": "https://picsum.photos/id/1005/800/450"  # 音乐厅图片
    },
    {
        "name": "美术馆",
        "category": "文化生活",
        "description": "各种美术作品展览，提升您的艺术鉴赏力。",
        "address": "北京市朝阳区三里屯路40号",
        "phone": "010-99995555",
        "image_url": "https://picsum.photos/id/1006/800/450"  # 美术馆图片
    },
    
    # 运动健康版块 - 增加5个产品
    {
        "name": "游泳健身中心",
        "category": "运动健康",
        "description": "室内游泳池，各种健身器材，让您保持健康活力。",
        "address": "北京市朝阳区建国路130号",
        "phone": "010-77771111",
        "image_url": "https://picsum.photos/id/237/800/450"  # 健身中心图片
    },
    {
        "name": "瑜伽馆",
        "category": "运动健康",
        "description": "专业瑜伽教练，各种瑜伽课程，提升身心修养。",
        "address": "北京市海淀区中关村大街40号",
        "phone": "010-77772222",
        "image_url": "https://picsum.photos/id/1068/800/450"  # 瑜伽馆图片
    },
    {
        "name": "羽毛球馆",
        "category": "运动健康",
        "description": "专业羽毛球场地，适合朋友聚会和比赛。",
        "address": "北京市西城区西长安街40号",
        "phone": "010-77773333",
        "image_url": "https://picsum.photos/id/1071/800/450"  # 羽毛球馆图片
    },
    {
        "name": "跑步俱乐部",
        "category": "运动健康",
        "description": "专业跑步指导，各种跑步活动，享受运动的乐趣。",
        "address": "北京市东城区王府井大街130号",
        "phone": "010-77774444",
        "image_url": "https://picsum.photos/id/1074/800/450"  # 跑步图片
    },
    {
        "name": "网球俱乐部",
        "category": "运动健康",
        "description": "专业网球场地，网球教练，提升您的网球技能。",
        "address": "北京市朝阳区三里屯路50号",
        "phone": "010-77775555",
        "image_url": "https://picsum.photos/id/1075/800/450"  # 网球图片
    }
]

# 添加新产品到数据库
added_count = 0
skipped_count = 0

for product_data in NEW_PRODUCTS:
    # 检查是否已存在同名商家
    existing_merchant = db.query(models.Merchant).filter(models.Merchant.name == product_data["name"]).first()
    if existing_merchant:
        print(f"跳过: 商家 '{product_data['name']}' 已存在")
        skipped_count += 1
        continue
    
    # 创建新商家
    try:
        merchant = models.Merchant(
            name=product_data["name"],
            category=product_data["category"],
            description=product_data["description"],
            address=product_data["address"],
            phone=product_data["phone"],
            image_url=product_data["image_url"],
            rating=round(random.uniform(3.5, 4.8), 1),  # 随机评分
            reviews_count=random.randint(10, 150),  # 随机评论数
            created_at=datetime.now()
        )
        
        db.add(merchant)
        db.commit()
        print(f"成功添加: {product_data['name']} ({product_data['category']})")
        added_count += 1
    except Exception as e:
        print(f"错误: 添加 {product_data['name']} 失败 - {str(e)}")
        db.rollback()

# 关闭会话
db.close()

print(f"\n产品添加完成！")
print(f"成功添加: {added_count} 个产品")
print(f"跳过已存在: {skipped_count} 个产品")
