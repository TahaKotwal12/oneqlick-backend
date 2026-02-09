import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.infra.db.postgres.postgres_config import engine
from app.infra.db.postgres.base import Base
from app.infra.db.postgres.models import * 

def create_tables():
    print("Creating database tables...")
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")

if __name__ == "__main__":
    create_tables()
