#!/usr/bin/env python3

import os
from app.domain.services.sms_service import SMSService

def test_twilio_setup():
    """Test if Twilio is properly configured."""
    print("Testing Twilio Setup...")
    print("=" * 50)
    
    # Check environment variables
    print(f"USE_MOCK_SMS: {os.getenv('USE_MOCK_SMS', 'Not set')}")
    print(f"TWILIO_ACCOUNT_SID: {os.getenv('TWILIO_ACCOUNT_SID', 'Not set')}")
    print(f"TWILIO_AUTH_TOKEN: {'Set' if os.getenv('TWILIO_AUTH_TOKEN') else 'Not set'}")
    print(f"TWILIO_PHONE_NUMBER: {os.getenv('TWILIO_PHONE_NUMBER', 'Not set')}")
    
    # Test SMS service
    print("\nTesting SMS Service...")
    sms_service = SMSService()
    
    print(f"Using Mock SMS: {sms_service.use_mock_sms}")
    print(f"Twilio Client: {'Initialized' if sms_service.twilio_client else 'Not initialized'}")
    
    # Test phone validation
    test_phone = "+1234567890"
    is_valid = sms_service.validate_phone_number(test_phone)
    print(f"Phone validation for {test_phone}: {is_valid}")
    
    # Test SMS sending (this will show which method is used)
    print("\nTesting SMS sending...")
    success, message = sms_service.send_otp_sms(test_phone, "123456")
    print(f"SMS Result: {success}")
    print(f"SMS Message: {message}")

if __name__ == "__main__":
    test_twilio_setup() 