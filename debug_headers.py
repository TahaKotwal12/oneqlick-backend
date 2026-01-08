import requests

# Test a simple endpoint
response = requests.get("http://localhost:8000/api/v1/restaurants/nearby?latitude=19.0760&longitude=72.8777")

print("Status Code:", response.status_code)
print("\nAll Response Headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")

print("\nRate Limit Headers:")
print(f"  X-RateLimit-Limit: {response.headers.get('X-RateLimit-Limit', 'NOT FOUND')}")
print(f"  X-RateLimit-Remaining: {response.headers.get('X-RateLimit-Remaining', 'NOT FOUND')}")
print(f"  X-RateLimit-Reset: {response.headers.get('X-RateLimit-Reset', 'NOT FOUND')}")

# Check rate limit status
print("\n" + "="*60)
status_response = requests.get("http://localhost:8000/api/v1/rate-limit/status")
print("Rate Limit Status:")
print(status_response.json())
