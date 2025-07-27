import os
from typing import Optional, Tuple
from app.config.logger import get_logger

class SMSService:
    def __init__(self):
        self.logger = get_logger(__name__)
        self.twilio_account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.use_mock_sms = os.getenv('USE_MOCK_SMS', 'true').lower() == 'true'
        
        # Initialize Twilio client if credentials are available
        self.twilio_client = None
        if not self.use_mock_sms and self.twilio_account_sid and self.twilio_auth_token:
            try:
                from twilio.rest import Client
                self.twilio_client = Client(self.twilio_account_sid, self.twilio_auth_token)
                self.logger.info("Twilio client initialized successfully")
            except ImportError:
                self.logger.warning("Twilio library not installed. Using mock SMS.")
                self.use_mock_sms = True
            except Exception as e:
                self.logger.error(f"Error initializing Twilio client: {str(e)}")
                self.use_mock_sms = True

    def send_otp_sms(self, phone_number: str, otp: str) -> Tuple[bool, str]:
        """
        Send OTP via SMS.
        Returns (success, message)
        """
        try:
            if self.use_mock_sms:
                return self._send_mock_sms(phone_number, otp)
            else:
                return self._send_twilio_sms(phone_number, otp)
        except Exception as e:
            self.logger.error(f"Error sending SMS to {phone_number}: {str(e)}")
            return False, f"Error sending SMS: {str(e)}"

    def _send_twilio_sms(self, phone_number: str, otp: str) -> Tuple[bool, str]:
        """Send SMS using Twilio."""
        try:
            if not self.twilio_client:
                return False, "Twilio client not initialized"

            message = self.twilio_client.messages.create(
                body=f"Your OneQlick verification code is: {otp}. Valid for 5 minutes.",
                from_=self.twilio_phone_number,
                to=phone_number
            )
            
            self.logger.info(f"Twilio SMS sent successfully to {phone_number}. SID: {message.sid}")
            return True, f"SMS sent successfully. SID: {message.sid}"
            
        except Exception as e:
            self.logger.error(f"Twilio SMS error for {phone_number}: {str(e)}")
            return False, f"Twilio SMS error: {str(e)}"

    def _send_mock_sms(self, phone_number: str, otp: str) -> Tuple[bool, str]:
        """Send mock SMS (for development/testing)."""
        try:
            # In development, just log the OTP
            self.logger.info(f"📱 MOCK SMS to {phone_number}: Your OneQlick verification code is: {otp}")
            
            # You can also print to console for easy testing
            print(f"\n{'='*50}")
            print(f"📱 MOCK SMS SENT")
            print(f"To: {phone_number}")
            print(f"Message: Your OneQlick verification code is: {otp}")
            print(f"Valid for: 5 minutes")
            print(f"{'='*50}\n")
            
            return True, "Mock SMS sent successfully"
            
        except Exception as e:
            self.logger.error(f"Mock SMS error for {phone_number}: {str(e)}")
            return False, f"Mock SMS error: {str(e)}"

    def validate_phone_number(self, phone_number: str) -> bool:
        """Basic phone number validation."""
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone_number))
        
        # Check if it's a valid length (7-15 digits)
        if len(digits_only) < 7 or len(digits_only) > 15:
            return False
            
        return True

    def format_phone_number(self, phone_number: str) -> str:
        """Format phone number for SMS sending."""
        # Remove all non-digit characters
        digits_only = ''.join(filter(str.isdigit, phone_number))
        
        # Add country code if not present (assuming +1 for US/Canada)
        if len(digits_only) == 10:
            return f"+1{digits_only}"
        elif len(digits_only) == 11 and digits_only.startswith('1'):
            return f"+{digits_only}"
        else:
            return f"+{digits_only}" 