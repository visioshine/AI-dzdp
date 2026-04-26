#!/usr/bin/env python3
"""测试邮件发送功能"""
import sys
import os

# 添加backend到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend import email_service
from backend.config import EmailConfig

def main():
    print("=" * 60)
    print("邮件服务测试")
    print("=" * 60)
    
    print(f"\n[当前配置状态]")
    print(f"   启用邮件发送: {EmailConfig.ENABLE_EMAIL_SENDING}")
    print(f"   SMTP服务器: {EmailConfig.SMTP_SERVER}:{EmailConfig.SMTP_PORT}")
    print(f"   发件人: {EmailConfig.SENDER_EMAIL}")
    print(f"   配置完整: {'是' if EmailConfig.is_configured() else '否'}")
    
    if not EmailConfig.ENABLE_EMAIL_SENDING:
        print("\n[警告] 邮件服务未启用！")
        print("\n要启用邮件服务，请：")
        print("1. 复制 .env.example 为 .env")
        print("2. 编辑 .env 文件，填写您的邮箱配置")
        print("3. 设置 ENABLE_EMAIL_SENDING=true")
        print("\n详细说明请查看 '邮件配置说明.md'")
        print("\n当前为测试模式，验证码会直接返回在API响应中。")
        return
    
    if not EmailConfig.is_configured():
        print("\n[错误] 邮件配置不完整！")
        print("请检查 .env 文件中的配置项。")
        return
    
    print("\n[成功] 邮件配置完整！")
    
    # 测试发送邮件
    test_email = input("\n请输入测试邮箱地址: ").strip()
    
    if not test_email:
        print("未输入邮箱，退出测试。")
        return
    
    import random
    test_code = str(random.randint(100000, 999999))
    
    print(f"\n正在发送测试邮件到 {test_email}...")
    print(f"测试验证码: {test_code}")
    
    success, message = email_service.send_password_reset_email(test_email, test_code)
    
    if success:
        print(f"\n[成功] {message}")
        print("请检查您的邮箱（包括垃圾邮件文件夹）")
    else:
        print(f"\n[失败] {message}")
        print("\n故障排除建议:")
        print("1. 检查网络连接")
        print("2. 确认授权码正确")
        print("3. 检查SMTP服务器和端口")
        print("4. 查看 '邮件配置说明.md' 获取更多帮助")

if __name__ == "__main__":
    main()
