import random
import string
from datetime import datetime, timedelta
from typing import Optional, Tuple
from app.config.logger import get_logger
import redis
import json

class OTPService:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client
        self.logger = get_logger(__name__)
        self.otp_expiry_minutes = 5  # OTP expires in 5 minutes
        self.max_attempts = 3  # Maximum verification attempts

    def generate_otp(self, length: int = 6) -> str:
        """Generate a random OTP of specified length."""
        return ''.join(random.choices(string.digits, k=length))

    def store_otp(self, phone: str, otp: str) -> bool:
        """Store OTP in Redis with expiry time."""
        try:
            otp_data = {
                'otp': otp,
                'attempts': 0,
                'created_at': datetime.utcnow().isoformat(),
                'expires_at': (datetime.utcnow() + timedelta(minutes=self.otp_expiry_minutes)).isoformat()
            }
            
            key = f"otp:{phone}"
            self.redis_client.setex(
                key, 
                self.otp_expiry_minutes * 60,  # Convert to seconds
                json.dumps(otp_data)
            )
            
            self.logger.info(f"OTP stored for phone: {phone}")
            return True
        except Exception as e:
            self.logger.error(f"Error storing OTP for {phone}: {str(e)}")
            return False

    def get_otp_data(self, phone: str) -> Optional[dict]:
        """Retrieve OTP data from Redis."""
        try:
            key = f"otp:{phone}"
            data = self.redis_client.get(key)
            if data:
                return json.loads(data)
            return None
        except Exception as e:
            self.logger.error(f"Error retrieving OTP for {phone}: {str(e)}")
            return None

    def verify_otp(self, phone: str, provided_otp: str) -> Tuple[bool, str]:
        """
        Verify OTP for given phone number.
        Returns (is_valid, message)
        """
        try:
            otp_data = self.get_otp_data(phone)
            if not otp_data:
                return False, "OTP expired or not found"

            # Check if OTP is expired
            expires_at = datetime.fromisoformat(otp_data['expires_at'])
            if datetime.utcnow() > expires_at:
                self.delete_otp(phone)
                return False, "OTP has expired"

            # Check attempts limit
            if otp_data['attempts'] >= self.max_attempts:
                self.delete_otp(phone)
                return False, "Maximum verification attempts exceeded"

            # Increment attempts
            otp_data['attempts'] += 1
            self.update_otp_attempts(phone, otp_data['attempts'])

            # Verify OTP
            if otp_data['otp'] == provided_otp:
                self.delete_otp(phone)  # Clear OTP after successful verification
                self.logger.info(f"OTP verified successfully for phone: {phone}")
                return True, "OTP verified successfully"
            else:
                if otp_data['attempts'] >= self.max_attempts:
                    self.delete_otp(phone)
                    return False, "Maximum verification attempts exceeded"
                return False, f"Invalid OTP. {self.max_attempts - otp_data['attempts']} attempts remaining"

        except Exception as e:
            self.logger.error(f"Error verifying OTP for {phone}: {str(e)}")
            return False, "Error verifying OTP"

    def update_otp_attempts(self, phone: str, attempts: int) -> bool:
        """Update the number of attempts for an OTP."""
        try:
            otp_data = self.get_otp_data(phone)
            if otp_data:
                otp_data['attempts'] = attempts
                key = f"otp:{phone}"
                self.redis_client.setex(
                    key,
                    self.otp_expiry_minutes * 60,
                    json.dumps(otp_data)
                )
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error updating OTP attempts for {phone}: {str(e)}")
            return False

    def delete_otp(self, phone: str) -> bool:
        """Delete OTP from Redis."""
        try:
            key = f"otp:{phone}"
            self.redis_client.delete(key)
            self.logger.info(f"OTP deleted for phone: {phone}")
            return True
        except Exception as e:
            self.logger.error(f"Error deleting OTP for {phone}: {str(e)}")
            return False

    def is_otp_request_allowed(self, phone: str) -> Tuple[bool, str]:
        """
        Check if OTP request is allowed (rate limiting).
        Returns (is_allowed, message)
        """
        try:
            key = f"otp_request:{phone}"
            last_request = self.redis_client.get(key)
            
            if last_request:
                last_request_time = datetime.fromisoformat(last_request.decode())
                time_diff = datetime.utcnow() - last_request_time
                
                # Allow only 1 request per minute
                if time_diff.total_seconds() < 60:
                    remaining_seconds = 60 - int(time_diff.total_seconds())
                    return False, f"Please wait {remaining_seconds} seconds before requesting another OTP"
            
            return True, "OTP request allowed"
        except Exception as e:
            self.logger.error(f"Error checking OTP request allowance for {phone}: {str(e)}")
            return True, "OTP request allowed"  # Allow in case of error

    def record_otp_request(self, phone: str) -> bool:
        """Record OTP request timestamp for rate limiting."""
        try:
            key = f"otp_request:{phone}"
            self.redis_client.setex(key, 60, datetime.utcnow().isoformat())  # 1 minute expiry
            return True
        except Exception as e:
            self.logger.error(f"Error recording OTP request for {phone}: {str(e)}")
            return False 