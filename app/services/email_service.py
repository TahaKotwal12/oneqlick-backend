import logging
from typing import Optional, Dict, Any
from app.config.config import EMAIL_CONFIG
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import os

logger = logging.getLogger(__name__)

class EmailService:
    """Email service for sending OTP and other emails using SMTP"""
    
    def __init__(self):
        self.config = EMAIL_CONFIG
        self._validate_smtp_config()
    
    def _validate_smtp_config(self):
        """Validate SMTP configuration"""
        if self.config.get("smtp_host") and self.config.get("smtp_username"):
            logger.info("SMTP configuration loaded successfully")
        else:
            logger.warning("SMTP configuration incomplete - emails will be logged instead")
    
    def send_otp_email(
        self, 
        to_email: str, 
        otp_code: str, 
        user_name: str = "User",
        otp_type: str = "email_verification"
    ) -> bool:
        """Send OTP email to user"""
        try:
            # Generate email content
            subject, html_content, _ = self._generate_otp_email_content(
                otp_code, user_name, otp_type
            )
            
            # Use SMTP directly
            return self._send_with_smtp(to_email, subject, html_content)
                
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
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #1F2937; margin: 0; padding: 0; background-color: #F8FAFC; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #4F46E5, #6366F1); color: white; padding: 40px 30px; text-align: center; border-radius: 12px 12px 0 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
                .content { background: #FFFFFF; padding: 40px 30px; border-radius: 0 0 12px 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
                .otp-code { background: #F8FAFC; border: 2px dashed #4F46E5; padding: 30px; text-align: center; margin: 30px 0; border-radius: 12px; box-shadow: 0 2px 4px -1px rgba(79, 70, 229, 0.1); }
                .otp-number { font-size: 36px; font-weight: 700; color: #4F46E5; letter-spacing: 8px; font-family: 'Courier New', monospace; }
                .footer { text-align: center; margin-top: 40px; color: #6B7280; font-size: 14px; }
                .button { display: inline-block; background: linear-gradient(135deg, #4F46E5, #6366F1); color: white; padding: 14px 28px; text-decoration: none; border-radius: 8px; margin: 15px 0; font-weight: 600; box-shadow: 0 2px 4px -1px rgba(79, 70, 229, 0.3); }
                .warning { background: #FEF3C7; border: 1px solid #F59E0B; color: #92400E; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #F59E0B; }
                .success-badge { background: #D1FAE5; color: #065F46; padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 600; display: inline-block; margin-bottom: 20px; }
                .brand-logo { font-size: 28px; font-weight: 800; margin-bottom: 10px; }
                .subtitle { font-size: 16px; opacity: 0.9; margin: 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="brand-logo">oneQlick</div>
                    <p class="subtitle">{{ subject }}</p>
                </div>
                <div class="content">
                    <div class="success-badge">🔐 Secure Verification</div>
                    
                    <p>Hello <strong>{{ user_name }}</strong>,</p>
                    
                    <p>You requested a verification code for {{ purpose }}. Use the code below to {{ action }}:</p>
                    
                    <div class="otp-code">
                        <div class="otp-number">{{ otp_code }}</div>
                        <p style="margin: 15px 0 0 0; color: #6B7280; font-size: 14px; font-weight: 500;">Your verification code</p>
                    </div>
                    
                    <p><strong style="color: #1F2937;">Important:</strong></p>
                    <ul style="color: #4B5563; line-height: 1.8;">
                        <li>This code will expire in <strong style="color: #EF4444;">10 minutes</strong></li>
                        <li>Do not share this code with anyone</li>
                        <li>If you didn't request this code, please ignore this email</li>
                    </ul>
                    
                    <div class="warning">
                        <strong>🛡️ Security Notice:</strong> oneQlick will never ask for your verification code via phone, email, or any other method. Keep this code confidential.
                    </div>
                    
                    <p style="color: #6B7280;">If you're having trouble, please contact our support team.</p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong style="color: #4F46E5;">The oneQlick Team</strong></p>
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
    
    def _send_with_smtp(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str
    ) -> bool:
        """Send email using SMTP"""
        try:
            # Check if SMTP is configured
            if not self.config.get("smtp_host") or not self.config.get("smtp_username"):
                logger.warning("SMTP not configured, logging email instead")
                logger.info("=== OTP EMAIL (SMTP Not Configured) ===")
                logger.info(f"To: {to_email}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {html_content}")
                logger.info("=====================================")
                return True
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["smtp_username"]
            msg['To'] = to_email
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
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
            logger.info(f"Content: {html_content}")
            logger.info("=====================================")
            return False
    
    def send_welcome_email(
        self, 
        to_email: str, 
        user_name: str,
        first_name: str = "User"
    ) -> bool:
        """Send welcome email to new users"""
        try:
            # Generate email content
            subject, html_content, _ = self._generate_welcome_email_content(
                user_name, first_name
            )
            
            # Use SMTP directly
            return self._send_welcome_with_smtp(to_email, subject, html_content)
                
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
                body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; line-height: 1.6; color: #1F2937; margin: 0; padding: 0; background-color: #F8FAFC; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #4F46E5, #6366F1); color: white; padding: 50px 40px; text-align: center; border-radius: 16px 16px 0 0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
                .content { background: #FFFFFF; padding: 50px 40px; border-radius: 0 0 16px 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
                .feature { background: #F8FAFC; padding: 25px; margin: 20px 0; border-radius: 12px; border-left: 4px solid #4F46E5; box-shadow: 0 2px 4px -1px rgba(79, 70, 229, 0.1); }
                .cta-button { display: inline-block; background: linear-gradient(135deg, #4F46E5, #6366F1); color: white; padding: 16px 32px; text-decoration: none; border-radius: 12px; margin: 25px 0; font-weight: 600; box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.3); }
                .footer { text-align: center; margin-top: 40px; color: #6B7280; font-size: 14px; }
                .emoji { font-size: 28px; margin-right: 15px; }
                .highlight { background: #D1FAE5; border: 1px solid #10B981; color: #065F46; padding: 20px; border-radius: 12px; margin: 25px 0; border-left: 4px solid #10B981; }
                .brand-logo { font-size: 32px; font-weight: 800; margin-bottom: 15px; }
                .subtitle { font-size: 18px; opacity: 0.9; margin: 0; }
                .feature-title { color: #1F2937; font-weight: 600; font-size: 16px; margin-bottom: 8px; }
                .feature-desc { color: #6B7280; font-size: 14px; margin: 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="brand-logo">oneQlick</div>
                    <p class="subtitle">Your Food Journey Starts Here</p>
                </div>
                <div class="content">
                    <p>Hello <strong>{{ first_name }}</strong>,</p>
                    
                    <p>🎉 <strong>Congratulations!</strong> Your account has been successfully created and verified. We're thrilled to have you join the oneQlick family!</p>
                    
                    <div class="highlight">
                        <strong>🎁 Special Welcome Offer:</strong> Get 20% off your first order! Use code <strong>WELCOME20</strong> at checkout.
                    </div>
                    
                    <h3 style="color: #1F2937; margin-top: 40px;">What you can do now:</h3>
                    
                    <div class="feature">
                        <span class="emoji">🍕</span>
                        <div class="feature-title">Explore Restaurants</div>
                        <div class="feature-desc">Browse thousands of restaurants and cuisines in your area</div>
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">📱</span>
                        <div class="feature-title">Easy Ordering</div>
                        <div class="feature-desc">Order your favorite food with just a few taps</div>
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">🚚</span>
                        <div class="feature-title">Real-time Tracking</div>
                        <div class="feature-desc">Track your orders from kitchen to your doorstep</div>
                    </div>
                    
                    <div class="feature">
                        <span class="emoji">⭐</span>
                        <div class="feature-title">Loyalty Rewards</div>
                        <div class="feature-desc">Earn points with every order and unlock exclusive benefits</div>
                    </div>
                    
                    <div style="text-align: center; margin: 40px 0;">
                        <a href="#" class="cta-button">Start Ordering Now</a>
                    </div>
                    
                    <h3 style="color: #1F2937; margin-top: 40px;">Need Help?</h3>
                    <p style="color: #6B7280;">Our support team is here to help you 24/7. If you have any questions or need assistance, don't hesitate to reach out!</p>
                    
                    <p style="margin-top: 30px;">Happy ordering and welcome to the oneQlick family! 🎉</p>
                    
                    <p style="margin-top: 30px;">Best regards,<br><strong style="color: #4F46E5;">The oneQlick Team</strong></p>
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
    
    def _send_welcome_with_smtp(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str
    ) -> bool:
        """Send welcome email using SMTP"""
        try:
            # Check if SMTP is configured
            if not self.config.get("smtp_host") or not self.config.get("smtp_username"):
                logger.warning("SMTP not configured, logging welcome email instead")
                logger.info("=== WELCOME EMAIL (SMTP Not Configured) ===")
                logger.info(f"To: {to_email}")
                logger.info(f"Subject: {subject}")
                logger.info(f"Content: {html_content}")
                logger.info("=======================================")
                return True
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.config["smtp_username"]
            msg['To'] = to_email
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html', 'utf-8')
            msg.attach(html_part)
            
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
            logger.info(f"Content: {html_content}")
            logger.info("=======================================")
            return False

# Global email service instance
email_service = EmailService()
