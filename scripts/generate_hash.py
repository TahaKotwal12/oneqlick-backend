import bcrypt

# Generate a new bcrypt hash for "Test@123"
password = "Test@123"
salt = bcrypt.gensalt(rounds=12)
hashed = bcrypt.hashpw(password.encode('utf-8'), salt)

print(f"Password: {password}")
print(f"Bcrypt Hash: {hashed.decode('utf-8')}")
print()

# Verify it works
if bcrypt.checkpw(password.encode('utf-8'), hashed):
    print("✅ Hash verification successful!")
else:
    print("❌ Hash verification failed!")

print()
print("Use this hash in your SQL script:")
print(f"'{hashed.decode('utf-8')}'")
