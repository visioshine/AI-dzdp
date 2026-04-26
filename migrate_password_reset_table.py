#!/usr/bin/env python3
import sqlite3
from datetime import datetime, timedelta

def migrate_database():
    """创建密码重置邮件表，不删除已有数据"""
    conn = sqlite3.connect('dianping.db')
    cursor = conn.cursor()
    
    try:
        # 检查表是否已存在
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='password_reset_emails'")
        if cursor.fetchone():
            print("password_reset_emails 表已存在，无需创建")
        else:
            # 创建新表
            cursor.execute('''
                CREATE TABLE password_reset_emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT NOT NULL,
                    verification_code TEXT NOT NULL,
                    sent_at TIMESTAMP NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    is_used INTEGER DEFAULT 0,
                    user_id INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            print("password_reset_emails 表创建成功")
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_password_reset_emails_email ON password_reset_emails (email)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_password_reset_emails_code ON password_reset_emails (verification_code)")
        
        conn.commit()
        print("数据库迁移完成")
        
    except Exception as e:
        print(f"迁移过程中发生错误: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
