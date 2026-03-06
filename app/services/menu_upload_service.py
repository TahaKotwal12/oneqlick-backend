import pandas as pd
import io
from typing import List, Dict, Tuple
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.category import Category
from app.config.logger import get_logger

logger = get_logger(__name__)

class MenuUploadService:
    @staticmethod
    def process_upload(db: Session, file_contents: bytes, extension: str, restaurant_id: UUID) -> Dict:
        try:
            # 1. Load data into Pandas
            if extension == 'csv':
                df = pd.read_csv(io.BytesIO(file_contents))
            else:
                df = pd.read_excel(io.BytesIO(file_contents))

            # 2. Basic Validations
            required_columns = ['name', 'category_name', 'price']
            missing = [col for col in required_columns if col not in df.columns]
            if missing:
                return {"success": False, "message": f"Missing columns: {', '.join(missing)}"}

            stats = {"total": len(df), "created": 0, "skipped": 0, "errors": 0, "details": []}

            for index, row in df.iterrows():
                try:
                    name = str(row['name']).strip()
                    cat_name = str(row['category_name']).strip()
                    price = Decimal(str(row['price']))

                    if not name or not cat_name:
                        stats["errors"] += 1
                        continue

                    # 3. Check if Item Already Exists (Requirement)
                    existing = db.query(FoodItem).filter(
                        FoodItem.restaurant_id == restaurant_id,
                        FoodItem.name == name
                    ).first()

                    if existing:
                        stats["skipped"] += 1
                        stats["details"].append(f"Row {index+2}: '{name}' already exists. Skipped.")
                        continue

                    # 4. Get or Create Category
                    category = db.query(Category).filter(Category.name.ilike(cat_name)).first()
                    if not category:
                        category = Category(name=cat_name, is_active=True)
                        db.add(category)
                        db.flush() # Get ID

                    # 5. Create Food Item
                    new_item = FoodItem(
                        restaurant_id=restaurant_id,
                        category_id=category.category_id,
                        name=name,
                        price=price,
                        description=str(row.get('description', '')) if pd.notna(row.get('description')) else None,
                        is_veg=str(row.get('is_veg', 'true')).lower() in ['true', '1', 'yes'],
                        prep_time=int(row.get('prep_time', 0)) if pd.notna(row.get('prep_time')) else None,
                        status='available'
                    )
                    db.add(new_item)
                    stats["created"] += 1

                except Exception as e:
                    stats["errors"] += 1
                    stats["details"].append(f"Row {index+2}: Error - {str(e)}")

            db.commit()
            return {
                "success": True, 
                "message": f"Processed {stats['total']} items",
                "data": stats
            }

        except Exception as e:
            db.rollback()
            logger.error(f"Upload failed: {str(e)}")
            return {"success": False, "message": str(e)}
