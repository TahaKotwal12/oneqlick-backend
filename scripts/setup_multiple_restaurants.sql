-- ====================================================================
-- ONEQLICK - MULTIPLE RESTAURANTS DUMMY DATA
-- ====================================================================
-- This script creates 5 restaurants with owners, menus, and orders
-- ====================================================================

-- ====================================================================
-- RESTAURANT 1: SPICE KITCHEN (INDIAN)
-- ====================================================================

-- Owner 1
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    '11111111-1111-1111-1111-111111111111',
    'spicekitchen@oneqlick.com',
    '+919876543210',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Rajesh', 'Kumar', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Rajesh+Kumar&background=4F46E5&color=fff',
    true, true
) ON CONFLICT (email) DO NOTHING;

-- Restaurant 1
INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time
) VALUES (
    '55555555-5555-5555-5555-555555555551',
    '11111111-1111-1111-1111-111111111111',
    'Spice Kitchen',
    'Authentic North Indian cuisine with traditional recipes',
    '+919876543210', 'contact@spicekitchen.com',
    'Shop 12, Linking Road', 'Bandra West', 'Mumbai', 'Maharashtra', '400050',
    19.0596, 72.8295,
    'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
    'North Indian, Mughlai',
    30, 150.00, 40.00, 4.5, 250, 'active', true, '09:00:00', '23:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 2: PIZZA PARADISE (ITALIAN)
-- ====================================================================

-- Owner 2
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    '11111111-1111-1111-1111-111111111112',
    'pizzaparadise@oneqlick.com',
    '+919876543211',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Marco', 'Rossi', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Marco+Rossi&background=EF4444&color=fff',
    true, true
) ON CONFLICT (email) DO NOTHING;

-- Restaurant 2
INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time
) VALUES (
    '55555555-5555-5555-5555-555555555552',
    '11111111-1111-1111-1111-111111111112',
    'Pizza Paradise',
    'Wood-fired authentic Italian pizzas and pasta',
    '+919876543211', 'contact@pizzaparadise.com',
    '45, MG Road', 'Koramangala', 'Bangalore', 'Karnataka', '560034',
    12.9352, 77.6245,
    'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=400',
    'https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=800',
    'Italian, Pizza, Pasta',
    25, 200.00, 30.00, 4.7, 320, 'active', true, '11:00:00', '23:30:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 3: BURGER BROS (AMERICAN)
-- ====================================================================

-- Owner 3
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    '11111111-1111-1111-1111-111111111113',
    'burgerbros@oneqlick.com',
    '+919876543212',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'John', 'Smith', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=John+Smith&background=F59E0B&color=fff',
    true, true
) ON CONFLICT (email) DO NOTHING;

-- Restaurant 3
INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time
) VALUES (
    '55555555-5555-5555-5555-555555555553',
    '11111111-1111-1111-1111-111111111113',
    'Burger Bros',
    'Gourmet burgers and American comfort food',
    '+919876543212', 'contact@burgerbros.com',
    'Shop 8, Cyber Hub', 'DLF Phase 2', 'Gurgaon', 'Haryana', '122002',
    28.4950, 77.0890,
    'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
    'https://images.unsplash.com/photo-1550547660-d9450f859349?w=800',
    'American, Burgers, Fast Food',
    20, 180.00, 35.00, 4.6, 280, 'active', true, '10:00:00', '00:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 4: SUSHI STATION (JAPANESE)
-- ====================================================================

-- Owner 4
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    '11111111-1111-1111-1111-111111111114',
    'sushistation@oneqlick.com',
    '+919876543213',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Yuki', 'Tanaka', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Yuki+Tanaka&background=10B981&color=fff',
    true, true
) ON CONFLICT (email) DO NOTHING;

-- Restaurant 4
INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time
) VALUES (
    '55555555-5555-5555-5555-555555555554',
    '11111111-1111-1111-1111-111111111114',
    'Sushi Station',
    'Fresh sushi and authentic Japanese cuisine',
    '+919876543213', 'contact@sushistation.com',
    '23, Park Street', 'Park Street Area', 'Kolkata', 'West Bengal', '700016',
    22.5546, 88.3516,
    'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
    'https://images.unsplash.com/photo-1579027989536-b7b1f875659b?w=800',
    'Japanese, Sushi, Asian',
    35, 250.00, 50.00, 4.8, 410, 'active', true, '12:00:00', '22:30:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 5: TACO FIESTA (MEXICAN)
-- ====================================================================

-- Owner 5
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    '11111111-1111-1111-1111-111111111115',
    'tacofiesta@oneqlick.com',
    '+919876543214',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Carlos', 'Rodriguez', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Carlos+Rodriguez&background=8B5CF6&color=fff',
    true, true
) ON CONFLICT (email) DO NOTHING;

-- Restaurant 5
INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time
) VALUES (
    '55555555-5555-5555-5555-555555555555',
    '11111111-1111-1111-1111-111111111115',
    'Taco Fiesta',
    'Vibrant Mexican flavors and street food',
    '+919876543214', 'contact@tacofiesta.com',
    '67, FC Road', 'Deccan Gymkhana', 'Pune', 'Maharashtra', '411004',
    18.5196, 73.8553,
    'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400',
    'https://images.unsplash.com/photo-1613514785940-daed07799d9b?w=800',
    'Mexican, Tex-Mex',
    28, 170.00, 38.00, 4.4, 190, 'active', true, '11:30:00', '23:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- CREATE CATEGORIES (SHARED)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order) VALUES 
    ('66666666-6666-6666-6666-666666666661', 'Starters', 'Appetizers and starters', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200', true, 1),
    ('66666666-6666-6666-6666-666666666662', 'Main Course', 'Main dishes', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200', true, 2),
    ('66666666-6666-6666-6666-666666666663', 'Breads', 'Breads and sides', 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=200', true, 3),
    ('66666666-6666-6666-6666-666666666664', 'Rice & Biryani', 'Rice dishes', 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200', true, 4),
    ('66666666-6666-6666-6666-666666666665', 'Desserts', 'Sweet dishes', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=200', true, 5),
    ('66666666-6666-6666-6666-666666666666', 'Beverages', 'Drinks', 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=200', true, 6),
    ('66666666-6666-6666-6666-666666666667', 'Pizza', 'Pizzas', 'https://images.unsplash.com/photo-1513104890138-7c749659a591?w=200', true, 7),
    ('66666666-6666-6666-6666-666666666668', 'Pasta', 'Pasta dishes', 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=200', true, 8),
    ('66666666-6666-6666-6666-666666666669', 'Burgers', 'Burgers', 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=200', true, 9),
    ('66666666-6666-6666-6666-666666666670', 'Sushi', 'Sushi rolls', 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=200', true, 10),
    ('66666666-6666-6666-6666-666666666671', 'Tacos', 'Tacos and wraps', 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=200', true, 11)
ON CONFLICT (category_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 1 MENU (SPICE KITCHEN - INDIAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('77777777-7777-7777-7777-777777777101', '55555555-5555-5555-5555-555555555551', '66666666-6666-6666-6666-666666666661',
     'Paneer Tikka', 'Grilled cottage cheese with spices', 220.00, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400',
     true, 15, 'available', 4.6, 85),
    ('77777777-7777-7777-7777-777777777102', '55555555-5555-5555-5555-555555555551', '66666666-6666-6666-6666-666666666662',
     'Butter Chicken', 'Creamy tomato-based chicken curry', 320.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400',
     false, 25, 'available', 4.9, 200),
    ('77777777-7777-7777-7777-777777777103', '55555555-5555-5555-5555-555555555551', '66666666-6666-6666-6666-666666666663',
     'Butter Naan', 'Soft leavened bread', 50.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
     true, 8, 'available', 4.5, 180),
    ('77777777-7777-7777-7777-777777777104', '55555555-5555-5555-5555-555555555551', '66666666-6666-6666-6666-666666666664',
     'Chicken Biryani', 'Fragrant rice with chicken', 280.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
     false, 35, 'available', 4.8, 220),
    ('77777777-7777-7777-7777-777777777105', '55555555-5555-5555-5555-555555555551', '66666666-6666-6666-6666-666666666665',
     'Gulab Jamun', 'Sweet milk dumplings', 80.00, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400',
     true, 5, 'available', 4.6, 95);

-- ====================================================================
-- RESTAURANT 2 MENU (PIZZA PARADISE - ITALIAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('77777777-7777-7777-7777-777777777201', '55555555-5555-5555-5555-555555555552', '66666666-6666-6666-6666-666666666667',
     'Margherita Pizza', 'Classic tomato and mozzarella', 350.00, 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=400',
     true, 18, 'available', 4.7, 150),
    ('77777777-7777-7777-7777-777777777202', '55555555-5555-5555-5555-555555555552', '66666666-6666-6666-6666-666666666667',
     'Pepperoni Pizza', 'Loaded with pepperoni', 420.00, 'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400',
     false, 20, 'available', 4.8, 180),
    ('77777777-7777-7777-7777-777777777203', '55555555-5555-5555-5555-555555555552', '66666666-6666-6666-6666-666666666668',
     'Alfredo Pasta', 'Creamy white sauce pasta', 280.00, 'https://images.unsplash.com/photo-1621996346565-e3dbc646d9a9?w=400',
     true, 15, 'available', 4.6, 120),
    ('77777777-7777-7777-7777-777777777204', '55555555-5555-5555-5555-555555555552', '66666666-6666-6666-6666-666666666668',
     'Arrabiata Pasta', 'Spicy tomato sauce pasta', 260.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
     true, 15, 'available', 4.5, 95),
    ('77777777-7777-7777-7777-777777777205', '55555555-5555-5555-5555-555555555552', '66666666-6666-6666-6666-666666666665',
     'Tiramisu', 'Classic Italian dessert', 180.00, 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=400',
     true, 10, 'available', 4.9, 140);

-- ====================================================================
-- RESTAURANT 3 MENU (BURGER BROS - AMERICAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('77777777-7777-7777-7777-777777777301', '55555555-5555-5555-5555-555555555553', '66666666-6666-6666-6666-666666666669',
     'Classic Burger', 'Beef patty with cheese', 250.00, 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
     false, 12, 'available', 4.7, 200),
    ('77777777-7777-7777-7777-777777777302', '55555555-5555-5555-5555-555555555553', '66666666-6666-6666-6666-666666666669',
     'Veggie Burger', 'Plant-based patty', 220.00, 'https://images.unsplash.com/photo-1520072959219-c595dc870360?w=400',
     true, 12, 'available', 4.5, 130),
    ('77777777-7777-7777-7777-777777777303', '55555555-5555-5555-5555-555555555553', '66666666-6666-6666-6666-666666666661',
     'Loaded Fries', 'Fries with cheese and bacon', 180.00, 'https://images.unsplash.com/photo-1573080496219-bb080dd4f877?w=400',
     false, 10, 'available', 4.6, 160),
    ('77777777-7777-7777-7777-777777777304', '55555555-5555-5555-5555-555555555553', '66666666-6666-6666-6666-666666666666',
     'Chocolate Shake', 'Thick chocolate milkshake', 150.00, 'https://images.unsplash.com/photo-1572490122747-3968b75cc699?w=400',
     true, 5, 'available', 4.8, 175),
    ('77777777-7777-7777-7777-777777777305', '55555555-5555-5555-5555-555555555553', '66666666-6666-6666-6666-666666666665',
     'Brownie Sundae', 'Warm brownie with ice cream', 160.00, 'https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=400',
     true, 8, 'available', 4.7, 145);

-- ====================================================================
-- RESTAURANT 4 MENU (SUSHI STATION - JAPANESE)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('77777777-7777-7777-7777-777777777401', '55555555-5555-5555-5555-555555555554', '66666666-6666-6666-6666-666666666670',
     'California Roll', 'Crab, avocado, cucumber', 380.00, 'https://images.unsplash.com/photo-1579584425555-c3ce17fd4351?w=400',
     false, 20, 'available', 4.8, 210),
    ('77777777-7777-7777-7777-777777777402', '55555555-5555-5555-5555-555555555554', '66666666-6666-6666-6666-666666666670',
     'Veggie Roll', 'Cucumber, avocado, carrot', 320.00, 'https://images.unsplash.com/photo-1617196034796-73dfa7b1fd56?w=400',
     true, 18, 'available', 4.6, 150),
    ('77777777-7777-7777-7777-777777777403', '55555555-5555-5555-5555-555555555554', '66666666-6666-6666-6666-666666666661',
     'Edamame', 'Steamed soybeans', 120.00, 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=400',
     true, 8, 'available', 4.5, 95),
    ('77777777-7777-7777-7777-777777777404', '55555555-5555-5555-5555-555555555554', '66666666-6666-6666-6666-666666666662',
     'Teriyaki Chicken', 'Grilled chicken with teriyaki', 340.00, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400',
     false, 22, 'available', 4.7, 180),
    ('77777777-7777-7777-7777-777777777405', '55555555-5555-5555-5555-555555555554', '66666666-6666-6666-6666-666666666665',
     'Mochi Ice Cream', 'Japanese rice cake dessert', 140.00, 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=400',
     true, 5, 'available', 4.9, 165);

-- ====================================================================
-- RESTAURANT 5 MENU (TACO FIESTA - MEXICAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('77777777-7777-7777-7777-777777777501', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666671',
     'Chicken Tacos', 'Grilled chicken tacos (3 pcs)', 240.00, 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=400',
     false, 15, 'available', 4.6, 140),
    ('77777777-7777-7777-7777-777777777502', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666671',
     'Veggie Burrito', 'Bean and veggie burrito', 220.00, 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f?w=400',
     true, 12, 'available', 4.4, 110),
    ('77777777-7777-7777-7777-777777777503', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666661',
     'Nachos Supreme', 'Loaded nachos with cheese', 200.00, 'https://images.unsplash.com/photo-1513456852971-30c0b8199d4d?w=400',
     true, 10, 'available', 4.5, 125),
    ('77777777-7777-7777-7777-777777777504', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666666',
     'Margarita', 'Classic lime margarita', 180.00, 'https://images.unsplash.com/photo-1514362545857-3bc16c4c7d1b?w=400',
     true, 5, 'available', 4.7, 155),
    ('77777777-7777-7777-7777-777777777505', '55555555-5555-5555-5555-555555555555', '66666666-6666-6666-6666-666666666665',
     'Churros', 'Fried dough with chocolate', 130.00, 'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400',
     true, 8, 'available', 4.6, 135);

-- ====================================================================
-- CREATE CUSTOMER & ADDRESS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, email_verified, phone_verified
) VALUES (
    '33333333-3333-3333-3333-333333333333',
    'customer@oneqlick.com', '+919876543299',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
    'Priya', 'Patel', 'customer', 'active', true, true
) ON CONFLICT (email) DO NOTHING;

INSERT INTO core_mstr_one_qlick_addresses_tbl (
    address_id, user_id, title, address_line1, city, state, postal_code,
    latitude, longitude, is_default
) VALUES (
    '44444444-4444-4444-4444-444444444444',
    '33333333-3333-3333-3333-333333333333',
    'Home', 'Flat 301, Sunshine Apartments', 'Mumbai', 'Maharashtra', '400058',
    19.1334, 72.8397, true
) ON CONFLICT (address_id) DO NOTHING;

-- ====================================================================
-- CREATE SAMPLE ORDERS FOR EACH RESTAURANT
-- ====================================================================

-- Restaurant 1 Orders
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('99999999-9999-9999-9999-999999999101', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555551', '44444444-4444-4444-4444-444444444444',
     'ORD-1001', 600.00, 54.00, 40.00, 694.00, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '5 minutes'),
    ('99999999-9999-9999-9999-999999999102', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555551', '44444444-4444-4444-4444-444444444444',
     'ORD-1002', 500.00, 45.00, 40.00, 585.00, 'card', 'paid', 'preparing',
     CURRENT_TIMESTAMP - INTERVAL '15 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 2 Orders
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('99999999-9999-9999-9999-999999999201', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555552', '44444444-4444-4444-4444-444444444444',
     'ORD-2001', 700.00, 63.00, 30.00, 793.00, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '8 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 3 Orders
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('99999999-9999-9999-9999-999999999301', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555553', '44444444-4444-4444-4444-444444444444',
     'ORD-3001', 430.00, 38.70, 35.00, 503.70, 'upi', 'paid', 'preparing',
     CURRENT_TIMESTAMP - INTERVAL '12 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 4 Orders
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('99999999-9999-9999-9999-999999999401', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555554', '44444444-4444-4444-4444-444444444444',
     'ORD-4001', 700.00, 63.00, 50.00, 813.00, 'card', 'paid', 'ready_for_pickup',
     CURRENT_TIMESTAMP - INTERVAL '20 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 5 Orders
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('99999999-9999-9999-9999-999999999501', '33333333-3333-3333-3333-333333333333',
     '55555555-5555-5555-5555-555555555555', '44444444-4444-4444-4444-444444444444',
     'ORD-5001', 460.00, 41.40, 38.00, 539.40, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '6 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- ====================================================================
-- ORDER ITEMS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    -- Restaurant 1 orders
    ('99999999-9999-9999-9999-999999999101', '77777777-7777-7777-7777-777777777102', 1, 320.00, 320.00),
    ('99999999-9999-9999-9999-999999999101', '77777777-7777-7777-7777-777777777104', 1, 280.00, 280.00),
    -- Restaurant 2 orders
    ('99999999-9999-9999-9999-999999999201', '77777777-7777-7777-7777-777777777201', 2, 350.00, 700.00),
    -- Restaurant 3 orders
    ('99999999-9999-9999-9999-999999999301', '77777777-7777-7777-7777-777777777301', 1, 250.00, 250.00),
    ('99999999-9999-9999-9999-999999999301', '77777777-7777-7777-7777-777777777303', 1, 180.00, 180.00),
    -- Restaurant 4 orders
    ('99999999-9999-9999-9999-999999999401', '77777777-7777-7777-7777-777777777401', 1, 380.00, 380.00),
    ('99999999-9999-9999-9999-999999999401', '77777777-7777-7777-7777-777777777404', 1, 340.00, 340.00),
    -- Restaurant 5 orders
    ('99999999-9999-9999-9999-999999999501', '77777777-7777-7777-7777-777777777501', 1, 240.00, 240.00),
    ('99999999-9999-9999-9999-999999999501', '77777777-7777-7777-7777-777777777503', 1, 200.00, 200.00);

-- ====================================================================
-- SUCCESS MESSAGE
-- ====================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Multiple restaurants setup complete!';
    RAISE NOTICE '';
    RAISE NOTICE '📧 LOGIN CREDENTIALS (All use password: Test@123):';
    RAISE NOTICE '';
    RAISE NOTICE '1️⃣  SPICE KITCHEN (Indian)';
    RAISE NOTICE '   Email: spicekitchen@oneqlick.com';
    RAISE NOTICE '   Location: Mumbai | Rating: 4.5⭐ | 5 menu items';
    RAISE NOTICE '';
    RAISE NOTICE '2️⃣  PIZZA PARADISE (Italian)';
    RAISE NOTICE '   Email: pizzaparadise@oneqlick.com';
    RAISE NOTICE '   Location: Bangalore | Rating: 4.7⭐ | 5 menu items';
    RAISE NOTICE '';
    RAISE NOTICE '3️⃣  BURGER BROS (American)';
    RAISE NOTICE '   Email: burgerbros@oneqlick.com';
    RAISE NOTICE '   Location: Gurgaon | Rating: 4.6⭐ | 5 menu items';
    RAISE NOTICE '';
    RAISE NOTICE '4️⃣  SUSHI STATION (Japanese)';
    RAISE NOTICE '   Email: sushistation@oneqlick.com';
    RAISE NOTICE '   Location: Kolkata | Rating: 4.8⭐ | 5 menu items';
    RAISE NOTICE '';
    RAISE NOTICE '5️⃣  TACO FIESTA (Mexican)';
    RAISE NOTICE '   Email: tacofiesta@oneqlick.com';
    RAISE NOTICE '   Location: Pune | Rating: 4.4⭐ | 5 menu items';
    RAISE NOTICE '';
    RAISE NOTICE '🚀 Total: 5 restaurants, 25 menu items, 6 orders';
    RAISE NOTICE '🔑 Password for all: Test@123';
END $$;
