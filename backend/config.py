#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# 加载环境变量（如果有 .env 文件）
load_dotenv()

class EmailConfig:
    """邮件服务配置"""
    
    # SMTP服务器配置
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.qq.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    SENDER_EMAIL = os.getenv('SENDER_EMAIL', SMTP_USERNAME)
    
    # 是否启用真实邮件发送
    ENABLE_EMAIL_SENDING = os.getenv('ENABLE_EMAIL_SENDING', 'false').lower() == 'true'
    
    @classmethod
    def is_configured(cls):
        """检查邮件配置是否完整"""
        return all([
            cls.SMTP_SERVER,
            cls.SMTP_PORT,
            cls.SMTP_USERNAME,
            cls.SMTP_PASSWORD
        ])

class AppConfig:
    """应用通用配置"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))
    PASSWORD_RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv('PASSWORD_RESET_TOKEN_EXPIRE_MINUTES', '15'))
