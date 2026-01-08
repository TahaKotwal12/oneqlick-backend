import requests
import time

print("Testing Rate Limiting - Restaurant Endpoint (100 req/min)")
print("=" * 70)

# Test with a simple GET endpoint that doesn't require authentication
url = "http://localhost:8000/api/v1/restaurants/nearby"
params = {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "radius_km": 5
}

print(f"\nSending 12 requests to: {url}")
print(f"Expected limit: 100 requests/minute\n")

for i in range(1, 13):
    try:
        response = requests.get(url, params=params)
        
        limit = response.headers.get('X-RateLimit-Limit', 'N/A')
        remaining = response.headers.get('X-RateLimit-Remaining', 'N/A')
        reset = response.headers.get('X-RateLimit-Reset', 'N/A')
        
        status_icon = "✓" if response.status_code == 200 else "✗"
        
        print(f"{status_icon} Request {i:2d}: Status {response.status_code} | "
              f"Limit: {limit:3s} | Remaining: {remaining:3s}")
        
        if response.status_code == 429:
            data = response.json()
            print(f"  🛑 Rate limit exceeded!")
            print(f"  Message: {data.get('message', 'N/A')}")
        
        time.sleep(0.05)
    except Exception as e:
        print(f"✗ Request {i:2d}: ERROR - {e}")

print("\n" + "=" * 70)

# Now test the rate limit status endpoint
print("\nChecking Rate Limit Status Endpoint...")
print("=" * 70)

try:
    response = requests.get("http://localhost:8000/api/v1/rate-limit/status")
    if response.status_code == 200:
        data = response.json()
        print("✓ Rate limiting is ENABLED")
        print(f"  Storage: {data['data']['storage_backend']}")
        print(f"  Global limit: {data['data']['limits']['global_per_hour']} req/hour")
        print(f"  Login limit: {data['data']['limits']['auth_login_per_minute']} req/min")
        print(f"  Public limit: {data['data']['limits']['public_per_minute']} req/min")
        print(f"  Search limit: {data['data']['limits']['search_per_minute']} req/min")
    else:
        print(f"✗ Status endpoint returned: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 70)
print("✓ Rate limiting test complete!")
print("=" * 70)
