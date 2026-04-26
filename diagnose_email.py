#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
邮件服务诊断工具
"""

import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.config import EmailConfig
from backend import email_service

print("=" * 60)
print("邮件服务诊断工具")
print("=" * 60)

# 1. 检查配置加载
print("\n1. 配置检查:")
print(f"   ENABLE_EMAIL_SENDING: {EmailConfig.ENABLE_EMAIL_SENDING}")
print(f"   SMTP_SERVER: {EmailConfig.SMTP_SERVER}")
print(f"   SMTP_PORT: {EmailConfig.SMTP_PORT}")
print(f"   SMTP_USERNAME: {EmailConfig.SMTP_USERNAME}")
print(f"   SENDER_EMAIL: {EmailConfig.SENDER_EMAIL}")
print(f"   is_configured(): {EmailConfig.is_configured()}")

# 2. 测试邮件发送
print("\n2. 测试邮件发送:")
test_email = EmailConfig.SMTP_USERNAME
test_code = "123456"

print(f"   正在发送测试邮件到: {test_email}")
print(f"   测试验证码: {test_code}")

success, message = email_service.send_password_reset_email(test_email, test_code)

if success:
    print(f"   [OK] 邮件发送成功!")
    print(f"   消息: {message}")
else:
    print(f"   [FAIL] 邮件发送失败!")
    print(f"   错误: {message}")

print("\n" + "=" * 60)
print("诊断完成!")
print("=" * 60)
