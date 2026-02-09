-- ====================================================================
-- FOOD CATEGORIES SETUP SCRIPT
-- ====================================================================
-- This script inserts the 8 food categories used in the OneQlick User App
-- with their corresponding images, icons, and colors.
-- ====================================================================

-- First, add the new columns to the categories table if they don't exist
ALTER TABLE core_mstr_one_qlick_categories_tbl 
ADD COLUMN IF NOT EXISTS icon VARCHAR(100),
ADD COLUMN IF NOT EXISTS color VARCHAR(20),
ADD COLUMN IF NOT EXISTS show_on_home BOOLEAN DEFAULT FALSE;

-- Clear existing categories (optional - comment out if you want to keep existing data)
-- TRUNCATE TABLE core_mstr_one_qlick_categories_tbl CASCADE;

-- Insert the 8 food categories with their complete data
-- These categories will be shown on home/search screens (show_on_home = TRUE)
INSERT INTO core_mstr_one_qlick_categories_tbl (
    name, 
    description, 
    image, 
    icon, 
    color, 
    is_active, 
    show_on_home,
    sort_order
) VALUES
-- 1. South Indian
(
    'South Indian',
    'Traditional South Indian cuisine including dosas, idlis, vadas, and more',
    'https://www.vegrecipesofindia.com/wp-content/uploads/2018/09/drumstick-recipe-1.jpg',
    'food-drumstick',
    '#06B6D4',
    TRUE,
    TRUE,
    1
),

-- 2. North Indian
(
    'North Indian',
    'Rich and flavorful North Indian dishes including curries, tandoori, and biryanis',
    'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=200&h=200&fit=crop&crop=center&q=80',
    'food-turkey',
    '#8B5CF6',
    TRUE,
    TRUE,
    2
),

-- 3. Chinese
(
    'Chinese',
    'Indo-Chinese fusion cuisine with noodles, fried rice, and manchurian',
    'https://curlytales.com/wp-content/uploads/2019/12/WhatsApp-Image-2019-12-04-at-1.55.49-PM.jpeg',
    'noodles',
    '#10B981',
    TRUE,
    TRUE,
    3
),

-- 4. Beverages
(
    'Beverages',
    'Refreshing drinks including tea, coffee, juices, and soft drinks',
    'https://www.saveur.com/uploads/2007/02/SAVEUR_Mojito_1149-Edit-scaled.jpg?format=auto&optimize=high&width=1440',
    'cup-outline',
    '#A78BFA',
    TRUE,
    TRUE,
    4
),

-- 5. Fast Food
(
    'Fast Food',
    'Quick bites including pizzas, burgers, sandwiches, and wraps',
    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200&h=200&fit=crop&crop=center&q=80',
    'pizza',
    '#84CC16',
    TRUE,
    TRUE,
    5
),

-- 6. Breakfast
(
    'Breakfast',
    'Morning delights including parathas, poha, upma, and breakfast combos',
    'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=500&h=500&fit=crop&crop=center&q=80',
    'truck-delivery',
    '#64748B',
    TRUE,
    TRUE,
    6
),

-- 7. Kokani
(
    'Kokani',
    'Authentic Kokani cuisine with fresh seafood and traditional coastal flavors',
    'https://gmcratnagiri.in/wp-content/uploads/2024/08/non-veg-thali.png',
    'pasta',
    '#EC4899',
    TRUE,
    TRUE,
    7
),

-- 8. Desserts
(
    'Desserts',
    'Sweet treats including ice creams, cakes, traditional sweets, and more',
    'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200&h=200&fit=crop&crop=center&q=80',
    'cake',
    '#F97316',
    TRUE,
    TRUE,
    8
)
ON CONFLICT DO NOTHING;

-- Verify the insertion
SELECT 
    category_id,
    name,
    icon,
    color,
    sort_order,
    is_active
FROM core_mstr_one_qlick_categories_tbl
ORDER BY sort_order;

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================
SELECT '✅ Food categories setup completed successfully!' as status,
       COUNT(*) as total_categories
FROM core_mstr_one_qlick_categories_tbl;
