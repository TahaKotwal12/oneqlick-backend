import requests
import time

print("Testing Rate Limiting - Login Endpoint (10 req/min)")
print("=" * 60)

for i in range(1, 13):
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json={'identifier': 'test@example.com', 'password': 'wrongpassword'}
        )
        
        limit = response.headers.get('X-RateLimit-Limit', 'N/A')
        remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
        reset = response.headers.get('X-RateLimit-Reset', 'N/A')
        
        print(f"Request {i:2d}: Status {response.status_code} | "
              f"Limit: {limit} | Remaining: {remaining} | Reset: {reset}")
        
        if response.status_code == 429:
            print(f"  ✓ Rate limit exceeded as expected!")
            print(f"  Response: {response.json()['message']}")
        
        time.sleep(0.1)
    except Exception as e:
        print(f"Request {i:2d}: ERROR - {e}")

print("\n" + "=" * 60)
print("Test complete!")
