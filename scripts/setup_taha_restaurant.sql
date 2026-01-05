-- ====================================================================
-- ONEQLICK - RESTAURANT DATA FOR TAHA KOTWAL
-- ====================================================================
-- Creates complete restaurant with menu, offers, and orders
-- Owner: Taha Kotwal (codisisofficial@gmail.com)
-- ====================================================================

DO $$
DECLARE
    owner_user_id UUID := '0b99ca07-6ca5-469c-85c6-fb68aff593dd';
    restaurant_id UUID := gen_random_uuid();
    
    -- Category IDs
    cat_starters UUID;
    cat_main UUID;
    cat_breads UUID;
    cat_rice UUID;
    cat_desserts UUID;
    cat_beverages UUID;
    
    -- Customer for orders
    customer_id UUID := gen_random_uuid();
    address_id UUID := gen_random_uuid();
    
    -- Menu item IDs
    item1_id UUID := gen_random_uuid();
    item2_id UUID := gen_random_uuid();
    item3_id UUID := gen_random_uuid();
    item4_id UUID := gen_random_uuid();
    item5_id UUID := gen_random_uuid();
    item6_id UUID := gen_random_uuid();
    item7_id UUID := gen_random_uuid();
    item8_id UUID := gen_random_uuid();
    
BEGIN
    -- ================================================================
    -- STEP 1: GET CATEGORY IDs
    -- ================================================================
    
    SELECT category_id INTO cat_starters FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Starters';
    SELECT category_id INTO cat_main FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course';
    SELECT category_id INTO cat_breads FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads';
    SELECT category_id INTO cat_rice FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Rice & Biryani';
    SELECT category_id INTO cat_desserts FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts';
    SELECT category_id INTO cat_beverages FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Beverages';
    
    -- ================================================================
    -- STEP 2: CREATE RESTAURANT
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_restaurants_tbl (
        restaurant_id, owner_id, name, description, phone, email,
        address_line1, address_line2, city, state, postal_code,
        latitude, longitude, image, cover_image, cuisine_type,
        avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
        status, is_open, opening_time, closing_time
    ) VALUES (
        restaurant_id,
        owner_user_id,
        'Taha''s Spice Kitchen',
        'Authentic North Indian & Mughlai cuisine with a modern twist. Experience the rich flavors of traditional recipes passed down through generations.',
        '+917219342956',
        'contact@tahasspicekitchen.com',
        'Shop 12, FC Road',
        'Near Deccan Gymkhana',
        'Pune',
        'Maharashtra',
        '411004',
        18.5196,
        73.8553,
        'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=400',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800',
        'North Indian, Mughlai, Punjabi',
        30,
        150.00,
        40.00,
        4.8,
        156,
        'active',
        true,
        '11:00:00',
        '23:30:00'
    );
    
    RAISE NOTICE '✅ Restaurant created: Taha''s Spice Kitchen';
    
    -- ================================================================
    -- STEP 3: CREATE MENU ITEMS
    -- ================================================================
    
    -- Starters
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (item1_id, restaurant_id, cat_starters, 'Paneer Tikka', 'Cottage cheese marinated in tandoori spices, grilled to perfection', 240.00, 'https://images.unsplash.com/photo-1567188040759-fb8a883dc6d8?w=400', true, 15, 'available', 4.7, 89),
        (item2_id, restaurant_id, cat_starters, 'Chicken Tikka', 'Tender chicken pieces marinated in yogurt and spices', 280.00, 'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400', false, 20, 'available', 4.8, 124);
    
    -- Main Course
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (item3_id, restaurant_id, cat_main, 'Butter Chicken', 'Creamy tomato-based chicken curry - our signature dish', 350.00, 'https://images.unsplash.com/photo-1603894584373-5ac82b2ae398?w=400', false, 30, 'available', 4.9, 203),
        (item4_id, restaurant_id, cat_main, 'Dal Makhani', 'Black lentils slow-cooked overnight with butter and cream', 260.00, 'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400', true, 35, 'available', 4.6, 145),
        (item5_id, restaurant_id, cat_main, 'Paneer Butter Masala', 'Cottage cheese in rich tomato and cashew gravy', 290.00, 'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400', true, 25, 'available', 4.7, 167);
    
    -- Breads & Rice
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (item6_id, restaurant_id, cat_breads, 'Garlic Naan', 'Soft naan bread topped with garlic and butter', 60.00, 'https://images.unsplash.com/photo-1619881589935-e0c3d0d2a9e4?w=400', true, 10, 'available', 4.8, 198),
        (item7_id, restaurant_id, cat_rice, 'Chicken Biryani', 'Fragrant basmati rice layered with spiced chicken', 320.00, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8?w=400', false, 40, 'available', 4.9, 234);
    
    -- Desserts
    INSERT INTO core_mstr_one_qlick_food_items_tbl (
        food_item_id, restaurant_id, category_id, name, description, price, image,
        is_veg, prep_time, status, rating, total_ratings
    ) VALUES 
        (item8_id, restaurant_id, cat_desserts, 'Gulab Jamun', 'Sweet milk dumplings soaked in rose-flavored syrup (2 pcs)', 80.00, 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=400', true, 5, 'available', 4.6, 112);
    
    RAISE NOTICE '✅ Created 8 menu items';
    
    -- ================================================================
    -- STEP 4: CREATE OFFERS
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_offers_tbl (
        offer_id, restaurant_id, title, description, discount_type, discount_value,
        min_order_amount, max_discount, start_date, end_date, is_active, usage_limit
    ) VALUES 
        (gen_random_uuid(), restaurant_id, 'WELCOME20', 'Get 20% off on your first order!', 'percentage', 20.00, 200.00, 100.00, CURRENT_DATE, CURRENT_DATE + INTERVAL '30 days', true, 100),
        (gen_random_uuid(), restaurant_id, 'BIRYANI50', 'Flat ₹50 off on Biryani orders above ₹300', 'flat', 50.00, 300.00, 50.00, CURRENT_DATE, CURRENT_DATE + INTERVAL '15 days', true, 50),
        (gen_random_uuid(), restaurant_id, 'WEEKEND30', 'Weekend Special - 30% off on orders above ₹500', 'percentage', 30.00, 500.00, 150.00, CURRENT_DATE, CURRENT_DATE + INTERVAL '7 days', true, null);
    
    RAISE NOTICE '✅ Created 3 offers';
    
    -- ================================================================
    -- STEP 5: CREATE TEST CUSTOMER & ADDRESS
    -- ================================================================
    
    INSERT INTO core_mstr_one_qlick_users_tbl (
        user_id, email, phone, password_hash, first_name, last_name,
        role, status, email_verified, phone_verified
    ) VALUES (
        customer_id,
        'customer.test@oneqlick.com',
        '+919876543210',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzNW6NwZWu',
        'Test', 'Customer', 'customer', 'active', true, true
    ) ON CONFLICT (email) DO NOTHING;
    
    SELECT user_id INTO customer_id FROM core_mstr_one_qlick_users_tbl WHERE email = 'customer.test@oneqlick.com';
    
    INSERT INTO core_mstr_one_qlick_addresses_tbl (
        address_id, user_id, title, address_line1, city, state, postal_code,
        latitude, longitude, is_default
    ) VALUES (
        address_id, customer_id, 'Home', 'Flat 201, Koregaon Park',
        'Pune', 'Maharashtra', '411001', 18.5362, 73.8958, true
    );
    
    RAISE NOTICE '✅ Created test customer';
    
    -- ================================================================
    -- STEP 6: CREATE SAMPLE ORDERS
    -- ================================================================
    
    -- Order 1: Pending (New order - needs acceptance)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES (
        gen_random_uuid(), customer_id, restaurant_id, address_id, 'ORD-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
        670.00, 60.30, 40.00, 770.30, 'upi', 'paid', 'pending',
        CURRENT_TIMESTAMP - INTERVAL '5 minutes'
    );
    
    -- Order 2: Preparing (Accepted and being prepared)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES (
        gen_random_uuid(), customer_id, restaurant_id, address_id, 'ORD-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
        550.00, 49.50, 40.00, 639.50, 'card', 'paid', 'preparing',
        CURRENT_TIMESTAMP - INTERVAL '15 minutes'
    );
    
    -- Order 3: Ready for pickup
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, created_at
    ) VALUES (
        gen_random_uuid(), customer_id, restaurant_id, address_id, 'ORD-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
        320.00, 28.80, 40.00, 388.80, 'upi', 'paid', 'ready_for_pickup',
        CURRENT_TIMESTAMP - INTERVAL '25 minutes'
    );
    
    -- Order 4: Completed (from yesterday)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, rating, created_at
    ) VALUES (
        gen_random_uuid(), customer_id, restaurant_id, address_id, 'ORD-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
        890.00, 80.10, 40.00, 1010.10, 'card', 'paid', 'delivered', 5,
        CURRENT_TIMESTAMP - INTERVAL '1 day'
    );
    
    -- Order 5: Completed (from 2 days ago)
    INSERT INTO core_mstr_one_qlick_orders_tbl (
        order_id, customer_id, restaurant_id, delivery_address_id, order_number,
        subtotal, tax_amount, delivery_fee, total_amount, payment_method,
        payment_status, order_status, rating, created_at
    ) VALUES (
        gen_random_uuid(), customer_id, restaurant_id, address_id, 'ORD-' || LPAD(FLOOR(RANDOM() * 10000)::TEXT, 4, '0'),
        450.00, 40.50, 40.00, 530.50, 'upi', 'paid', 'delivered', 4,
        CURRENT_TIMESTAMP - INTERVAL '2 days'
    );
    
    RAISE NOTICE '✅ Created 5 sample orders';
    
    -- ================================================================
    -- SUCCESS MESSAGE
    -- ================================================================
    
    RAISE NOTICE '========================================';
    RAISE NOTICE 'RESTAURANT SETUP COMPLETE!';
    RAISE NOTICE '========================================';
    RAISE NOTICE 'Restaurant: Tahas Spice Kitchen';
    RAISE NOTICE 'Owner: Taha Kotwal';
    RAISE NOTICE 'Email: codisisofficial@gmail.com';
    RAISE NOTICE 'Password: (Your existing password)';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'Created:';
    RAISE NOTICE '  - 1 Restaurant';
    RAISE NOTICE '  - 8 Menu Items';
    RAISE NOTICE '  - 3 Active Offers';
    RAISE NOTICE '  - 5 Sample Orders';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'Location: FC Road, Pune';
    RAISE NOTICE 'Rating: 4.8 (156 reviews)';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'Order Status:';
    RAISE NOTICE '  - 1 Pending (needs acceptance)';
    RAISE NOTICE '  - 1 Preparing';
    RAISE NOTICE '  - 1 Ready for pickup';
    RAISE NOTICE '  - 2 Delivered';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'Active Offers:';
    RAISE NOTICE '  - WELCOME20 - 20%% off first order';
    RAISE NOTICE '  - BIRYANI50 - Rs.50 off on biryani';
    RAISE NOTICE '  - WEEKEND30 - 30%% weekend discount';
    RAISE NOTICE '----------------------------------------';
    RAISE NOTICE 'You can now login to Partner App!';
    RAISE NOTICE '========================================';
    
    
    
END $$;
