import logging
from typing import Optional, Dict, Any
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config.config import EMAIL_CONFIG
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending OTP and other emails"""
    
    def __init__(self):
        self.config = EMAIL_CONFIG
        self.fastmail = None
        self._setup_fastmail()
    
    def _setup_fastmail(self):
        """Setup FastMail configuration"""
        try:
            if self.config.get("smtp_host") and self.config.get("smtp_username"):
                conf = ConnectionConfig(
                    MAIL_USERNAME=self.config["smtp_username"],
                    MAIL_PASSWORD=self.config["smtp_password"],
                    MAIL_FROM=self.config["smtp_username"],
                    MAIL_PORT=self.config["smtp_port"],
                    MAIL_SERVER=self.config["smtp_host"],
                    MAIL_STARTTLS=self.config["smtp_use_tls"],
                    MAIL_SSL_TLS=False,
                    USE_CREDENTIALS=True,
                    VALIDATE_CERTS=True
                )
                self.fastmail = FastMail(conf)
                logger.info("FastMail configured successfully")
            else:
                logger.warning("Email configuration incomplete, using fallback method")
        except Exception as e:
            logger.error(f"Failed to setup FastMail: {e}")
            self.fastmail = None
    
    async def send_otp_email(
        self, 
        to_email: str, 
        otp_code: str, 
        user_name: str = "User",
        otp_type: str = "email_verification"
    ) -> bool:
        """Send OTP email to user"""
        try:
            # Generate email content
            subject, html_content, text_content = self._generate_otp_email_content(
                otp_code, user_name, otp_type
            )
            
            # Try FastMail first
            if self.fastmail:
                return await self._send_with_fastmail(to_email, subject, html_content)
            else:
                # Fallback to SMTP
                return self._send_with_smtp(to_email, subject, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send OTP email: {e}")
            return False
    
    def _generate_otp_email_content(
        self, 
        otp_code: str, 
        user_name: str, 
        otp_type: str
    ) -> tuple[str, str, str]:
        """Generate email content for OTP"""
        
        # Determine email type and content
        if otp_type == "email_verification":
            subject = "Verify Your Email - oneQlick"
            purpose = "email verification"
            action = "verify your email address"
        elif otp_type == "phone_verification":
            subject = "Verify Your Phone - oneQlick"
            purpose = "phone verification"
            action = "verify your phone number"
        elif otp_type == "password_reset":
            subject = "Reset Your Password - oneQlick"
            purpose = "password reset"
            action = "reset your password"
        else:
            subject = "Your Verification Code - oneQlick"
            purpose = "verification"
            action = "complete your verification"
        
        # HTML Template
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ subject }}</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #FF6B35, #F7931E); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .otp-code { background: #fff; border: 2px dashed #FF6B35; padding: 20px; text-align: center; margin: 20px 0; border-radius: 8px; }
                .otp-number { font-size: 32px; font-weight: bold; color: #FF6B35; letter-spacing: 5px; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                .button { display: inline-block; background: #FF6B35; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 10px 0; }
                .warning { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 5px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>oneQlick</h1>
                    <h2>{{ subject }}</h2>
                </div>
                <div class="content">
                    <p>Hello <strong>{{ user_name }}</strong>,</p>
                    
                    <p>You requested a verification code for {{ purpose }}. Use the code below to {{ action }}:</p>
                    
                    <div class="otp-code">
                        <div class="otp-number">{{ otp_code }}</div>
                        <p style="margin: 10px 0 0 0; color: #666;">Your verification code</p>
                    </div>
                    
                    <p><strong>Important:</strong></p>
                    <ul>
                        <li>This code will expire in <strong>10 minutes</strong></li>
                        <li>Do not share this code with anyone</li>
                        <li>If you didn't request this code, please ignore this email</li>
                    </ul>
                    
                    <div class="warning">
                        <strong>Security Notice:</strong> oneQlick will never ask for your verification code via phone, email, or any other method. Keep this code confidential.
                    </div>
                    
                    <p>If you're having trouble, please contact our support team.</p>
                    
                    <p>Best regards,<br>The oneQlick Team</p>
                </div>
                <div class="footer">
                    <p>© 2024 oneQlick. All rights reserved.</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        # Text Template
        text_template = Template("""
        oneQlick - {{ subject }}
        
        Hello {{ user_name }},
        
        You requested a verification code for {{ purpose }}. Use the code below to {{ action }}:
        
        Verification Code: {{ otp_code }}
        
        Important:
        - This code will expire in 10 minutes
        - Do not share this code with anyone
        - If you didn't request this code, please ignore this email
        
        Security Notice: oneQlick will never ask for your verification code via phone, email, or any other method. Keep this code confidential.
        
        If you're having trouble, please contact our support team.
        
        Best regards,
        The oneQlick Team
        
        © 2024 oneQlick. All rights reserved.
        This is an automated message, please do not reply to this email.
        """)
        
        html_content = html_template.render(
            subject=subject,
            user_name=user_name,
            otp_code=otp_code,
            purpose=purpose,
            action=action
        )
        
        text_content = text_template.render(
            subject=subject,
            user_name=user_name,
            otp_code=otp_code,
            purpose=purpose,
            action=action
        )
        
        return subject, html_content, text_content
    
    async def _send_with_fastmail(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str
    ) -> bool:
        """Send email using FastMail"""
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[to_email],
                body=html_content,
                subtype="html"
            )
            await self.fastmail.send_message(message)
            logger.info(f"OTP email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"FastMail send failed: {e}")
            # Fallback to SMTP if FastMail fails
            return self._send_with_smtp(to_email, subject, html_content)
    
    def _send_with_smtp(
        self, 
        to_email: str, 
        subject: str, 
        text_content: str
    ) -> bool:
        """Send email using SMTP fallback"""
        try:
            # Check if SMTP is configured
            if not self.config.get("smtp_host") or not self.config.get("smtp_username"):
                logger.warning("SMTP not configured, logging email instead")
                logger.info("=== OTP EMAIL (SMTP Not Configured) ===")
                logger.info(f"To: {to_email}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {text_content}")
                logger.info("=====================================")
                return True
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["smtp_username"]
            msg['To'] = to_email
            
            # Add text content
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Connect to SMTP server and send
            if self.config["smtp_use_tls"]:
                server = smtplib.SMTP(self.config["smtp_host"], self.config["smtp_port"])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_host"], self.config["smtp_port"])
            
            server.login(self.config["smtp_username"], self.config["smtp_password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"OTP email sent successfully via SMTP to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP send failed: {e}")
            # Log the email content for debugging
            logger.info("=== OTP EMAIL (SMTP Failed - Debug Info) ===")
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Content: {text_content}")
            logger.info("=====================================")
            return False
    
    async def send_welcome_email(
        self, 
        to_email: str, 
        user_name: str,
        first_name: str = "User"
    ) -> bool:
        """Send welcome email to new users"""
        try:
            # Generate email content
            subject, html_content, text_content = self._generate_welcome_email_content(
                user_name, first_name
            )
            
            # Try FastMail first
            if self.fastmail:
                return await self._send_welcome_with_fastmail(to_email, subject, html_content)
            else:
                # Fallback to SMTP
                return self._send_welcome_with_smtp(to_email, subject, text_content)
                
        except Exception as e:
            logger.error(f"Failed to send welcome email: {e}")
            return False
    
    def _generate_welcome_email_content(
        self, 
        user_name: str, 
        first_name: str
    ) -> tuple[str, str, str]:
        """Generate welcome email content"""
        
        subject = "Welcome to oneQlick! 🎉 Your Food Journey Starts Here"
        
        # HTML Template
        html_template = Template("""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to oneQlick</title>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #FF6B35, #F7931E); color: white; padding: 40px; text-align: center; border-radius: 15px 15px 0 0; }
                .content { background: #f9f9f9; padding: 40px; border-radius: 0 0 15px 15px; }
                .feature { background: #fff; padding: 20px; margin: 15px 0; border-radius: 10px; border-left: 4px solid #FF6B35; }
                .cta-button { display: inline-block; background: #FF6B35; color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; font-weight: bold; }
                .footer { text-align: center; margin-top: 30px; color: #666; font-size: 14px; }
                .emoji { font-size: 24px; margin-right: 10px; }
                .highlight { background: #fff3cd; border: 1px solid #ffeaa7; color: #856404; padding: 15px; border-radius: 8px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to oneQlick!</h1>
                    <h2>Your Food Journey Starts Here</h2>
                </div>
                <div class="content">
                    <p>Hello <strong>{{ first_name }}</strong>,</p>
                    
                    <p>🎉 <strong>Congratulations!</strong> Your account has been successfully created and verified. We're thrilled to have you join the oneQlick family!</p>
                    
                    <div class="highlight">
                        <strong>🎁 Special Welcome Offer:</strong> Get 20% off your first order! Use code <strong>WELCOME20</strong> at checkout.
                    </div>
                    
                    <h3>What you can do now:</h3>
                    
                    <div class="feature">
                        <span class="emoji">🍕</span>
                        <strong>Explore Restaurants</strong><br>
                        Browse thousands of restaurants and cuisines in your area
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">📱</span>
                        <strong>Easy Ordering</strong><br>
                        Order your favorite food with just a few taps
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">🚚</span>
                        <strong>Real-time Tracking</strong><br>
                        Track your orders from kitchen to your doorstep
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">⭐</span>
                        <strong>Loyalty Rewards</strong><br>
                        Earn points with every order and unlock exclusive benefits
                    </div>
                    
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="#" class="cta-button">Start Ordering Now</a>
                    </div>
                    
                    <h3>Need Help?</h3>
                    <p>Our support team is here to help you 24/7. If you have any questions or need assistance, don't hesitate to reach out!</p>
                    
                    <p>Happy ordering and welcome to the oneQlick family! 🎉</p>
                    
                    <p>Best regards,<br><strong>The oneQlick Team</strong></p>
                </div>
                <div class="footer">
                    <p>© 2024 oneQlick. All rights reserved.</p>
                    <p>This is an automated message, please do not reply to this email.</p>
                    <p>Follow us on social media for the latest updates and offers!</p>
                </div>
            </div>
        </body>
        </html>
        """)
        
        # Text Template
        text_template = Template("""
        Welcome to oneQlick! 🎉 Your Food Journey Starts Here
        
        Hello {{ first_name }},
        
        🎉 Congratulations! Your account has been successfully created and verified. We're thrilled to have you join the oneQlick family!
        
        🎁 Special Welcome Offer: Get 20% off your first order! Use code WELCOME20 at checkout.
        
        What you can do now:
        
        🍕 Explore Restaurants
           Browse thousands of restaurants and cuisines in your area
        
        📱 Easy Ordering
           Order your favorite food with just a few taps
        
        🚚 Real-time Tracking
           Track your orders from kitchen to your doorstep
        
        ⭐ Loyalty Rewards
           Earn points with every order and unlock exclusive benefits
        
        Need Help?
        Our support team is here to help you 24/7. If you have any questions or need assistance, don't hesitate to reach out!
        
        Happy ordering and welcome to the oneQlick family! 🎉
        
        Best regards,
        The oneQlick Team
        
        © 2024 oneQlick. All rights reserved.
        This is an automated message, please do not reply to this email.
        Follow us on social media for the latest updates and offers!
        """)
        
        html_content = html_template.render(
            first_name=first_name,
            user_name=user_name
        )
        
        text_content = text_template.render(
            first_name=first_name,
            user_name=user_name
        )
        
        return subject, html_content, text_content
    
    async def _send_welcome_with_fastmail(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str
    ) -> bool:
        """Send welcome email using FastMail"""
        try:
            message = MessageSchema(
                subject=subject,
                recipients=[to_email],
                body=html_content,
                subtype="html"
            )
            await self.fastmail.send_message(message)
            logger.info(f"Welcome email sent successfully to {to_email}")
            return True
        except Exception as e:
            logger.error(f"FastMail welcome email send failed: {e}")
            # Fallback to SMTP if FastMail fails
            return self._send_welcome_with_smtp(to_email, subject, html_content)
    
    def _send_welcome_with_smtp(
        self, 
        to_email: str, 
        subject: str, 
        text_content: str
    ) -> bool:
        """Send welcome email using SMTP fallback"""
        try:
            # Check if SMTP is configured
            if not self.config.get("smtp_host") or not self.config.get("smtp_username"):
                logger.warning("SMTP not configured, logging welcome email instead")
                logger.info("=== WELCOME EMAIL (SMTP Not Configured) ===")
                logger.info(f"To: {to_email}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {text_content}")
                logger.info("=======================================")
                return True
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["smtp_username"]
            msg['To'] = to_email
            
            # Add text content
            text_part = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(text_part)
            
            # Connect to SMTP server and send
            if self.config["smtp_use_tls"]:
                server = smtplib.SMTP(self.config["smtp_host"], self.config["smtp_port"])
                server.starttls()
            else:
                server = smtplib.SMTP_SSL(self.config["smtp_host"], self.config["smtp_port"])
            
            server.login(self.config["smtp_username"], self.config["smtp_password"])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Welcome email sent successfully via SMTP to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"SMTP welcome email send failed: {e}")
            # Log the email content for debugging
            logger.info("=== WELCOME EMAIL (SMTP Failed - Debug Info) ===")
            logger.info(f"To: {to_email}")
            logger.info(f"Subject: {subject}")
            logger.info(f"Content: {text_content}")
            logger.info("=======================================")
            return False

# Global email service instance
email_service = EmailService()
