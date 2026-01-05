-- ====================================================================
-- ONEQLICK - INDIAN RESTAURANTS IN MUMBAI & PUNE
-- ====================================================================
-- 5 Authentic Indian Restaurants with Indian Names
-- All locations: Mumbai & Pune only
-- Auto-generates UUIDs using gen_random_uuid()
-- ====================================================================

-- ====================================================================
-- STEP 1: CREATE CATEGORIES (IF NOT EXISTS)
-- ====================================================================

DO $$
DECLARE
    cat_starters UUID;
    cat_main UUID;
    cat_breads UUID;
    cat_rice UUID;
    cat_street UUID;
    cat_south UUID;
    cat_breakfast UUID;
    cat_desserts UUID;
    cat_beverages UUID;
BEGIN
    -- Check and create categories
    -- Insert categories only if they don't exist
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Starters', 'Appetizers and starters', 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=200', true, 1
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Starters');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Main Course', 'Main dishes', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=200', true, 2
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Breads', 'Indian breads', 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=200', true, 3
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Rice & Biryani', 'Rice dishes', 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=200', true, 4
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Rice & Biryani');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Street Food', 'Mumbai street food', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=200', true, 5
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Street Food');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'South Indian', 'Dosa, Idli, Vada', 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=200', true, 6
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'South Indian');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Breakfast', 'Morning specials', 'https://images.unsplash.com/photo-1533089860892-a7c6f0a88666?w=200', true, 7
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breakfast');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Desserts', 'Indian sweets', 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=200', true, 8
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts');
    
    INSERT INTO core_mstr_one_qlick_categories_tbl (category_id, name, description, image, is_active, sort_order)
    SELECT gen_random_uuid(), 'Beverages', 'Drinks and beverages', 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=200', true, 9
    WHERE NOT EXISTS (SELECT 1 FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Beverages');
    
    RAISE NOTICE '✅ Categories created/verified';
END $$;

-- ====================================================================
-- STEP 2: CREATE RESTAURANTS WITH OWNERS
-- ====================================================================

DO $$
DECLARE
    owner1_id UUID := gen_random_uuid();
    owner2_id UUID := gen_random_uuid();
    owner3_id UUID := gen_random_uuid();
    owner4_id UUID := gen_random_uuid();
    owner5_id UUID := gen_random_uuid();
    
    rest1_id UUID := gen_random_uuid();
    rest2_id UUID := gen_random_uuid();
    rest3_id UUID := gen_random_uuid();
    rest4_id UUID := gen_random_uuid();
    rest5_id UUID := gen_random_uuid();
    
    cat_starters UUID;
    cat_main UUID;
    cat_breads UUID;
    cat_rice UUID;
    cat_street UUID;
    cat_south UUID;
    cat_breakfast UUID;
    cat_desserts UUID;
    cat_beverages UUID;
    
    customer_id UUID := gen_random_uuid();
    address_id UUID := gen_random_uuid();
BEGIN
    -- Get category IDs
    SELECT category_id INTO cat_starters FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Starters';
    SELECT category_id INTO cat_main FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course';
    SELECT category_id INTO cat_breads FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads';
    SELECT category_id INTO cat_rice FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Rice & Biryani';
    SELECT category_id INTO cat_street FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Street Food';
    SELECT category_id INTO cat_south FROM core_mstr_one_qlick_categories_tbl WHERE name = 'South Indian';
    SELECT category_id INTO cat_breakfast FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breakfast';
    SELECT category_id INTO cat_desserts FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts';
    SELECT category_id INTO cat_beverages FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Beverages';
    
    -- ================================================================
    -- RESTAURANT 1: MAHARAJA BHOJNALAYA (MUMBAI - NORTH INDIAN)
    -- ================================================================
    
    -- Create Owner 1 or get existing
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, profile_image, email_verified, phone_verified
    ) VALUES (
        owner1_id, 'maharaja@oneqlick.com', '+919876501001',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Rajesh', 'Sharma', 'restaurant_owner', 'active',
        'https://ui-avatars.com/api/?name=Rajesh+Sharma&background=FF6B35&color=fff',
        true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id (whether just inserted or already exists)
    SELECT user_id INTO owner1_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'maharaja@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        rest1_id, owner1_id, 'Maharaja Bhojnalaya',
        'Royal North Indian cuisine with traditional Mughlai flavors',
        '+919876501001', 'contact@maharaja.com',
        'Shop 15, Linking Road', 'Bandra West', 'Mumbai', 'Maharashtra', '400050',
        19.0596, 72.8295,
        'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
        'North Indian, Mughlai, Punjabi',
        30, 150.00, 40.00, 4.7, 320, 'active', true, '11:00:00', '23:30:00'
    );
    
    -- Menu for Restaurant 1
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (gen_random_uuid(), rest1_id, cat_starters, 'Paneer Tikka', 'Cottage cheese marinated in tandoori spices', 240.00, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400', true, 15, 'available', 4.7, 95),
        (gen_random_uuid(), rest1_id, cat_starters, 'Tandoori Chicken', 'Half chicken marinated in yogurt and spices', 320.00, 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400', false, 25, 'available', 4.8, 150),
        (gen_random_uuid(), rest1_id, cat_main, 'Butter Chicken', 'Creamy tomato-based chicken curry', 350.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400', false, 30, 'available', 4.9, 220),
        (gen_random_uuid(), rest1_id, cat_main, 'Dal Makhani', 'Black lentils cooked overnight with butter', 260.00, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400', true, 35, 'available', 4.6, 180),
        (gen_random_uuid(), rest1_id, cat_breads, 'Garlic Naan', 'Soft bread topped with garlic and butter', 60.00, 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400', true, 10, 'available', 4.7, 200),
        (gen_random_uuid(), rest1_id, cat_rice, 'Chicken Biryani', 'Fragrant basmati rice with spiced chicken', 300.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400', false, 40, 'available', 4.8, 250),
        (gen_random_uuid(), rest1_id, cat_desserts, 'Gulab Jamun', 'Sweet milk dumplings in sugar syrup', 80.00, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', true, 5, 'available', 4.6, 120);
    
    -- ================================================================
    -- RESTAURANT 2: SHIVAJI VADA PAV CENTER (MUMBAI - STREET FOOD)
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, profile_image, email_verified, phone_verified
    ) VALUES (
        owner2_id, 'shivaji@oneqlick.com', '+919876502002',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Ganesh', 'Patil', 'restaurant_owner', 'active',
        'https://ui-avatars.com/api/?name=Ganesh+Patil&background=F4A261&color=fff',
        true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id
    SELECT user_id INTO owner2_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'shivaji@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        rest2_id, owner2_id, 'Shivaji Vada Pav Center',
        'Authentic Mumbai street food - Vada Pav, Pav Bhaji, and more',
        '+919876502002', 'contact@shivaji.com',
        '23, Station Road', 'Dadar East', 'Mumbai', 'Maharashtra', '400014',
        19.0176, 72.8561,
        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
        'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=800',
        'Street Food, Maharashtrian, Fast Food',
        15, 80.00, 25.00, 4.5, 450, 'active', true, '08:00:00', '22:00:00'
    );
    
    -- Menu for Restaurant 2
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (gen_random_uuid(), rest2_id, cat_street, 'Vada Pav', 'Mumbai''s iconic potato fritter in bun', 30.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400', true, 8, 'available', 4.7, 380),
        (gen_random_uuid(), rest2_id, cat_street, 'Pav Bhaji', 'Spiced vegetable mash with buttered buns', 120.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400', true, 15, 'available', 4.8, 420),
        (gen_random_uuid(), rest2_id, cat_street, 'Misal Pav', 'Spicy sprouts curry with bread', 90.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400', true, 12, 'available', 4.6, 290),
        (gen_random_uuid(), rest2_id, cat_street, 'Samosa Pav', 'Crispy samosa served with pav', 40.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400', true, 10, 'available', 4.5, 310),
        (gen_random_uuid(), rest2_id, cat_beverages, 'Cutting Chai', 'Mumbai style half cup tea', 15.00, 'https://images.unsplash.com/photo-1597318130993-c1ca8f24c1e3?w=400', true, 3, 'available', 4.4, 450);
    
    -- ================================================================
    -- RESTAURANT 3: KOLHAPURI KATTA (PUNE - MAHARASHTRIAN)
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, profile_image, email_verified, phone_verified
    ) VALUES (
        owner3_id, 'kolhapuri@oneqlick.com', '+919876503003',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Santosh', 'Deshmukh', 'restaurant_owner', 'active',
        'https://ui-avatars.com/api/?name=Santosh+Deshmukh&background=E76F51&color=fff',
        true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id
    SELECT user_id INTO owner3_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'kolhapuri@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        rest3_id, owner3_id, 'Kolhapuri Katta',
        'Spicy Kolhapuri cuisine - Authentic Maharashtrian flavors',
        '+919876503003', 'contact@kolhapuri.com',
        '45, FC Road', 'Deccan Gymkhana', 'Pune', 'Maharashtra', '411004',
        18.5196, 73.8553,
        'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400',
        'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=800',
        'Maharashtrian, Kolhapuri, Spicy',
        25, 120.00, 30.00, 4.8, 280, 'active', true, '12:00:00', '23:00:00'
    );
    
    -- Menu for Restaurant 3
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (gen_random_uuid(), rest3_id, cat_main, 'Kolhapuri Chicken', 'Fiery spicy chicken curry', 280.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400', false, 30, 'available', 4.9, 180),
        (gen_random_uuid(), rest3_id, cat_main, 'Pandhara Rassa', 'White chicken curry with coconut', 260.00, 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?w=400', false, 28, 'available', 4.7, 140),
        (gen_random_uuid(), rest3_id, cat_main, 'Tambda Rassa', 'Red spicy mutton curry', 320.00, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=400', false, 35, 'available', 4.8, 160),
        (gen_random_uuid(), rest3_id, cat_breads, 'Bhakri', 'Traditional millet flatbread', 40.00, 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400', true, 8, 'available', 4.5, 95),
        (gen_random_uuid(), rest3_id, cat_rice, 'Kolhapuri Mutton Biryani', 'Spicy mutton biryani', 340.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400', false, 45, 'available', 4.9, 200);
    
    -- ================================================================
    -- RESTAURANT 4: SWAAD SOUTH INDIAN (MUMBAI - SOUTH INDIAN)
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, profile_image, email_verified, phone_verified
    ) VALUES (
        owner4_id, 'swaad@oneqlick.com', '+919876504004',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Venkatesh', 'Iyer', 'restaurant_owner', 'active',
        'https://ui-avatars.com/api/?name=Venkatesh+Iyer&background=2A9D8F&color=fff',
        true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id
    SELECT user_id INTO owner4_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'swaad@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        rest4_id, owner4_id, 'Swaad South Indian',
        'Crispy dosas, fluffy idlis, and authentic South Indian delicacies',
        '+919876504004', 'contact@swaad.com',
        '12, Andheri Link Road', 'Andheri West', 'Mumbai', 'Maharashtra', '400053',
        19.1136, 72.8697,
        'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400',
        'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=800',
        'South Indian, Dosa, Idli, Vada',
        20, 100.00, 35.00, 4.6, 380, 'active', true, '07:00:00', '22:30:00'
    );
    
    -- Menu for Restaurant 4
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (gen_random_uuid(), rest4_id, cat_south, 'Masala Dosa', 'Crispy rice crepe with potato filling', 120.00, 'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400', true, 15, 'available', 4.8, 320),
        (gen_random_uuid(), rest4_id, cat_south, 'Idli Sambar', 'Steamed rice cakes with lentil curry (4 pcs)', 80.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400', true, 10, 'available', 4.6, 280),
        (gen_random_uuid(), rest4_id, cat_south, 'Medu Vada', 'Crispy lentil donuts (3 pcs)', 70.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400', true, 12, 'available', 4.7, 240),
        (gen_random_uuid(), rest4_id, cat_south, 'Rava Dosa', 'Crispy semolina crepe', 100.00, 'https://images.unsplash.com/photo-1668236543090-82eba5ee5976?w=400', true, 12, 'available', 4.5, 190),
        (gen_random_uuid(), rest4_id, cat_beverages, 'Filter Coffee', 'Traditional South Indian filter coffee', 40.00, 'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400', true, 5, 'available', 4.9, 350);
    
    -- ================================================================
    -- RESTAURANT 5: PUNE MISAL HOUSE (PUNE - BREAKFAST)
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, profile_image, email_verified, phone_verified
    ) VALUES (
        owner5_id, 'misal@oneqlick.com', '+919876505005',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Prakash', 'Kulkarni', 'restaurant_owner', 'active',
        'https://ui-avatars.com/api/?name=Prakash+Kulkarni&background=E9C46A&color=000',
        true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id
    SELECT user_id INTO owner5_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'misal@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        rest5_id, owner5_id, 'Pune Misal House',
        'Famous Puneri Misal and traditional breakfast items',
        '+919876505005', 'contact@misal.com',
        '78, JM Road', 'Shivajinagar', 'Pune', 'Maharashtra', '411005',
        18.5304, 73.8567,
        'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800',
        'Maharashtrian, Breakfast, Misal',
        18, 90.00, 28.00, 4.4, 250, 'active', true, '06:30:00', '21:00:00'
    );
    
    -- Menu for Restaurant 5
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (gen_random_uuid(), rest5_id, cat_breakfast, 'Puneri Misal', 'Famous spicy Pune style misal', 100.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400', true, 12, 'available', 4.8, 280),
        (gen_random_uuid(), rest5_id, cat_breakfast, 'Poha', 'Flattened rice with peanuts and spices', 60.00, 'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400', true, 10, 'available', 4.6, 220),
        (gen_random_uuid(), rest5_id, cat_breakfast, 'Sabudana Khichdi', 'Tapioca pearls with peanuts', 80.00, 'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400', true, 15, 'available', 4.5, 180),
        (gen_random_uuid(), rest5_id, cat_breakfast, 'Upma', 'Semolina porridge with vegetables', 70.00, 'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400', true, 12, 'available', 4.4, 160),
        (gen_random_uuid(), rest5_id, cat_beverages, 'Lassi', 'Sweet yogurt drink', 50.00, 'https://images.unsplash.com/photo-1556679343-c7306c1976bc?w=400', true, 5, 'available', 4.7, 200);
    
    -- ================================================================
    -- CREATE CUSTOMER & ADDRESS
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, email_verified, phone_verified
    ) VALUES (
        customer_id, 'customer@oneqlick.com', '+919876509999',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Priya', 'Patel', 'customer', 'active', true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    -- Get the actual user_id
    SELECT user_id INTO customer_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'customer@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_addresses_tbl (
        address_id, user_id, title, address_line1, city, state, postal_code,
        latitude, longitude, is_default
    ) VALUES (
        address_id, customer_id, 'Home', 'Flat 301, Sunshine Apartments',
        'Mumbai', 'Maharashtra', '400058', 19.1334, 72.8397, true
    );
    
    -- ================================================================
    -- CREATE SAMPLE ORDERS
    -- ================================================================
    
    -- Orders for Restaurant 1 (Maharaja)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES 
        (gen_random_uuid(), customer_id, rest1_id, address_id, 'ORD-1001',
         650.00, 58.50, 40.00, 748.50, 'upi', 'paid', 'pending',
         CURRENT_TIMESTAMP - INTERVAL '5 minutes'),
        (gen_random_uuid(), customer_id, rest1_id, address_id, 'ORD-1002',
         560.00, 50.40, 40.00, 650.40, 'card', 'paid', 'preparing',
         CURRENT_TIMESTAMP - INTERVAL '15 minutes');
    
    -- Orders for Restaurant 2 (Shivaji)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES 
        (gen_random_uuid(), customer_id, rest2_id, address_id, 'ORD-2001',
         180.00, 16.20, 25.00, 221.20, 'upi', 'paid', 'pending',
         CURRENT_TIMESTAMP - INTERVAL '8 minutes');
    
    -- Orders for Restaurant 3 (Kolhapuri)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES 
        (gen_random_uuid(), customer_id, rest3_id, address_id, 'ORD-3001',
         600.00, 54.00, 30.00, 684.00, 'card', 'paid', 'ready_for_pickup',
         CURRENT_TIMESTAMP - INTERVAL '20 minutes');
    
    -- Orders for Restaurant 4 (Swaad)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES 
        (gen_random_uuid(), customer_id, rest4_id, address_id, 'ORD-4001',
         220.00, 19.80, 35.00, 274.80, 'upi', 'paid', 'preparing',
         CURRENT_TIMESTAMP - INTERVAL '12 minutes');
    
    -- Orders for Restaurant 5 (Misal House)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES 
        (gen_random_uuid(), customer_id, rest5_id, address_id, 'ORD-5001',
         160.00, 14.40, 28.00, 202.40, 'upi', 'paid', 'pending',
         CURRENT_TIMESTAMP - INTERVAL '6 minutes');
    
    RAISE NOTICE '✅ All restaurants, menus, and orders created successfully!';
    RAISE NOTICE '';
    RAISE NOTICE '🍛 5 AUTHENTIC INDIAN RESTAURANTS (Mumbai & Pune)';
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
    RAISE NOTICE '';
    RAISE NOTICE '✅ Setup complete! You can now login to the Partner App!';
END $$;
