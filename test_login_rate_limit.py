import requests

print("Testing Login Endpoint with Rate Limiting")
print("=" * 60)

# Test login endpoint
for i in range(1, 13):
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json={'identifier': 'test@example.com', 'password': 'Test@123456'}
        )
        
        limit = response.headers.get('X-RateLimit-Limit', 'N/A')
        remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
        
        status_icon = "✓" if response.status_code in [200, 401] else "✗"
        
        print(f"{status_icon} Request {i:2d}: Status {response.status_code} | "
              f"Limit: {limit:4s} | Remaining: {remaining:4s}")
        
        if response.status_code == 429:
            data = response.json()
            print(f"  🛑 Rate limit exceeded!")
            print(f"  Message: {data.get('message', 'N/A')}")
            break
        
    except Exception as e:
        print(f"✗ Request {i:2d}: ERROR - {e}")

print("\n" + "=" * 60)
print("Test complete!")
