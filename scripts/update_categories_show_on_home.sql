-- ====================================================================
-- QUICK UPDATE SCRIPT - SET FEATURED CATEGORIES
-- ====================================================================
-- Run this after checking your actual category names in the database
-- ====================================================================

-- STEP 1: First, check what categories you have
-- Run this query to see all your existing categories:

SELECT 
    category_id,
    name,
    description,
    is_active,
    sort_order
FROM core_mstr_one_qlick_categories_tbl
ORDER BY name;

-- ====================================================================
-- STEP 2: Add the show_on_home column
-- ====================================================================

ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS show_on_home BOOLEAN DEFAULT FALSE;

ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS icon VARCHAR(100);

ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS color VARCHAR(20);

-- ====================================================================
-- STEP 3: Set show_on_home = TRUE for categories you want on home screen
-- ====================================================================

-- METHOD 1: Update by category names
-- Replace these names with your actual category names from STEP 1

UPDATE core_mstr_one_qlick_categories_tbl 
SET show_on_home = TRUE 
WHERE name IN (
    'Appetizers',      -- Replace with your actual category name
    'Main Course',     -- Replace with your actual category name
    'Desserts',        -- Replace with your actual category name
    'Beverages',       -- Replace with your actual category name
    'Fast Food'        -- Replace with your actual category name
);

-- OR

-- METHOD 2: Update by category IDs (if you know the IDs)
-- Uncomment and use this if you prefer to use IDs

-- UPDATE core_mstr_one_qlick_categories_tbl 
-- SET show_on_home = TRUE 
-- WHERE category_id IN (
--     'uuid-1',  -- Replace with actual UUID
--     'uuid-2',  -- Replace with actual UUID
--     'uuid-3',  -- Replace with actual UUID
--     'uuid-4',  -- Replace with actual UUID
--     'uuid-5'   -- Replace with actual UUID
-- );

-- ====================================================================
-- STEP 4: Add icons and colors to featured categories
-- ====================================================================

-- Update icons and colors for each featured category
-- Customize these based on your preferences

UPDATE core_mstr_one_qlick_categories_tbl 
SET 
    icon = CASE name
        WHEN 'Appetizers' THEN 'food-drumstick'
        WHEN 'Main Course' THEN 'food-turkey'
        WHEN 'Desserts' THEN 'cake'
        WHEN 'Beverages' THEN 'cup-outline'
        WHEN 'Fast Food' THEN 'pizza'
        ELSE icon
    END,
    color = CASE name
        WHEN 'Appetizers' THEN '#06B6D4'
        WHEN 'Main Course' THEN '#8B5CF6'
        WHEN 'Desserts' THEN '#F97316'
        WHEN 'Beverages' THEN '#A78BFA'
        WHEN 'Fast Food' THEN '#84CC16'
        ELSE color
    END
WHERE show_on_home = TRUE;

-- ====================================================================
-- STEP 5: Verify the results
-- ====================================================================

-- Check featured categories
SELECT 
    name,
    icon,
    color,
    show_on_home,
    is_active,
    sort_order
FROM core_mstr_one_qlick_categories_tbl
WHERE show_on_home = TRUE
ORDER BY sort_order, name;

-- Check all categories
SELECT 
    name,
    show_on_home,
    is_active
FROM core_mstr_one_qlick_categories_tbl
ORDER BY show_on_home DESC, name;

-- Summary
SELECT 
    'Featured (shown on home)' as category_type,
    COUNT(*) as count
FROM core_mstr_one_qlick_categories_tbl
WHERE show_on_home = TRUE
UNION ALL
SELECT 
    'Other (searchable only)' as category_type,
    COUNT(*) as count
FROM core_mstr_one_qlick_categories_tbl
WHERE show_on_home = FALSE;

-- ====================================================================
-- OPTIONAL: If you want to reset and start over
-- ====================================================================

-- Uncomment this to reset all categories to NOT featured
-- UPDATE core_mstr_one_qlick_categories_tbl SET show_on_home = FALSE;

-- ====================================================================
-- COMPLETION
-- ====================================================================

SELECT '✅ Update complete! Check the results above.' as status;
