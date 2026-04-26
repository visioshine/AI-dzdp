#!/usr/bin/env python3

"""
更新沐足类产品的图片URL为更合适的图片
"""

import sqlite3

# 连接到数据库
conn = sqlite3.connect('dianping.db')
cursor = conn.cursor()

print("正在更新沐足类产品图片...")

# 定义新的图片URL（使用合适的按摩相关图片）
new_images = [
    "https://picsum.photos/id/338/800/450",  # 按摩服务图片1
    "https://picsum.photos/id/340/800/450",  # 按摩服务图片2
    "https://picsum.photos/id/342/800/450"   # 按摩服务图片3
]

# 定义沐足类产品名称
foot_massage_merchants = ["皇家沐足会所", "华夏足道", "御足堂"]

# 逐个更新图片
for i, merchant_name in enumerate(foot_massage_merchants):
    image_url = new_images[i % len(new_images)]
    cursor.execute("UPDATE merchants SET image_url = ? WHERE name = ?", (image_url, merchant_name))
    print(f"更新 {merchant_name}: {cursor.rowcount} 条记录")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("沐足类产品图片更新完成！")
