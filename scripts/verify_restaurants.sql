-- ====================================================================
-- VERIFICATION SCRIPT - Check if restaurants were created
-- ====================================================================

-- Check restaurant owners
SELECT 
    'RESTAURANT OWNERS' as check_type,
    user_id, email, first_name, last_name, role, status, email_verified
FROM core_mstr_one_qlick_users_tbl
WHERE email IN (
    'maharaja@oneqlick.com',
    'shivaji@oneqlick.com',
    'kolhapuri@oneqlick.com',
    'swaad@oneqlick.com',
    'misal@oneqlick.com'
)
ORDER BY email;

-- Check restaurants
SELECT 
    'RESTAURANTS' as check_type,
    restaurant_id, name, city, cuisine_type, status, is_open
FROM core_mstr_one_qlick_restaurants_tbl
WHERE name IN (
    'Maharaja Bhojnalaya',
    'Shivaji Vada Pav Center',
    'Kolhapuri Katta',
    'Swaad South Indian',
    'Pune Misal House'
)
ORDER BY name;

-- Check menu items count
SELECT 
    'MENU ITEMS COUNT' as check_type,
    r.name as restaurant_name,
    COUNT(f.food_item_id) as item_count
FROM core_mstr_one_qlick_restaurants_tbl r
LEFT JOIN core_mstr_one_qlick_food_items_tbl f ON r.restaurant_id = f.restaurant_id
WHERE r.name IN (
    'Maharaja Bhojnalaya',
    'Shivaji Vada Pav Center',
    'Kolhapuri Katta',
    'Swaad South Indian',
    'Pune Misal House'
)
GROUP BY r.name
ORDER BY r.name;

-- Check orders count
SELECT 
    'ORDERS COUNT' as check_type,
    r.name as restaurant_name,
    COUNT(o.order_id) as order_count
FROM core_mstr_one_qlick_restaurants_tbl r
LEFT JOIN core_mstr_one_qlick_orders_tbl o ON r.restaurant_id = o.restaurant_id
WHERE r.name IN (
    'Maharaja Bhojnalaya',
    'Shivaji Vada Pav Center',
    'Kolhapuri Katta',
    'Swaad South Indian',
    'Pune Misal House'
)
GROUP BY r.name
ORDER BY r.name;

-- Check password hash for one user (to verify it's correct)
SELECT 
    'PASSWORD CHECK' as check_type,
    email,
    LEFT(password_hash, 20) || '...' as password_hash_preview,
    LENGTH(password_hash) as hash_length
FROM core_mstr_one_qlick_users_tbl
WHERE email = 'maharaja@oneqlick.com';
