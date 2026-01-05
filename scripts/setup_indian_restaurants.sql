-- ====================================================================
-- ONEQLICK - INDIAN RESTAURANTS IN MUMBAI & PUNE
-- ====================================================================
-- 5 Authentic Indian Restaurants with Indian Names
-- All locations: Mumbai & Pune only
-- ====================================================================

-- ====================================================================
-- RESTAURANT 1: MAHARAJA BHOJNALAYA (MUMBAI - NORTH INDIAN)
-- ====================================================================

-- Owner 1
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d',
    'maharaja@oneqlick.com',
    '+919876501001',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Rajesh', 'Sharma', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Rajesh+Sharma&background=FF6B35&color=fff',
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
    'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b',
    'a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d',
    'Maharaja Bhojnalaya',
    'Royal North Indian cuisine with traditional Mughlai flavors',
    '+919876501001', 'contact@maharaja.com',
    'Shop 15, Linking Road', 'Bandra West', 'Mumbai', 'Maharashtra', '400050',
    19.0596, 72.8295,
    'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
    'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
    'North Indian, Mughlai, Punjabi',
    30, 150.00, 40.00, 4.7, 320, 'active', true, '11:00:00', '23:30:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 2: SHIVAJI VADA PAV CENTER (MUMBAI - STREET FOOD)
-- ====================================================================

-- Owner 2
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    'b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e',
    'shivaji@oneqlick.com',
    '+919876502002',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Ganesh', 'Patil', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Ganesh+Patil&background=F4A261&color=fff',
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
    'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f',
    'b2c3d4e5-f6a7-4b8c-9d0e-1f2a3b4c5d6e',
    'Shivaji Vada Pav Center',
    'Authentic Mumbai street food - Vada Pav, Pav Bhaji, and more',
    '+919876502002', 'contact@shivaji.com',
    '23, Station Road', 'Dadar East', 'Mumbai', 'Maharashtra', '400014',
    19.0176, 72.8561,
    'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
    'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800',
    'Street Food, Maharashtrian, Fast Food',
    15, 80.00, 25.00, 4.5, 450, 'active', true, '08:00:00', '22:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 3: KOLHAPURI KATTA (PUNE - MAHARASHTRIAN)
-- ====================================================================

-- Owner 3
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    'd4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a',
    'kolhapuri@oneqlick.com',
    '+919876503003',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Santosh', 'Deshmukh', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Santosh+Deshmukh&background=E76F51&color=fff',
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
    'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b',
    'd4e5f6a7-b8c9-4d0e-1f2a-3b4c5d6e7f8a',
    'Kolhapuri Katta',
    'Spicy Kolhapuri cuisine - Authentic Maharashtrian flavors',
    '+919876503003', 'contact@kolhapuri.com',
    '45, FC Road', 'Deccan Gymkhana', 'Pune', 'Maharashtra', '411004',
    18.5196, 73.8553,
    'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400',
    'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
    'Maharashtrian, Kolhapuri, Spicy',
    25, 120.00, 30.00, 4.8, 280, 'active', true, '12:00:00', '23:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 4: SWAAD SOUTH INDIAN (MUMBAI - SOUTH INDIAN)
-- ====================================================================

-- Owner 4
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    'f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c',
    'swaad@oneqlick.com',
    '+919876504004',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Venkatesh', 'Iyer', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Venkatesh+Iyer&background=2A9D8F&color=fff',
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
    'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d',
    'f6a7b8c9-d0e1-4f2a-3b4c-5d6e7f8a9b0c',
    'Swaad South Indian',
    'Crispy dosas, fluffy idlis, and authentic South Indian delicacies',
    '+919876504004', 'contact@swaad.com',
    '12, Andheri Link Road', 'Andheri West', 'Mumbai', 'Maharashtra', '400053',
    19.1136, 72.8697,
    'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400',
    'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=800',
    'South Indian, Dosa, Idli, Vada',
    20, 100.00, 35.00, 4.6, 380, 'active', true, '07:00:00', '22:30:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 5: PUNE MISAL HOUSE (PUNE - BREAKFAST SPECIALIST)
-- ====================================================================

-- Owner 5
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, profile_image, email_verified, phone_verified
) VALUES (
    'b8c9d0e1-f2a3-4b4c-5d6e-7f8a9b0c1d2e',
    'misal@oneqlick.com',
    '+919876505005',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu', -- Password: Test@123
    'Prakash', 'Kulkarni', 'restaurant_owner', 'active',
    'https://ui-avatars.com/api/?name=Prakash+Kulkarni&background=E9C46A&color=000',
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
    'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f',
    'b8c9d0e1-f2a3-4b4c-5d6e-7f8a9b0c1d2e',
    'Pune Misal House',
    'Famous Puneri Misal and traditional breakfast items',
    '+919876505005', 'contact@misal.com',
    '78, JM Road', 'Shivajinagar', 'Pune', 'Maharashtra', '411005',
    18.5304, 73.8567,
    'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
    'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800',
    'Maharashtrian, Breakfast, Misal',
    18, 90.00, 28.00, 4.4, 250, 'active', true, '06:30:00', '21:00:00'
) ON CONFLICT (restaurant_id) DO NOTHING;

-- ====================================================================
-- CREATE CATEGORIES
-- ====================================================================

INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order) VALUES 
    ('1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d', 'Starters', 'Appetizers and starters', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200', true, 1),
    ('2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e', 'Main Course', 'Main dishes', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200', true, 2),
    ('3c4d5e6f-7a8b-4c9d-0e1f-2a3b4c5d6e7f', 'Breads', 'Indian breads', 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=200', true, 3),
    ('4d5e6f7a-8b9c-4d0e-1f2a-3b4c5d6e7f8a', 'Rice & Biryani', 'Rice dishes', 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200', true, 4),
    ('5e6f7a8b-9c0d-4e1f-2a3b-4c5d6e7f8a9b', 'Street Food', 'Mumbai street food', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=200', true, 5),
    ('6f7a8b9c-0d1e-4f2a-3b4c-5d6e7f8a9b0c', 'South Indian', 'Dosa, Idli, Vada', 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=200', true, 6),
    ('7a8b9c0d-1e2f-4a3b-4c5d-6e7f8a9b0c1d', 'Breakfast', 'Morning specials', 'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=200', true, 7),
    ('8b9c0d1e-2f3a-4b4c-5d6e-7f8a9b0c1d2e', 'Desserts', 'Indian sweets', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=200', true, 8),
    ('9c0d1e2f-3a4b-4c5d-6e7f-8a9b0c1d2e3f', 'Beverages', 'Drinks and beverages', 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=200', true, 9)
ON CONFLICT (category_id) DO NOTHING;

-- ====================================================================
-- RESTAURANT 1 MENU (MAHARAJA BHOJNALAYA - NORTH INDIAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('11a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d',
     'Paneer Tikka', 'Cottage cheese marinated in tandoori spices', 240.00, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400',
     true, 15, 'available', 4.7, 95),
    ('12b3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d',
     'Tandoori Chicken', 'Half chicken marinated in yogurt and spices', 320.00, 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400',
     false, 25, 'available', 4.8, 150),
    ('13c4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e',
     'Butter Chicken', 'Creamy tomato-based chicken curry', 350.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400',
     false, 30, 'available', 4.9, 220),
    ('14d5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '2b3c4d5e-6f7a-4b8c-9d0e-1f2a3b4c5d6e',
     'Dal Makhani', 'Black lentils cooked overnight with butter', 260.00, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400',
     true, 35, 'available', 4.6, 180),
    ('15e6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '3c4d5e6f-7a8b-4c9d-0e1f-2a3b4c5d6e7f',
     'Garlic Naan', 'Soft bread topped with garlic and butter', 60.00, 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400',
     true, 10, 'available', 4.7, 200),
    ('16f7a8b9-c0d1-4e2f-3a4b-5c6d7e8f9a0b', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '4d5e6f7a-8b9c-4d0e-1f2a-3b4c5d6e7f8a',
     'Chicken Biryani', 'Fragrant basmati rice with spiced chicken', 300.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
     false, 40, 'available', 4.8, 250),
    ('17a8b9c0-d1e2-4f3a-4b5c-6d7e8f9a0b1c', 'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', '8b9c0d1e-2f3a-4b4c-5d6e-7f8a9b0c1d2e',
     'Gulab Jamun', 'Sweet milk dumplings in sugar syrup', 80.00, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400',
     true, 5, 'available', 4.6, 120);

-- ====================================================================
-- RESTAURANT 2 MENU (SHIVAJI VADA PAV - STREET FOOD)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('item8b9c-0d1e-4f2a-3b4c-5d6e7f8a9b0c', 'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'cat5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f',
     'Vada Pav', 'Mumbai''s iconic potato fritter in bun', 30.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
     true, 8, 'available', 4.7, 380),
    ('item9c0d-1e2f-4a3b-4c5d-6e7f8a9b0c1d', 'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'cat5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f',
     'Pav Bhaji', 'Spiced vegetable mash with buttered buns', 120.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
     true, 15, 'available', 4.8, 420),
    ('itema0d1-e2f3-4b4c-5d6e-7f8a9b0c1d2e', 'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'cat5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f',
     'Misal Pav', 'Spicy sprouts curry with bread', 90.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
     true, 12, 'available', 4.6, 290),
    ('itemb1e2-f3a4-4c5d-6e7f-8a9b0c1d2e3f', 'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'cat5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f',
     'Samosa Pav', 'Crispy samosa served with pav', 40.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
     true, 10, 'available', 4.5, 310),
    ('itemc2f3-a4b5-4d6e-7f8a-9b0c1d2e3f4a', 'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'cat9c0d1-e2f3-4a4b-5c6d-7e8f9a0b1c2d',
     'Cutting Chai', 'Mumbai style half cup tea', 15.00, 'https://images.unsplash.com/photo-1597318130993-c1ca8f24c1e3?w=400',
     true, 3, 'available', 4.4, 450);

-- ====================================================================
-- RESTAURANT 3 MENU (KOLHAPURI KATTA - MAHARASHTRIAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('itemd3a4-b5c6-4e7f-8a9b-0c1d2e3f4a5b', 'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'cat2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c',
     'Kolhapuri Chicken', 'Fiery spicy chicken curry', 280.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400',
     false, 30, 'available', 4.9, 180),
    ('iteme4b5-c6d7-4f8a-9b0c-1d2e3f4a5b6c', 'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'cat2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c',
     'Pandhara Rassa', 'White chicken curry with coconut', 260.00, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400',
     false, 28, 'available', 4.7, 140),
    ('itemf5c6-d7e8-4a9b-0c1d-2e3f4a5b6c7d', 'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'cat2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c',
     'Tambda Rassa', 'Red spicy mutton curry', 320.00, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400',
     false, 35, 'available', 4.8, 160),
    ('itema6d7-e8f9-4b0c-1d2e-3f4a5b6c7d8e', 'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'cat3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d',
     'Bhakri', 'Traditional millet flatbread', 40.00, 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400',
     true, 8, 'available', 4.5, 95),
    ('itemb7e8-f9a0-4c1d-2e3f-4a5b6c7d8e9f', 'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'cat4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e',
     'Kolhapuri Mutton Biryani', 'Spicy mutton biryani', 340.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400',
     false, 45, 'available', 4.9, 200);

-- ====================================================================
-- RESTAURANT 4 MENU (SWAAD SOUTH INDIAN)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('itemc8f9-a0b1-4d2e-3f4a-5b6c7d8e9f0a', 'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'cat6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a',
     'Masala Dosa', 'Crispy rice crepe with potato filling', 120.00, 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400',
     true, 15, 'available', 4.8, 320),
    ('itemd9a0-b1c2-4e3f-4a5b-6c7d8e9f0a1b', 'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'cat6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a',
     'Idli Sambar', 'Steamed rice cakes with lentil curry (4 pcs)', 80.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
     true, 10, 'available', 4.6, 280),
    ('iteme0b1-c2d3-4f4a-5b6c-7d8e9f0a1b2c', 'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'cat6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a',
     'Medu Vada', 'Crispy lentil donuts (3 pcs)', 70.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
     true, 12, 'available', 4.7, 240),
    ('itemf1c2-d3e4-4a5b-6c7d-8e9f0a1b2c3d', 'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'cat6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a',
     'Rava Dosa', 'Crispy semolina crepe', 100.00, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=400',
     true, 12, 'available', 4.5, 190),
    ('itema2d3-e4f5-4b6c-7d8e-9f0a1b2c3d4e', 'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'cat9c0d1-e2f3-4a4b-5c6d-7e8f9a0b1c2d',
     'Filter Coffee', 'Traditional South Indian filter coffee', 40.00, 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400',
     true, 5, 'available', 4.9, 350);

-- ====================================================================
-- RESTAURANT 5 MENU (PUNE MISAL HOUSE)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl (
    food_item_id, restaurant_id, category_id, name, description, price, image,
    is_veg, prep_time, status, rating, total_ratings
) VALUES 
    ('itemb3e4-f5a6-4c7d-8e9f-0a1b2c3d4e5f', 'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'cat7a8b9-c0d1-4e2f-3a4b-5c6d7e8f9a0b',
     'Puneri Misal', 'Famous spicy Pune style misal', 100.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
     true, 12, 'available', 4.8, 280),
    ('itemc4f5-a6b7-4d8e-9f0a-1b2c3d4e5f6a', 'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'cat7a8b9-c0d1-4e2f-3a4b-5c6d7e8f9a0b',
     'Poha', 'Flattened rice with peanuts and spices', 60.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
     true, 10, 'available', 4.6, 220),
    ('itemd5a6-b7c8-4e9f-0a1b-2c3d4e5f6a7b', 'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'cat7a8b9-c0d1-4e2f-3a4b-5c6d7e8f9a0b',
     'Sabudana Khichdi', 'Tapioca pearls with peanuts', 80.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
     true, 15, 'available', 4.5, 180),
    ('iteme6b7-c8d9-4f0a-1b2c-3d4e5f6a7b8c', 'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'cat7a8b9-c0d1-4e2f-3a4b-5c6d7e8f9a0b',
     'Upma', 'Semolina porridge with vegetables', 70.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
     true, 12, 'available', 4.4, 160),
    ('itemf7c8-d9e0-4a1b-2c3d-4e5f6a7b8c9d', 'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'cat9c0d1-e2f3-4a4b-5c6d-7e8f9a0b1c2d',
     'Lassi', 'Sweet yogurt drink', 50.00, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400',
     true, 5, 'available', 4.7, 200);

-- ====================================================================
-- CREATE CUSTOMER & ADDRESS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id, email, phone, password_hash, first_name, last_name,
    role, status, email_verified, phone_verified
) VALUES (
    'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
    'customer@oneqlick.com', '+919876509999',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
    'Priya', 'Patel', 'customer', 'active', true, true
) ON CONFLICT (email) DO NOTHING;

INSERT INTO core_mstr_one_qlick_addresses_tbl (
    address_id, user_id, title, address_line1, city, state, postal_code,
    latitude, longitude, is_default
) VALUES (
    'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
    'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
    'Home', 'Flat 301, Sunshine Apartments', 'Mumbai', 'Maharashtra', '400058',
    19.1334, 72.8397, true
) ON CONFLICT (address_id) DO NOTHING;

-- ====================================================================
-- CREATE SAMPLE ORDERS
-- ====================================================================

-- Restaurant 1 Orders (Maharaja)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('ord1a2b3-c4d5-4e6f-7a8b-9c0d1e2f3a4b', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-1001', 650.00, 58.50, 40.00, 748.50, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '5 minutes'),
    ('ord2b3c4-d5e6-4f7a-8b9c-0d1e2f3a4b5c', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'f1a2b3c4-d5e6-47f8-9a0b-1c2d3e4f5a6b', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-1002', 560.00, 50.40, 40.00, 650.40, 'card', 'paid', 'preparing',
     CURRENT_TIMESTAMP - INTERVAL '15 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 2 Orders (Shivaji Vada Pav)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('ord3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'c3d4e5f6-a7b8-4c9d-0e1f-2a3b4c5d6e7f', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-2001', 180.00, 16.20, 25.00, 221.20, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '8 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 3 Orders (Kolhapuri)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('ord4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'e5f6a7b8-c9d0-4e1f-2a3b-4c5d6e7f8a9b', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-3001', 600.00, 54.00, 30.00, 684.00, 'card', 'paid', 'ready_for_pickup',
     CURRENT_TIMESTAMP - INTERVAL '20 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 4 Orders (Swaad)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES 
    ('ord5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'a7b8c9d0-e1f2-4a3b-4c5d-6e7f8a9b0c1d', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-4001', 220.00, 19.80, 35.00, 274.80, 'upi', 'paid', 'preparing',
     CURRENT_TIMESTAMP - INTERVAL '12 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- Restaurant 5 Orders (Misal House)
INSERT INTO core_mstr_one_qlick_orders_tbl (
    order_id, customer_id, restaurant_id, delivery_address_id, order_number,
    subtotal, tax_amount, delivery_fee, total_amount, payment_method,
    payment_status, order_status, created_at
) VALUES (
    'ord6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a', 'cust1a2b-3c4d-4e5f-6a7b-8c9d0e1f2a3b',
     'c9d0e1f2-a3b4-4c5d-6e7f-8a9b0c1d2e3f', 'addr1b2c-3d4e-4f5a-6b7c-8d9e0f1a2b3c',
     'ORD-5001', 160.00, 14.40, 28.00, 202.40, 'upi', 'paid', 'pending',
     CURRENT_TIMESTAMP - INTERVAL '6 minutes')
ON CONFLICT (order_id) DO NOTHING;

-- ====================================================================
-- ORDER ITEMS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_order_items_tbl (order_id, food_item_id, quantity, unit_price, total_price) VALUES
    -- Maharaja orders
    ('ord1a2b3-c4d5-4e6f-7a8b-9c0d1e2f3a4b', 'item3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d', 1, 350.00, 350.00),
    ('ord1a2b3-c4d5-4e6f-7a8b-9c0d1e2f3a4b', 'item6f7a-8b9c-4d0e-1f2a-3b4c5d6e7f8a', 1, 300.00, 300.00),
    -- Shivaji orders
    ('ord3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d', 'item9c0d-1e2f-4a3b-4c5d-6e7f8a9b0c1d', 1, 120.00, 120.00),
    ('ord3c4d5-e6f7-4a8b-9c0d-1e2f3a4b5c6d', 'item8b9c-0d1e-4f2a-3b4c-5d6e7f8a9b0c', 2, 30.00, 60.00),
    -- Kolhapuri orders
    ('ord4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e', 'itemd3a4-b5c6-4e7f-8a9b-0c1d2e3f4a5b', 1, 280.00, 280.00),
    ('ord4d5e6-f7a8-4b9c-0d1e-2f3a4b5c6d7e', 'iteme4b5-c6d7-4f8a-9b0c-1d2e3f4a5b6c', 1, 260.00, 260.00),
    -- Swaad orders
    ('ord5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f', 'itemc8f9-a0b1-4d2e-3f4a-5b6c7d8e9f0a', 1, 120.00, 120.00),
    ('ord5e6f7-a8b9-4c0d-1e2f-3a4b5c6d7e8f', 'itemd9a0-b1c2-4e3f-4a5b-6c7d8e9f0a1b', 1, 80.00, 80.00),
    -- Misal House orders
    ('ord6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a', 'itemb3e4-f5a6-4c7d-8e9f-0a1b2c3d4e5f', 1, 100.00, 100.00),
    ('ord6f7a8-b9c0-4d1e-2f3a-4b5c6d7e8f9a', 'itemc4f5-a6b7-4d8e-9f0a-1b2c3d4e5f6a', 1, 60.00, 60.00);

-- ====================================================================
-- SUCCESS MESSAGE
-- ====================================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Indian Restaurants Setup Complete!';
    RAISE NOTICE '';
    RAISE NOTICE '🍛 5 AUTHENTIC INDIAN RESTAURANTS (Mumbai & Pune Only)';
    RAISE NOTICE '';
    RAISE NOTICE '1️⃣  MAHARAJA BHOJNALAYA (North Indian - Mumbai)';
    RAISE NOTICE '   📧 maharaja@oneqlick.com | 🔑 Test@123';
    RAISE NOTICE '   📍 Bandra West, Mumbai | ⭐ 4.7 | 🍽️ 7 items';
    RAISE NOTICE '';
    RAISE NOTICE '2️⃣  SHIVAJI VADA PAV CENTER (Street Food - Mumbai)';
    RAISE NOTICE '   📧 shivaji@oneqlick.com | 🔑 Test@123';
    RAISE NOTICE '   📍 Dadar East, Mumbai | ⭐ 4.5 | 🍽️ 5 items';
    RAISE NOTICE '';
    RAISE NOTICE '3️⃣  KOLHAPURI KATTA (Maharashtrian - Pune)';
    RAISE NOTICE '   📧 kolhapuri@oneqlick.com | 🔑 Test@123';
    RAISE NOTICE '   📍 FC Road, Pune | ⭐ 4.8 | 🍽️ 5 items';
    RAISE NOTICE '';
    RAISE NOTICE '4️⃣  SWAAD SOUTH INDIAN (South Indian - Mumbai)';
    RAISE NOTICE '   📧 swaad@oneqlick.com | 🔑 Test@123';
    RAISE NOTICE '   📍 Andheri West, Mumbai | ⭐ 4.6 | 🍽️ 5 items';
    RAISE NOTICE '';
    RAISE NOTICE '5️⃣  PUNE MISAL HOUSE (Breakfast - Pune)';
    RAISE NOTICE '   📧 misal@oneqlick.com | 🔑 Test@123';
    RAISE NOTICE '   📍 Shivajinagar, Pune | ⭐ 4.4 | 🍽️ 5 items';
    RAISE NOTICE '';
    RAISE NOTICE '📊 Total: 5 Restaurants | 27 Menu Items | 6 Orders';
    RAISE NOTICE '🔑 Password for all: Test@123';
    RAISE NOTICE '🎯 All restaurants in Mumbai & Pune only!';
END $$;
