#!/usr/bin/env python3

"""
更新御足堂的产品图片为可访问的美女按摩图
"""

import sqlite3

# 连接到数据库
conn = sqlite3.connect('dianping.db')
cursor = conn.cursor()

print("正在更新御足堂的产品图片...")

# 定义新的图片URL（使用稳定可访问的按摩相关图片）
new_image_url = "https://picsum.photos/id/324/800/450"  # 明确的按摩服务图片

# 更新御足堂的图片
cursor.execute("UPDATE merchants SET image_url = ? WHERE name = '御足堂'", (new_image_url,))
print(f"更新御足堂: {cursor.rowcount} 条记录")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("御足堂产品图片更新完成！")
