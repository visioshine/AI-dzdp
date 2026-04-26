#!/usr/bin/env python3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from .config import EmailConfig

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        # 从配置文件加载SMTP服务器配置
        self.smtp_server = EmailConfig.SMTP_SERVER
        self.smtp_port = EmailConfig.SMTP_PORT
        self.smtp_username = EmailConfig.SMTP_USERNAME
        self.smtp_password = EmailConfig.SMTP_PASSWORD
        self.sender_email = EmailConfig.SENDER_EMAIL
        self.enabled = EmailConfig.ENABLE_EMAIL_SENDING and EmailConfig.is_configured()
    
    def send_password_reset_email(self, to_email, verification_code):
        """发送密码重置邮件"""
        subject = "大众点评系统 - 密码重置验证码"
        
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background: linear-gradient(135deg, #ff6b35, #f7931e); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                    .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                    .code-box {{ background: white; border: 2px dashed #ff6b35; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }}
                    .code {{ font-size: 36px; font-weight: bold; color: #ff6b35; letter-spacing: 10px; }}
                    .note {{ color: #666; font-size: 14px; margin-top: 20px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 密码重置</h1>
                    </div>
                    <div class="content">
                        <p>您好！</p>
                        <p>您正在申请重置大众点评系统的密码，请使用以下验证码：</p>
                        
                        <div class="code-box">
                            <div class="code">{verification_code}</div>
                        </div>
                        
                        <p class="note">
                            ⚠️ 此验证码将在15分钟后失效<br>
                            如果这不是您本人的操作，请忽略此邮件
                        </p>
                        
                        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee; text-align: center; color: #999; font-size: 12px;">
                            此邮件由系统自动发送，请勿回复
                        </div>
                    </div>
                </div>
            </body>
        </html>
        """
        
        return self._send_email(to_email, subject, html_content, is_html=True)
    
    def _send_email(self, to_email, subject, content, is_html=False):
        """发送邮件的通用方法"""
        if not self.enabled:
            logger.info(f"邮件服务未启用，模拟发送邮件到: {to_email}")
            return True, "邮件服务未启用，已模拟发送"
        
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(content, 'html', 'utf-8'))
            else:
                msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            logger.info(f"正在连接SMTP服务器: {self.smtp_server}:{self.smtp_port}")
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                logger.info(f"正在登录: {self.smtp_username}")
                server.login(self.smtp_username, self.smtp_password)
                
                logger.info(f"正在发送邮件到: {to_email}")
                server.send_message(msg)
            
            logger.info(f"邮件发送成功: {to_email}")
            return True, "邮件发送成功"
            
        except smtplib.SMTPAuthenticationError:
            error_msg = "SMTP认证失败，请检查用户名和密码"
            logger.error(error_msg)
            return False, error_msg
        except smtplib.SMTPConnectError:
            error_msg = "无法连接到SMTP服务器"
            logger.error(error_msg)
            return False, error_msg
        except Exception as e:
            error_msg = f"邮件发送失败: {str(e)}"
            logger.error(error_msg)
            return False, error_msg

# 创建全局实例
email_service = EmailService()

def send_password_reset_email(to_email, verification_code):
    """便捷函数：发送密码重置邮件"""
    return email_service.send_password_reset_email(to_email, verification_code)
