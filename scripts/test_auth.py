#!/usr/bin/env python3
"""
Test script for authentication endpoints
"""

import requests
import json
import sys
import random
import time

# API Base URL
BASE_URL = "http://localhost:8000/api/v1"

# Global variable to store test email
test_email = None

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL.replace('/api/v1', '')}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            print(f"   Make sure the backend server is running: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print(f"   Make sure the backend server is running: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        return False

def test_signup():
    """Test user signup"""
    print("\n🔍 Testing user signup...")
    try:
        # Generate unique test data to avoid conflicts
        timestamp = int(time.time())
        random_num = random.randint(1000, 9999)
        
        signup_data = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test{timestamp}{random_num}@example.com",
            "phone": f"+123456{random_num}",
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        
        if response.status_code == 201:
            print("✅ Signup successful")
            data = response.json()
            print(f"   User ID: {data['data']['user']['user_id']}")
            print(f"   Email: {data['data']['user']['email']}")
            # Store the email for login test
            global test_email
            test_email = signup_data["email"]
            return data['data']['tokens']['access_token']
        else:
            print(f"❌ Signup failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Signup error: {e}")
        return None

def test_login():
    """Test user login"""
    print("\n🔍 Testing user login...")
    try:
        # Use the same email from signup or fallback to a test email
        if test_email:
            email = test_email
        else:
            # Fallback to a known test email if signup didn't run
            email = "test@example.com"
        
        login_data = {
            "email": email,
            "password": "testpassword123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        
        if response.status_code == 200:
            print("✅ Login successful")
            data = response.json()
            print(f"   User: {data['data']['user']['first_name']} {data['data']['user']['last_name']}")
            return data['data']['tokens']['access_token']
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None

def test_protected_endpoint(token):
    """Test protected endpoint with token"""
    print("\n🔍 Testing protected endpoint...")
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}/auth/sessions", headers=headers)
        
        if response.status_code == 200:
            print("✅ Protected endpoint access successful")
            data = response.json()
            print(f"   Sessions: {data['data']['total_sessions']}")
            return True
        else:
            print(f"❌ Protected endpoint failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Protected endpoint error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Authentication API Tests\n")
    
    # Test health
    if not test_health():
        print("\n❌ Health check failed, stopping tests")
        return False
    
    # Test signup
    token = test_signup()
    if not token:
        print("\n❌ Signup failed, trying login...")
        token = test_login()
    
    if not token:
        print("\n❌ Both signup and login failed")
        return False
    
    # Test protected endpoint
    if not test_protected_endpoint(token):
        print("\n❌ Protected endpoint test failed")
        return False
    
    print("\n🎉 All tests passed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
