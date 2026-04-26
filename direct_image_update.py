#!/usr/bin/env python3

"""
直接更新数据库中的图片URL
"""

import sqlite3

# 连接到数据库
conn = sqlite3.connect('dianping.db')
cursor = conn.cursor()

print("正在直接更新图片URL...")

# 1. 更新星光大道KTV的图片
cursor.execute("UPDATE merchants SET image_url = 'https://picsum.photos/id/210/800/450' WHERE name = '星光大道KTV'")
print(f"更新星光大道KTV: {cursor.rowcount} 条记录")

# 2. 更新皇家沐足会所的图片
cursor.execute("UPDATE merchants SET image_url = 'https://picsum.photos/id/321/800/450' WHERE name = '皇家沐足会所'")
print(f"更新皇家沐足会所: {cursor.rowcount} 条记录")

# 3. 更新华夏足道的图片
cursor.execute("UPDATE merchants SET image_url = 'https://picsum.photos/id/322/800/450' WHERE name = '华夏足道'")
print(f"更新华夏足道: {cursor.rowcount} 条记录")

# 4. 更新御足堂的图片
cursor.execute("UPDATE merchants SET image_url = 'https://picsum.photos/id/323/800/450' WHERE name = '御足堂'")
print(f"更新御足堂: {cursor.rowcount} 条记录")

# 提交更改并关闭连接
conn.commit()
conn.close()

print("图片URL更新完成！")
