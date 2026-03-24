"""
SMS Service for sending OTP and notifications via Twilio.
Mirrors the pattern of email_service.py.
"""

import logging
from typing import Optional

from app.config.config import NOTIFICATION_CONFIG

logger = logging.getLogger(__name__)


class SMSService:
    """Service for sending SMS messages via Twilio."""

    def __init__(self):
        self._client = None
        self._from_number: str = NOTIFICATION_CONFIG.get("twilio_phone_number", "")
        self._account_sid: str = NOTIFICATION_CONFIG.get("twilio_account_sid", "")
        self._api_key_sid: str = NOTIFICATION_CONFIG.get("twilio_api_key_sid", "")
        self._api_key_secret: str = NOTIFICATION_CONFIG.get("twilio_api_key_secret", "")
        self._auth_token: str = NOTIFICATION_CONFIG.get("twilio_auth_token", "")

    def _get_client(self):
        """Lazily initialise the Twilio client (uses API Key auth if available,
        falls back to Account SID + Auth Token)."""
        if self._client is None:
            try:
                from twilio.rest import Client  # type: ignore

                if self._api_key_sid and self._api_key_secret and self._account_sid:
                    # Preferred: API Key authentication (more secure, rotatable)
                    self._client = Client(
                        self._api_key_sid,
                        self._api_key_secret,
                        account_sid=self._account_sid,
                    )
                    logger.info("Twilio client initialised with API Key authentication")
                elif self._account_sid and self._auth_token:
                    # Fallback: Account SID + Auth Token
                    self._client = Client(self._account_sid, self._auth_token)
                    logger.info("Twilio client initialised with Account SID + Auth Token")
                else:
                    logger.error(
                        "Twilio credentials not configured. "
                        "Set TWILIO_ACCOUNT_SID, TWILIO_API_KEY_SID, "
                        "TWILIO_API_KEY_SECRET in your environment."
                    )
            except ImportError:
                logger.error("Twilio package is not installed. Run: pip install twilio")
        return self._client

    def _format_e164(self, phone: str) -> str:
        """Ensure the phone number is in E.164 format (+<country_code><number>).
        If it already starts with '+', it's returned as-is."""
        phone = phone.strip().replace(" ", "").replace("-", "")
        if not phone.startswith("+"):
            # Default assumption: prepend India country code for bare 10-digit numbers
            # The frontend PhoneNumberInput should always send E.164 format, so
            # this is only a safety fallback.
            if len(phone) == 10:
                phone = f"+91{phone}"
            else:
                logger.warning(
                    f"Phone number '{phone}' is not in E.164 format and could not be auto-corrected. "
                    "Ensure the frontend sends country code with the phone number."
                )
        return phone

    async def send_otp_sms(
        self,
        to_phone: str,
        otp_code: str,
        user_name: Optional[str] = None,
    ) -> bool:
        """Send an OTP verification SMS via Twilio.

        Args:
            to_phone: Recipient phone number (E.164 format preferred).
            otp_code: The 6-digit OTP code to send.
            user_name: Optional user name (for logging only, not in message body).

        Returns:
            True if the message was accepted by Twilio, False otherwise.
        """
        client = self._get_client()
        if not client:
            logger.error("Twilio client not available — SMS not sent")
            return False

        if not self._from_number:
            logger.error("TWILIO_PHONE_NUMBER is not configured — SMS not sent")
            return False

        to_e164 = self._format_e164(to_phone)

        # Keep the message body under 160 characters to avoid multi-part SMS charges
        message_body = (
            f"[oneQlick] Your verification code is {otp_code}. "
            f"Valid for 10 minutes. Do not share this code with anyone."
        )

        try:
            message = client.messages.create(
                body=message_body,
                from_=self._from_number,
                to=to_e164,
            )

            logger.info(
                f"OTP SMS sent successfully to {to_e164}"
                f"{' for ' + user_name if user_name else ''}. "
                f"Twilio SID: {message.sid}"
            )
            return True

        except Exception as exc:
            logger.error(
                f"Failed to send OTP SMS to {to_e164}: {exc}"
            )
            return False

    async def send_generic_sms(self, to_phone: str, body: str) -> bool:
        """Send a generic SMS message via Twilio (for future use).

        Args:
            to_phone: Recipient phone number (E.164 format preferred).
            body: The SMS message body (max 160 chars to avoid split SMS).

        Returns:
            True if accepted, False otherwise.
        """
        client = self._get_client()
        if not client or not self._from_number:
            logger.error("Twilio client/number not configured — SMS not sent")
            return False

        to_e164 = self._format_e164(to_phone)
        try:
            message = client.messages.create(
                body=body[:160],  # Hard-cap to avoid multi-part SMS
                from_=self._from_number,
                to=to_e164,
            )
            logger.info(f"Generic SMS sent to {to_e164}. SID: {message.sid}")
            return True
        except Exception as exc:
            logger.error(f"Failed to send generic SMS to {to_e164}: {exc}")
            return False


# Singleton instance — import and use this throughout the app
sms_service = SMSService()
