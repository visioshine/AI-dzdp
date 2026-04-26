import sqlite3
import os

# 数据库文件路径 (应该在 backend 目录下)
db_path = "d:\\workspace\\trae-space\\05_project_sole_cn\\dazhongdianping\\backend\\dianping.db"

print(f"Checking database: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

if os.path.exists(db_path):
    # 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n1. Checking tables...")
    # 查看所有表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tables: {[table[0] for table in tables]}")
    
    # 查看 merchants 表结构
    if 'merchants' in [table[0] for table in tables]:
        print("\n2. Checking merchants table structure...")
        cursor.execute("PRAGMA table_info(merchants);")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Column: {col[1]} (Type: {col[2]})")
        
        # 查看 merchants 表数据
        print("\n3. Checking merchants table data...")
        cursor.execute("SELECT * FROM merchants;")
        rows = cursor.fetchall()
        print(f"Total merchants: {len(rows)}")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Category: {row[4]}")
    
    # 关闭连接
    conn.close()
else:
    # 尝试在根目录查找
    root_db_path = "d:\\workspace\\trae-space\\05_project_sole_cn\\dazhongdianping\\dianping.db"
    print(f"\nChecking root directory database: {root_db_path}")
    print(f"Root database exists: {os.path.exists(root_db_path)}")

print("\nDatabase check completed!")
