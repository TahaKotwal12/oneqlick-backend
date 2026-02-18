"""
Twilio SMS Service for OneQlick
Handles sending OTP and other SMS messages via Twilio REST API.
"""
import logging
import re
from typing import Optional

from app.config.config import NOTIFICATION_CONFIG

logger = logging.getLogger(__name__)


def _format_e164(phone: str) -> str:
    """
    Ensure phone number is in E.164 format (+<country_code><number>).
    If it already starts with '+', return as-is (stripped of spaces/dashes).
    If it's a 10-digit Indian number, prepend +91.
    """
    # Remove all spaces, dashes, parentheses
    cleaned = re.sub(r"[\s\-\(\)]", "", phone)

    if cleaned.startswith("+"):
        return cleaned

    # Assume Indian number if 10 digits
    if re.match(r"^\d{10}$", cleaned):
        return f"+91{cleaned}"

    # If already has country code without +
    if re.match(r"^\d{11,15}$", cleaned):
        return f"+{cleaned}"

    return cleaned


class SMSService:
    """Twilio-backed SMS service for sending OTP and notifications."""

    def __init__(self):
        self.account_sid: str = NOTIFICATION_CONFIG.get("twilio_account_sid", "")
        self.auth_token: str = NOTIFICATION_CONFIG.get("twilio_auth_token", "")
        self.api_key_sid: str = NOTIFICATION_CONFIG.get("twilio_api_key_sid", "")
        self.api_key_secret: str = NOTIFICATION_CONFIG.get("twilio_api_key_secret", "")
        self.from_number: str = NOTIFICATION_CONFIG.get("twilio_phone_number", "")
        self._client = None

    def _get_client(self):
        """Lazily initialise the Twilio REST client."""
        if self._client is not None:
            return self._client

        try:
            from twilio.rest import Client  # type: ignore

            if self.api_key_sid and self.api_key_secret and self.account_sid:
                # Preferred: use scoped API Key credentials
                self._client = Client(
                    self.api_key_sid,
                    self.api_key_secret,
                    self.account_sid,
                )
                logger.info("Twilio client initialised with API Key credentials")
            elif self.account_sid and self.auth_token:
                # Fallback: use main Auth Token
                self._client = Client(self.account_sid, self.auth_token)
                logger.info("Twilio client initialised with Auth Token credentials")
            else:
                logger.error(
                    "Twilio credentials not configured. "
                    "Set TWILIO_ACCOUNT_SID + TWILIO_API_KEY_SID + TWILIO_API_KEY_SECRET in .env"
                )
                return None

        except ImportError:
            logger.error(
                "twilio package not installed. Run: pip install twilio==9.3.7"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to initialise Twilio client: {e}")
            return None

        return self._client

    async def send_otp_sms(
        self,
        to_phone: str,
        otp_code: str,
        user_name: str = "",
        expires_minutes: int = 10,
    ) -> bool:
        """
        Send an OTP verification SMS.

        Args:
            to_phone: Destination phone number (any common format).
            otp_code: The 6-digit OTP code to send.
            user_name: Optional recipient name for personalisation.
            expires_minutes: OTP validity window shown in the message.

        Returns:
            True if the SMS was sent successfully, False otherwise.
        """
        greeting = f"Hi {user_name.split()[0]}, " if user_name else ""
        message_body = (
            f"{greeting}Your OneQlick verification code is: {otp_code}. "
            f"Valid for {expires_minutes} minutes. Do not share this code with anyone."
        )
        return await self.send_sms(to_phone=to_phone, message=message_body)

    async def send_sms(self, to_phone: str, message: str) -> bool:
        """
        Send a raw SMS message via Twilio.

        Args:
            to_phone: Destination phone number.
            message: SMS body text.

        Returns:
            True on success, False on failure.
        """
        if not to_phone:
            logger.error("send_sms called with empty phone number")
            return False

        formatted_phone = _format_e164(to_phone)
        logger.info(f"Sending SMS to {formatted_phone}")

        client = self._get_client()
        if client is None:
            logger.error("Twilio client unavailable — SMS not sent")
            return False

        if not self.from_number:
            logger.error("TWILIO_PHONE_NUMBER not configured — SMS not sent")
            return False

        try:
            msg = client.messages.create(
                body=message,
                from_=self.from_number,
                to=formatted_phone,
            )
            logger.info(
                f"SMS sent successfully to {formatted_phone} | SID: {msg.sid} | Status: {msg.status}"
            )
            return True

        except Exception as e:
            # Twilio raises TwilioRestException for API errors
            logger.error(f"Failed to send SMS to {formatted_phone}: {e}")
            return False


# Singleton instance — import this in route handlers
sms_service = SMSService()
