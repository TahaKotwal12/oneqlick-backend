#!/usr/bin/env python3
"""
Generate secure random secrets for OneQlick Backend
Run this script to generate production-ready secret keys
"""

import secrets
import string

def generate_secret_key(length=64):
    """Generate a secure random secret key."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_hex_key(length=32):
    """Generate a secure random hex key."""
    return secrets.token_hex(length)

def main():
    print("=" * 70)
    print("OneQlick Backend - Secret Key Generator")
    print("=" * 70)
    print()
    print("Copy these values to your .env file:")
    print()
    print("-" * 70)
    print(f"SECRET_KEY={generate_secret_key()}")
    print()
    print(f"JWT_SECRET_KEY={generate_hex_key()}")
    print("-" * 70)
    print()
    print("⚠️  IMPORTANT: Keep these keys secure and never commit them to git!")
    print()

if __name__ == "__main__":
    main()
