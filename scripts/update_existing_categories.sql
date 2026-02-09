-- ====================================================================
-- UPDATE EXISTING CATEGORIES TO SHOW ON HOME/SEARCH SCREENS
-- ====================================================================
-- This script adds the show_on_home column and updates existing categories
-- to be featured on the home and search screens.
-- ====================================================================

-- Step 1: Add the show_on_home column if it doesn't exist
ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS show_on_home BOOLEAN DEFAULT FALSE;

-- Step 2: Add icon and color columns if they don't exist (for future use)
ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS icon VARCHAR(100),
ADD COLUMN IF NOT EXISTS color VARCHAR(20);

-- Step 3: Set show_on_home = TRUE for existing categories that should be featured
-- Update based on category names (adjust the names to match your actual data)

UPDATE core_mstr_one_qlick_categories_tbl 
SET show_on_home = TRUE 
WHERE name IN (
    'Appetizers',
    'Main Course', 
    'Desserts',
    'Beverages',
    'Fast Food'
);

-- Step 4: Update icon and color for the featured categories (optional)
-- You can customize these based on your design preferences

-- Appetizers
UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = 'food-drumstick',
    color = '#06B6D4'
WHERE name = 'Appetizers' AND show_on_home = TRUE;

-- Main Course
UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = 'food-turkey',
    color = '#8B5CF6'
WHERE name = 'Main Course' AND show_on_home = TRUE;

-- Desserts
UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = 'cake',
    color = '#F97316'
WHERE name = 'Desserts' AND show_on_home = TRUE;

-- Beverages
UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = 'cup-outline',
    color = '#A78BFA'
WHERE name = 'Beverages' AND show_on_home = TRUE;

-- Fast Food
UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = 'pizza',
    color = '#84CC16'
WHERE name = 'Fast Food' AND show_on_home = TRUE;

-- Step 5: Verify the updates
SELECT 
    category_id,
    name,
    icon,
    color,
    is_active,
    show_on_home,
    sort_order,
    created_at
FROM core_mstr_one_qlick_categories_tbl
ORDER BY 
    show_on_home DESC,
    sort_order ASC,
    name ASC;

-- Step 6: Show summary
SELECT 
    show_on_home,
    COUNT(*) as category_count
FROM core_mstr_one_qlick_categories_tbl
GROUP BY show_on_home
ORDER BY show_on_home DESC;

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================
SELECT '✅ Categories updated successfully!' as status,
       (SELECT COUNT(*) FROM core_mstr_one_qlick_categories_tbl WHERE show_on_home = TRUE) as featured_categories,
       (SELECT COUNT(*) FROM core_mstr_one_qlick_categories_tbl WHERE show_on_home = FALSE) as other_categories,
       (SELECT COUNT(*) FROM core_mstr_one_qlick_categories_tbl) as total_categories;
