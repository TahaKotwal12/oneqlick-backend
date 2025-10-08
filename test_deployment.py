#!/usr/bin/env python3
"""
Test script to verify the deployment configuration works locally.
Run this before deploying to Vercel.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        print("Testing imports...")
        
        # Test core imports
        import fastapi
        print("✅ FastAPI imported successfully")
        
        import psycopg2
        print("✅ psycopg2 imported successfully")
        
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
        
        import uvicorn
        print("✅ Uvicorn imported successfully")
        
        import redis
        print("✅ Redis imported successfully")
        
        import pydantic
        print("✅ Pydantic imported successfully")
        
        import bcrypt
        print("✅ bcrypt imported successfully")
        
        # Test app imports
        from app.main import app
        print("✅ App imported successfully")
        
        from app.infra.db.postgres.models.pending_user import PendingUser
        print("✅ PendingUser model imported successfully")
        
        from app.utils.pending_user_utils import PendingUserUtils
        print("✅ PendingUserUtils imported successfully")
        
        print("\n🎉 All imports successful! Ready for deployment.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_database_connection():
    """Test database connection."""
    try:
        print("\nTesting database connection...")
        from app.infra.db.postgres.postgres_config import get_db
        from app.config.config import DATABASE_URL
        
        print(f"Database URL: {DATABASE_URL[:50]}...")
        
        # Try to get a database session
        db = next(get_db())
        print("✅ Database connection successful")
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing deployment configuration...\n")
    
    # Test imports
    imports_ok = test_imports()
    
    # Test database connection
    db_ok = test_database_connection()
    
    if imports_ok and db_ok:
        print("\n✅ All tests passed! Ready for Vercel deployment.")
        return 0
    else:
        print("\n❌ Some tests failed. Fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
