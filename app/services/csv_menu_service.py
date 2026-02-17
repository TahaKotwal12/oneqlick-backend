"""
CSV Menu Service for bulk menu item import.
Handles CSV parsing, validation, and bulk creation of menu items.
"""
import csv
import io
from typing import List, Tuple, Dict, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session

from app.infra.db.postgres.models.food_item import FoodItem
from app.infra.db.postgres.models.category import Category
from app.api.schemas.onboarding_schemas import MenuItemImportRow, MenuItemError
from app.config.logger import get_logger

logger = get_logger(__name__)


class CSVMenuService:
    """Service for handling CSV menu imports."""
    
    # CSV template headers
    CSV_HEADERS = [
        'name',
        'category_id',
        'price',
        'description',
        'is_veg',
        'image_url',
        'prep_time'
    ]
    
    @staticmethod
    def generate_csv_template() -> str:
        """
        Generate CSV template with headers and sample data.
        
        Returns:
            str: CSV template content
        """
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write headers
        writer.writerow(CSVMenuService.CSV_HEADERS)
        
        # Write sample rows
        writer.writerow([
            'Paneer Butter Masala',
            '<category-uuid>',
            '250.00',
            'Creamy tomato curry with cottage cheese',
            'true',
            'https://example.com/paneer.jpg',
            '20'
        ])
        writer.writerow([
            'Chicken Biryani',
            '<category-uuid>',
            '300.00',
            'Aromatic rice with tender chicken',
            'false',
            'https://example.com/biryani.jpg',
            '30'
        ])
        
        return output.getvalue()
    
    @staticmethod
    def parse_csv(csv_content: str) -> Tuple[List[MenuItemImportRow], List[MenuItemError]]:
        """
        Parse CSV content into menu item rows.
        
        Args:
            csv_content: Raw CSV content as string
            
        Returns:
            Tuple[List[MenuItemImportRow], List[MenuItemError]]: 
                Valid rows and parsing errors
        """
        valid_rows = []
        errors = []
        
        try:
            # Parse CSV
            csv_file = io.StringIO(csv_content)
            reader = csv.DictReader(csv_file)
            
            # Validate headers
            if not reader.fieldnames:
                errors.append(MenuItemError(
                    row_number=0,
                    item_name=None,
                    error="CSV file is empty or has no headers"
                ))
                return valid_rows, errors
            
            # Check for required headers
            missing_headers = set(CSVMenuService.CSV_HEADERS) - set(reader.fieldnames)
            if missing_headers:
                errors.append(MenuItemError(
                    row_number=0,
                    item_name=None,
                    error=f"Missing required headers: {', '.join(missing_headers)}"
                ))
                return valid_rows, errors
            
            # Parse each row
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (header is row 1)
                try:
                    # Convert is_veg to boolean
                    is_veg_str = row.get('is_veg', 'true').lower()
                    is_veg = is_veg_str in ['true', '1', 'yes', 'y']
                    
                    # Convert prep_time to int or None
                    prep_time_str = row.get('prep_time', '').strip()
                    prep_time = int(prep_time_str) if prep_time_str else None
                    
                    # Create MenuItemImportRow
                    menu_item = MenuItemImportRow(
                        name=row['name'].strip(),
                        category_id=row['category_id'].strip(),
                        price=Decimal(row['price'].strip()),
                        description=row.get('description', '').strip() or None,
                        is_veg=is_veg,
                        image_url=row.get('image_url', '').strip() or None,
                        prep_time=prep_time
                    )
                    
                    valid_rows.append(menu_item)
                    
                except Exception as e:
                    errors.append(MenuItemError(
                        row_number=row_num,
                        item_name=row.get('name', 'Unknown'),
                        error=str(e)
                    ))
            
        except Exception as e:
            errors.append(MenuItemError(
                row_number=0,
                item_name=None,
                error=f"Failed to parse CSV: {str(e)}"
            ))
        
        return valid_rows, errors
    
    @staticmethod
    def validate_menu_items(
        db: Session,
        items: List[MenuItemImportRow],
        restaurant_id: UUID
    ) -> List[MenuItemError]:
        """
        Validate menu items before import.
        
        Args:
            db: Database session
            items: List of menu items to validate
            restaurant_id: Restaurant ID for validation
            
        Returns:
            List[MenuItemError]: Validation errors
        """
        errors = []
        
        # Get all valid category IDs for this restaurant
        valid_categories = db.query(Category.category_id).all()
        valid_category_ids = {str(cat.category_id) for cat in valid_categories}
        
        for idx, item in enumerate(items, start=2):
            # Validate category exists
            if item.category_id not in valid_category_ids:
                errors.append(MenuItemError(
                    row_number=idx,
                    item_name=item.name,
                    error=f"Invalid category_id: {item.category_id}"
                ))
            
            # Validate price
            if item.price <= 0:
                errors.append(MenuItemError(
                    row_number=idx,
                    item_name=item.name,
                    error="Price must be greater than 0"
                ))
            
            # Validate name length
            if len(item.name) > 255:
                errors.append(MenuItemError(
                    row_number=idx,
                    item_name=item.name,
                    error="Name exceeds 255 characters"
                ))
        
        return errors
    
    @staticmethod
    def bulk_create_menu_items(
        db: Session,
        items: List[MenuItemImportRow],
        restaurant_id: UUID
    ) -> Tuple[int, List[MenuItemError]]:
        """
        Bulk create menu items from validated rows.
        
        Args:
            db: Database session
            items: List of validated menu items
            restaurant_id: Restaurant ID
            
        Returns:
            Tuple[int, List[MenuItemError]]: 
                Count of created items and any errors
        """
        created_count = 0
        errors = []
        
        try:
            for idx, item in enumerate(items, start=2):
                try:
                    food_item = FoodItem(
                        restaurant_id=restaurant_id,
                        category_id=UUID(item.category_id),
                        name=item.name,
                        description=item.description,
                        price=item.price,
                        image=item.image_url,
                        is_veg=item.is_veg,
                        prep_time=item.prep_time,
                        is_available=True,
                        status='available'
                    )
                    
                    db.add(food_item)
                    created_count += 1
                    
                except Exception as e:
                    errors.append(MenuItemError(
                        row_number=idx,
                        item_name=item.name,
                        error=f"Failed to create item: {str(e)}"
                    ))
            
            # Commit all items at once
            db.commit()
            logger.info(f"Bulk created {created_count} menu items for restaurant {restaurant_id}")
            
        except Exception as e:
            db.rollback()
            logger.error(f"Bulk create failed: {str(e)}")
            errors.append(MenuItemError(
                row_number=0,
                item_name=None,
                error=f"Database error: {str(e)}"
            ))
            created_count = 0
        
        return created_count, errors
    
    @staticmethod
    def process_csv_upload(
        db: Session,
        csv_content: str,
        restaurant_id: UUID
    ) -> Dict:
        """
        Complete CSV upload process: parse, validate, and create items.
        
        Args:
            db: Database session
            csv_content: Raw CSV content
            restaurant_id: Restaurant ID
            
        Returns:
            Dict: Result with counts and errors
        """
        # Step 1: Parse CSV
        valid_rows, parse_errors = CSVMenuService.parse_csv(csv_content)
        
        if parse_errors and not valid_rows:
            return {
                'success': False,
                'total_rows': 0,
                'success_count': 0,
                'error_count': len(parse_errors),
                'errors': parse_errors
            }
        
        # Step 2: Validate items
        validation_errors = CSVMenuService.validate_menu_items(db, valid_rows, restaurant_id)
        
        if validation_errors:
            return {
                'success': False,
                'total_rows': len(valid_rows),
                'success_count': 0,
                'error_count': len(validation_errors),
                'errors': validation_errors
            }
        
        # Step 3: Bulk create items
        created_count, create_errors = CSVMenuService.bulk_create_menu_items(
            db, valid_rows, restaurant_id
        )
        
        total_errors = parse_errors + validation_errors + create_errors
        
        return {
            'success': created_count > 0,
            'total_rows': len(valid_rows),
            'success_count': created_count,
            'error_count': len(total_errors),
            'errors': total_errors
        }
