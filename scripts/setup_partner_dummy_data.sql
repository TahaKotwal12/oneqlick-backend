-- ====================================================================
-- ONEQLICK PARTNER APP - DUMMY DATA SETUP SCRIPT
-- ====================================================================
-- This script creates test data for the Partner App including:
-- 1. Restaurant Owner User
-- 2. Delivery Partner User
-- 3. Customer User (for orders)
-- 4. Restaurant with menu items
-- 5. Sample orders
-- 6. Categories
-- ====================================================================

-- ====================================================================
-- STEP 1: CREATE TEST USERS
-- ====================================================================

-- 1.1 Restaurant Owner User
-- Email: restaurant@oneqlick.com
-- Password: Restaurant@123 (hashed with bcrypt)
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id,
    email,
    phone,
    password_hash,
    first_name,
    last_name,
    role,
    status,
    profile_image,
    email_verified,
    phone_verified,
    created_at,
    updated_at
) VALUES (
    '11111111-1111-1111-1111-111111111111',
    'restaurant@oneqlick.com',
    '+919876543210',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Restaurant@123
    'Rajesh',
    'Kumar',
    'restaurant_owner',
    'active',
    'https://ui-avatars.com/api/?name=Rajesh+Kumar&background=4F46E5&color=fff',
    true,
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (email) DO NOTHING;

-- 1.2 Delivery Partner User
-- Email: partner@oneqlick.com
-- Password: Partner@123 (hashed with bcrypt)
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id,
    email,
    phone,
    password_hash,
    first_name,
    last_name,
    role,
    status,
    profile_image,
    email_verified,
    phone_verified,
    created_at,
    updated_at
) VALUES (
    '22222222-2222-2222-2222-222222222222',
    'partner@oneqlick.com',
    '+919876543211',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Partner@123
    'Amit',
    'Sharma',
    'delivery_partner',
    'active',
    'https://ui-avatars.com/api/?name=Amit+Sharma&background=10B981&color=fff',
    true,
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (email) DO NOTHING;

-- 1.3 Customer User (for creating orders)
-- Email: customer@oneqlick.com
-- Password: Customer@123
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id,
    email,
    phone,
    password_hash,
    first_name,
    last_name,
    role,
    status,
    profile_image,
    email_verified,
    phone_verified,
    created_at,
    updated_at
) VALUES (
    '33333333-3333-3333-3333-333333333333',
    'customer@oneqlick.com',
    '+919876543212',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Customer@123
    'Priya',
    'Patel',
    'customer',
    'active',
    'https://ui-avatars.com/api/?name=Priya+Patel&background=F59E0B&color=fff',
    true,
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (email) DO NOTHING;

-- ====================================================================
-- STEP 2: CREATE CUSTOMER ADDRESS (for orders)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_addresses_tbl (
    address_id,
    user_id,
    title,
    address_line1,
    address_line2,
    city,
    state,
    postal_code,
    latitude,
    longitude,
    is_default,
    created_at
) VALUES (
    '44444444-4444-4444-4444-444444444444',
    '33333333-3333-3333-3333-333333333333',
    'Home',
    'Flat 301, Sunshine Apartments',
    'Andheri West',
    'Mumbai',
    'Maharashtra',
    '400058',
    19.1334,
    72.8397,
    true,
    CURRENT_TIMESTAMP
) ON CONFLICT (address_id) DO NOTHING;

-- ====================================================================
-- STEP 3: CREATE RESTAURANT
-- ====================================================================

INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id,
    owner_id,
    name,
    description,
    phone,
    email,
    address_line1,
    address_line2,
    city,
    state,
    postal_code,
    latitude,
    longitude,
    image,
    cover_image,
    cuisine_type,
    avg_delivery_time,
    min_order_amount,
    delivery_fee,
    rating,
    total_ratings,
    status,
    is_open,
    opening_time,
    closing_time,
    created_at,
    updated_at
) VALUES (
    '55555555-5555-5555-5555-555555555555',
    '11111111-1111-1111-1111-111111111111', -- Restaurant owner user_id
    'Spice Kitchen - Mumbai',
    'Authentic Indian cuisine with a modern twist. We serve the best North Indian and South Indian dishes in Mumbai.',
    '+919876543210',
    'contact@spicekitchen.com',
    'Shop 12, Linking Road',
    'Bandra West',
    'Mumbai',
    'Maharashtra',
    '400050',
    19.0596,
    72.8295,
    'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
    'Indian, North Indian, South Indian',
    30,
    100.00,
    40.00,
    4.5,
    250,
    'active',
    true,
    '09:00:00',
    '23:00:00',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- STEP 4: CREATE FOOD CATEGORIES
-- ====================================================================

INSERT INTO core_mstr_one_qlick_categories_tbl (
    category_id,
    name,
    description,
    image,
    is_active,
    sort_order,
    created_at
) VALUES 
    ('66666666-6666-6666-6666-666666666661', 'Starters', 'Appetizers and starters', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200', true, 1, CURRENT_TIMESTAMP),
    ('66666666-6666-6666-6666-666666666662', 'Main Course', 'Main dishes and curries', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200', true, 2, CURRENT_TIMESTAMP),
    ('66666666-6666-6666-6666-666666666663', 'Breads', 'Naan, roti, and other breads', 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=200', true, 3, CURRENT_TIMESTAMP),
    ('66666666-6666-6666-6666-666666666664', 'Rice & Biryani', 'Rice dishes and biryani', 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200', true, 4, CURRENT_TIMESTAMP),
    ('66666666-6666-6666-6666-666666666665', 'Desserts', 'Sweet dishes and desserts', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=200', true, 5, CURRENT_TIMESTAMP),
    ('66666666-6666-6666-6666-666666666666', 'Beverages', 'Drinks and beverages', 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=200', true, 6, CURRENT_TIMESTAMP)
ON CONFLICT (category_id) DO NOTHING;

-- ====================================================================
-- STEP 5: CREATE FOOD ITEMS (MENU)
-- ====================================================================

-- Starters
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777771', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666661',
     'Paneer Tikka', 'Cottage cheese marinated in spices and grilled to perfection', 220.00, NULL,
     'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400', true,
     'Paneer, Yogurt, Spices, Bell Peppers', 'Dairy', 320, 15, 'available', 4.6, 85, 1),
    
    ('77777777-7777-7777-7777-777777777772', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666661',
     'Chicken Tikka', 'Tender chicken pieces marinated in yogurt and spices', 250.00, 230.00,
     'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400', false,
     'Chicken, Yogurt, Spices, Lemon', 'Dairy', 280, 20, 'available', 4.8, 120, 2),
    
    ('77777777-7777-7777-7777-777777777773', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666661',
     'Veg Spring Rolls', 'Crispy rolls filled with fresh vegetables', 180.00, NULL,
     'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb?w=400', true,
     'Cabbage, Carrots, Beans, Flour', 'Gluten', 250, 12, 'available', 4.3, 65, 3);

-- Main Course
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777774', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666662',
     'Butter Chicken', 'Rich and creamy tomato-based chicken curry', 320.00, NULL,
     'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400', false,
     'Chicken, Butter, Cream, Tomatoes, Spices', 'Dairy', 450, 25, 'available', 4.9, 200, 1),
    
    ('77777777-7777-7777-7777-777777777775', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666662',
     'Paneer Butter Masala', 'Cottage cheese in rich tomato and butter gravy', 280.00, 260.00,
     'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400', true,
     'Paneer, Butter, Cream, Tomatoes, Spices', 'Dairy', 380, 20, 'available', 4.7, 150, 2),
    
    ('77777777-7777-7777-7777-777777777776', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666662',
     'Dal Makhani', 'Black lentils cooked overnight with butter and cream', 240.00, NULL,
     'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400', true,
     'Black Lentils, Butter, Cream, Spices', 'Dairy', 320, 30, 'available', 4.6, 110, 3);

-- Breads
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777777', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666663',
     'Butter Naan', 'Soft leavened bread brushed with butter', 50.00, NULL,
     'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400', true,
     'Flour, Butter, Yeast', 'Gluten, Dairy', 180, 8, 'available', 4.5, 180, 1),
    
    ('77777777-7777-7777-7777-777777777778', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666663',
     'Garlic Naan', 'Naan topped with fresh garlic and coriander', 60.00, NULL,
     'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400', true,
     'Flour, Garlic, Butter, Coriander', 'Gluten, Dairy', 200, 10, 'available', 4.7, 160, 2);

-- Rice & Biryani
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777779', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666664',
     'Chicken Biryani', 'Fragrant basmati rice cooked with chicken and spices', 280.00, NULL,
     'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400', false,
     'Basmati Rice, Chicken, Spices, Saffron', NULL, 520, 35, 'available', 4.8, 220, 1),
    
    ('77777777-7777-7777-7777-777777777780', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666664',
     'Veg Biryani', 'Aromatic rice with mixed vegetables and spices', 220.00, 200.00,
     'https://images.unsplash.com/photo-1596797038530-2c107229654b?w=400', true,
     'Basmati Rice, Mixed Vegetables, Spices', NULL, 420, 30, 'available', 4.5, 140, 2);

-- Desserts
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777781', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666665',
     'Gulab Jamun', 'Soft milk dumplings in sugar syrup', 80.00, NULL,
     'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', true,
     'Milk Powder, Sugar, Cardamom', 'Dairy', 280, 5, 'available', 4.6, 95, 1),
    
    ('77777777-7777-7777-7777-777777777782', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666665',
     'Rasmalai', 'Cottage cheese dumplings in sweetened milk', 100.00, NULL,
     'https://images.unsplash.com/photo-1589119908995-c6c1f5f7e93c?w=400', true,
     'Paneer, Milk, Sugar, Saffron', 'Dairy', 320, 10, 'available', 4.7, 88, 2);

-- Beverages
INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, discount_price,
    image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, sort_order
) VALUES 
    ('77777777-7777-7777-7777-777777777783', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666666',
     'Mango Lassi', 'Refreshing yogurt drink with mango', 80.00, NULL,
     'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400', true,
     'Yogurt, Mango, Sugar', 'Dairy', 180, 5, 'available', 4.5, 120, 1),
    
    ('77777777-7777-7777-7777-777777777784', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666666',
     'Masala Chai', 'Traditional Indian spiced tea', 40.00, NULL,
     'https://images.unsplash.com/photo-1597318130993-c1ca8f24c1e3?w=400', true,
     'Tea, Milk, Spices, Sugar', 'Dairy', 120, 5, 'available', 4.4, 95, 2);

-- ====================================================================
-- STEP 6: CREATE DELIVERY PARTNER RECORD
-- ====================================================================

INSERT INTO core_mstr_one_qlick_delivery_partners_tbl (
    delivery_partner_id,
    user_id,
    vehicle_type,
    vehicle_number,
    license_number,
    current_latitude,
    current_longitude,
    availability_status,
    rating,
    total_ratings,
    total_deliveries,
    documents_json,
    is_verified,
    created_at,
    updated_at
) VALUES (
    '88888888-8888-8888-8888-888888888888',
    '22222222-2222-2222-2222-222222222222', -- Delivery partner user_id
    'motorcycle',
    'MH02AB1234',
    'DL1234567890',
    19.0760,
    72.8777,
    'available',
    4.7,
    85,
    120,
    '{"driving_license": "https://example.com/dl.jpg", "vehicle_rc": "https://example.com/rc.jpg"}',
    true,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
) ON CONFLICT (delivery_partner_id) DO NOTHING;

-- ====================================================================
-- STEP 7: CREATE SAMPLE ORDERS
-- ====================================================================

-- Order 1: Pending Order
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id,
    customer_id,
    restaurant_id,
    delivery_partner_id,
    delivery_address_id,
    order_number,
    subtotal,
    tax_amount,
    delivery_fee,
    discount_amount,
    total_amount,
    payment_method,
    payment_status,
    payment_id,
    order_status,
    estimated_delivery_time,
    special_instructions,
    created_at,
    updated_at
) VALUES (
    '99999999-9999-9999-9999-999999999991',
    '33333333-3333-3333-3333-333333333333',
    '55555555-5555-5555-5555-555555555555',
    NULL,
    '44444444-4444-4444-4444-444444444444',
    'ORD-1001',
    600.00,
    54.00,
    40.00,
    0.00,
    694.00,
    'upi',
    'paid',
    'UPI123456789',
    'pending',
    CURRENT_TIMESTAMP + INTERVAL '45 minutes',
    'Extra spicy please',
    CURRENT_TIMESTAMP - INTERVAL '5 minutes',
    CURRENT_TIMESTAMP - INTERVAL '5 minutes'
) ON CONFLICT (order_id) DO NOTHING;

-- Order 1 Items
INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    ('99999999-9999-9999-9999-999999999991', '77777777-7777-7777-7777-777777777774', 1, 320.00, 320.00), -- Butter Chicken
    ('99999999-9999-9999-9999-999999999991', '77777777-7777-7777-7777-777777777779', 1, 280.00, 280.00); -- Chicken Biryani

-- Order 2: Preparing Order
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_partner_id, delivery_address_id,
    order_number, subtotal, tax_amount, delivery_fee, discount_amount, total_amount,
    payment_method, payment_status, payment_id, order_status, estimated_delivery_time,
    special_instructions, created_at, updated_at
) VALUES (
    '99999999-9999-9999-9999-999999999992',
    '33333333-3333-3333-3333-333333333333',
    '55555555-5555-5555-5555-555555555555',
    NULL,
    '44444444-4444-4444-4444-444444444444',
    'ORD-1002',
    500.00,
    45.00,
    40.00,
    50.00,
    535.00,
    'card',
    'paid',
    'CARD987654321',
    'preparing',
    CURRENT_TIMESTAMP + INTERVAL '40 minutes',
    'Less oil',
    CURRENT_TIMESTAMP - INTERVAL '15 minutes',
    CURRENT_TIMESTAMP - INTERVAL '10 minutes'
) ON CONFLICT (order_id) DO NOTHING;

-- Order 2 Items
INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    ('99999999-9999-9999-9999-999999999992', '77777777-7777-7777-7777-777777777775', 1, 280.00, 280.00), -- Paneer Butter Masala
    ('99999999-9999-9999-9999-999999999992', '77777777-7777-7777-7777-777777777772', 1, 220.00, 220.00); -- Paneer Tikka

-- Order 3: Ready for Pickup
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_partner_id, delivery_address_id,
    order_number, subtotal, tax_amount, delivery_fee, discount_amount, total_amount,
    payment_method, payment_status, payment_id, order_status, estimated_delivery_time,
    created_at, updated_at
) VALUES (
    '99999999-9999-9999-9999-999999999993',
    '33333333-3333-3333-3333-333333333333',
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222',
    '44444444-4444-4444-4444-444444444444',
    'ORD-1003',
    380.00,
    34.20,
    40.00,
    0.00,
    454.20,
    'upi',
    'paid',
    'UPI111222333',
    'ready_for_pickup',
    CURRENT_TIMESTAMP + INTERVAL '30 minutes',
    CURRENT_TIMESTAMP - INTERVAL '25 minutes',
    CURRENT_TIMESTAMP - INTERVAL '5 minutes'
) ON CONFLICT (order_id) DO NOTHING;

-- Order 3 Items
INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    ('99999999-9999-9999-9999-999999999993', '77777777-7777-7777-7777-777777777780', 1, 220.00, 220.00), -- Veg Biryani
    ('99999999-9999-9999-9999-999999999993', '77777777-7777-7777-7777-777777777781', 2, 80.00, 160.00); -- Gulab Jamun

-- Order 4: Delivered Order (for history)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_partner_id, delivery_address_id,
    order_number, subtotal, tax_amount, delivery_fee, discount_amount, total_amount,
    payment_method, payment_status, payment_id, order_status, estimated_delivery_time,
    actual_delivery_time, rating, review, created_at, updated_at
) VALUES (
    '99999999-9999-9999-9999-999999999994',
    '33333333-3333-3333-3333-333333333333',
    '55555555-5555-5555-5555-555555555555',
    '22222222-2222-2222-2222-222222222222',
    '44444444-4444-4444-4444-444444444444',
    'ORD-1004',
    720.00,
    64.80,
    40.00,
    0.00,
    824.80,
    'upi',
    'paid',
    'UPI444555666',
    'delivered',
    CURRENT_TIMESTAMP - INTERVAL '1 hour',
    CURRENT_TIMESTAMP - INTERVAL '30 minutes',
    5,
    'Excellent food and fast delivery!',
    CURRENT_TIMESTAMP - INTERVAL '2 hours',
    CURRENT_TIMESTAMP - INTERVAL '30 minutes'
) ON CONFLICT (order_id) DO NOTHING;

-- Order 4 Items
INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    ('99999999-9999-9999-9999-999999999994', '77777777-7777-7777-7777-777777777774', 2, 320.00, 640.00), -- Butter Chicken x2
    ('99999999-9999-9999-9999-999999999994', '77777777-7777-7777-7777-777777777783', 1, 80.00, 80.00); -- Mango Lassi

-- ====================================================================
-- VERIFICATION QUERIES
-- ====================================================================

-- Verify users created
SELECT 
    user_id, 
    email, 
    first_name, 
    last_name, 
    role, 
    status,
    email_verified
FROM core_mstr_one_qlick_users_tbl
WHERE email IN ('restaurant@oneqlick.com', 'partner@oneqlick.com', 'customer@oneqlick.com')
ORDER BY role;

-- Verify restaurant created
SELECT 
    restaurant_id,
    name,
    owner_id,
    city,
    cuisine_type,
    status,
    is_open
FROM core_mstr_one_qlick_restaurants_tbl
WHERE owner_id = '11111111-1111-1111-1111-111111111111';

-- Verify menu items created
SELECT 
    f.name,
    c.name as category,
    f.price,
    f.is_veg,
    f.status
FROM core_mstr_one_qlick_food_items_tbl f
JOIN core_mstr_one_qlick_categories_tbl c ON f.category_id = c.category_id
WHERE f.restaurant_id = '55555555-5555-5555-5555-555555555555'
ORDER BY c.sort_order, f.sort_order;

-- Verify orders created
SELECT 
    order_number,
    order_status,
    payment_status,
    total_amount,
    created_at
FROM core_mstr_one_qlick_orders_tbl
WHERE restaurant_id = '55555555-5555-5555-5555-555555555555'
ORDER BY created_at DESC;

-- ====================================================================
-- SUCCESS MESSAGE
-- ====================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Dummy data setup complete!';
    RAISE NOTICE '';
    RAISE NOTICE '📧 Login Credentials:';
    RAISE NOTICE '   Restaurant Owner: restaurant@oneqlick.com / Restaurant@123';
    RAISE NOTICE '   Delivery Partner: partner@oneqlick.com / Partner@123';
    RAISE NOTICE '   Customer: customer@oneqlick.com / Customer@123';
    RAISE NOTICE '';
    RAISE NOTICE '🏪 Restaurant: Spice Kitchen - Mumbai';
    RAISE NOTICE '   - 14 menu items across 6 categories';
    RAISE NOTICE '   - 4 sample orders (pending, preparing, ready, delivered)';
    RAISE NOTICE '';
    RAISE NOTICE '🚀 You can now test the Partner App!';
END $$;
