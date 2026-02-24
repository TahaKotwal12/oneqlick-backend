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
        'category_name',
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
            'Main Course',
            '250.00',
            'Creamy tomato curry with cottage cheese',
            'true',
            'https://example.com/paneer.jpg',
            '20'
        ])
        writer.writerow([
            'Chicken Biryani',
            'Main Course',
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
                        category_name=row['category_name'].strip(),
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
    def get_or_create_category(
        db: Session,
        category_name: str,
        restaurant_id: UUID
    ) -> UUID:
        """
        Get existing category or create new one.
        Categories are global (shared across all restaurants).
        
        Args:
            db: Database session
            category_name: Name of the category
            restaurant_id: Restaurant ID (not used, categories are global)
            
        Returns:
            UUID: Category ID
        """
        from sqlalchemy import func
        
        # Check if category exists (case-insensitive)
        # Categories are global, so we don't filter by restaurant_id
        category = db.query(Category).filter(
            func.lower(Category.name) == category_name.lower()
        ).first()
        
        if category:
            return category.category_id
        
        # Create new category
        new_category = Category(
            name=category_name.strip(),
            description=f"Category for {category_name}",
            is_active=True,
            show_on_home=False,
            sort_order=0
        )
        db.add(new_category)
        db.flush()  # Get the ID without committing
        
        logger.info(f"Created new global category: {category_name}")
        return new_category.category_id
    
    @staticmethod
    def validate_and_prepare_items(
        db: Session,
        items: List[MenuItemImportRow],
        restaurant_id: UUID
    ) -> Tuple[List[Dict], List[MenuItemError]]:
        """
        Validate menu items and prepare with category IDs.
        Creates categories automatically if they don't exist.
        
        Args:
            db: Database session
            items: List of menu items to validate
            restaurant_id: Restaurant ID
            
        Returns:
            Tuple[List[Dict], List[MenuItemError]]: Prepared items and errors
        """
        errors = []
        prepared_items = []
        category_cache = {}  # Cache to avoid duplicate queries
        
        for idx, item in enumerate(items, start=2):
            try:
                # Get or create category
                if item.category_name not in category_cache:
                    category_id = CSVMenuService.get_or_create_category(
                        db, item.category_name, restaurant_id
                    )
                    category_cache[item.category_name] = category_id
                else:
                    category_id = category_cache[item.category_name]
                
                # Validate price
                if item.price <= 0:
                    errors.append(MenuItemError(
                        row_number=idx,
                        item_name=item.name,
                        error="Price must be greater than 0"
                    ))
                    continue
                
                # Validate name length
                if len(item.name) > 255:
                    errors.append(MenuItemError(
                        row_number=idx,
                        item_name=item.name,
                        error="Name exceeds 255 characters"
                    ))
                    continue
                
                # Add to prepared items
                prepared_items.append({
                    'item': item,
                    'category_id': category_id
                })
                
            except Exception as e:
                errors.append(MenuItemError(
                    row_number=idx,
                    item_name=item.name,
                    error=f"Failed to process: {str(e)}"
                ))
        
        return prepared_items, errors
    
    @staticmethod
    def bulk_create_menu_items(
        db: Session,
        prepared_items: List[Dict],
        restaurant_id: UUID
    ) -> Tuple[int, List[MenuItemError]]:
        """
        Bulk create menu items from prepared items with category IDs.
        
        Args:
            db: Database session
            prepared_items: List of prepared items with category IDs
            restaurant_id: Restaurant ID
            
        Returns:
            Tuple[int, List[MenuItemError]]: 
                Count of created items and any errors
        """
        created_count = 0
        errors = []
        
        try:
            for idx, prepared in enumerate(prepared_items, start=2):
                try:
                    item = prepared['item']
                    category_id = prepared['category_id']
                    
                    food_item = FoodItem(
                        restaurant_id=restaurant_id,
                        category_id=category_id,
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
                'message': 'CSV parsing failed',
                'total_rows': 0,
                'success_count': 0,
                'error_count': len(parse_errors),
                'errors': parse_errors
            }
        
        # Step 2: Validate and prepare items (creates categories automatically)
        prepared_items, validation_errors = CSVMenuService.validate_and_prepare_items(
            db, valid_rows, restaurant_id
        )
        
        if validation_errors and not prepared_items:
            return {
                'success': False,
                'message': 'Validation failed',
                'total_rows': len(valid_rows),
                'success_count': 0,
                'error_count': len(validation_errors),
                'errors': validation_errors
            }
        
        # Step 3: Bulk create items
        created_count, create_errors = CSVMenuService.bulk_create_menu_items(
            db, prepared_items, restaurant_id
        )
        
        total_errors = parse_errors + validation_errors + create_errors
        
        return {
            'success': created_count > 0,
            'message': f'Successfully uploaded {created_count} items',
            'total_rows': len(valid_rows),
            'success_count': created_count,
            'error_count': len(total_errors),
            'errors': total_errors
        }
