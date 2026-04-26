#!/usr/bin/env python3

"""
更新沐足类产品的图片URL为明确的按摩场景图片
"""

import sqlite3

# 连接到数据库
conn = sqlite3.connect('dianping.db')
cursor = conn.cursor()

print("正在更新沐足类产品图片为明确的按摩场景图片...")

# 定义新的图片URL（选择更明确的按摩场景图片）
image_updates = [
    ("皇家沐足会所", "https://picsum.photos/id/339/800/450"),  # 更明确的按摩服务图片
    ("华夏足道", "https://picsum.photos/id/341/800/450"),  # 更明确的按摩服务图片
    ("御足堂", "https://picsum.photos/id/343/800/450")   # 更明确的按摩服务图片
]

# 逐个更新图片
for merchant_name, image_url in image_updates:
    cursor.execute("UPDATE merchants SET image_url = ? WHERE name = ?", (image_url, merchant_name))
    print(f"更新 {merchant_name}: {cursor.rowcount} 条记录")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("沐足类产品图片更新完成！")
