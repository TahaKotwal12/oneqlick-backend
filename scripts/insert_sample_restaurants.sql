-- ====================================================================
-- INSERT SAMPLE DATA - RESTAURANTS & OWNERS
-- OneQlick Food Delivery Application
-- ====================================================================

-- NOTE: All passwords are hashed using bcrypt
-- Plain text password for all users: "Restaurant@123"
-- Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W

-- ====================================================================
-- STEP 1: INSERT RESTAURANT OWNER USERS
-- ====================================================================

-- Restaurant Owners (Total: 10 owners for 10 different restaurants)
INSERT INTO core_mstr_one_qlick_users_tbl 
    (user_id, email, phone, password_hash, first_name, last_name, role, status, email_verified, phone_verified, gender, date_of_birth, loyalty_points)
VALUES
    -- Owner 1: Spice Garden (North Indian)
    (
        'a1b2c3d4-e5f6-4a5b-8c9d-1e2f3a4b5c6d',
        'owner.spicegarden@oneqlick.com',
        '+919876543210',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Rajesh',
        'Sharma',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1985-03-15',
        0
    ),
    
    -- Owner 2: Pizza Palace (Italian)
    (
        'b2c3d4e5-f6a7-4b5c-9d0e-2f3a4b5c6d7e',
        'owner.pizzapalace@oneqlick.com',
        '+919876543211',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Giuseppe',
        'Rossi',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1982-07-22',
        0
    ),
    
    -- Owner 3: Biryani House (Hyderabadi)
    (
        'c3d4e5f6-a7b8-4c5d-0e1f-3a4b5c6d7e8f',
        'owner.biryanihouse@oneqlick.com',
        '+919876543212',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Mohammed',
        'Khan',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1988-11-30',
        0
    ),
    
    -- Owner 4: Sweet Corner (Desserts)
    (
        'd4e5f6a7-b8c9-4d5e-1f2a-4b5c6d7e8f9a',
        'owner.sweetcorner@oneqlick.com',
        '+919876543213',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Priya',
        'Mehta',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'female',
        '1990-05-18',
        0
    ),
    
    -- Owner 5: Chai Point (Beverages & Snacks)
    (
        'e5f6a7b8-c9d0-4e5f-2a3b-5c6d7e8f9a0b',
        'owner.chaipoint@oneqlick.com',
        '+919876543214',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Amit',
        'Patel',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1987-09-25',
        0
    ),
    
    -- Owner 6: Dhaba Express (Punjabi)
    (
        'f6a7b8c9-d0e1-4f5a-3b4c-6d7e8f9a0b1c',
        'owner.dhabaexpress@oneqlick.com',
        '+919876543215',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Gurpreet',
        'Singh',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1984-12-10',
        0
    ),
    
    -- Owner 7: South Indian Delights (South Indian)
    (
        'a7b8c9d0-e1f2-4a5b-4c5d-7e8f9a0b1c2d',
        'owner.southindian@oneqlick.com',
        '+919876543216',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Lakshmi',
        'Iyer',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'female',
        '1991-04-08',
        0
    ),
    
    -- Owner 8: Dragon Wok (Chinese)
    (
        'b8c9d0e1-f2a3-4b5c-5d6e-8f9a0b1c2d3e',
        'owner.dragonwok@oneqlick.com',
        '+919876543217',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Wei',
        'Chen',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1986-08-14',
        0
    ),
    
    -- Owner 9: Burger Nation (Fast Food)
    (
        'c9d0e1f2-a3b4-4c5d-6e7f-9a0b1c2d3e4f',
        'owner.burgernation@oneqlick.com',
        '+919876543218',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Arjun',
        'Malhotra',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'male',
        '1989-06-20',
        0
    ),
    
    -- Owner 10: Pure Veg Kitchen (Vegetarian)
    (
        'd0e1f2a3-b4c5-4d5e-7f8a-0b1c2d3e4f5a',
        'owner.pureveg@oneqlick.com',
        '+919876543219',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W',
        'Meera',
        'Gupta',
        'restaurant_owner',
        'active',
        TRUE,
        TRUE,
        'female',
        '1992-02-28',
        0
    );

-- ====================================================================
-- STEP 2: INSERT RESTAURANTS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_restaurants_tbl 
    (restaurant_id, owner_id, name, description, phone, email, address_line1, address_line2, city, state, postal_code, latitude, longitude, image, cover_image, cuisine_type, avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings, status, is_open, opening_time, closing_time, is_veg, is_pure_veg, cost_for_two, platform_fee)
VALUES
    -- Restaurant 1: Spice Garden (Mumbai)
    (
        '11111111-1111-1111-1111-111111111111',
        'a1b2c3d4-e5f6-4a5b-8c9d-1e2f3a4b5c6d',
        'Spice Garden',
        'Authentic North Indian and Mughlai cuisine with traditional recipes passed down through generations. Famous for our butter chicken and dal makhani.',
        '+912222333444',
        'contact@spicegarden.com',
        'Shop 15, MG Road',
        'Near Metro Station',
        'Mumbai',
        'Maharashtra',
        '400001',
        19.0760,
        72.8777,
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=400',
        'North Indian, Mughlai',
        30,
        150.00,
        20.00,
        4.5,
        450,
        'active',
        TRUE,
        '09:00:00',
        '23:00:00',
        FALSE,
        FALSE,
        400.00,
        5.00
    ),
    
    -- Restaurant 2: Pizza Palace (Mumbai)
    (
        '22222222-2222-2222-2222-222222222222',
        'b2c3d4e5-f6a7-4b5c-9d0e-2f3a4b5c6d7e',
        'Pizza Palace',
        'Authentic Italian pizzas with hand-tossed dough and imported ingredients. Wood-fired oven for that perfect crispy crust.',
        '+912222333445',
        'contact@pizzapalace.com',
        '23, Linking Road',
        'Bandra West',
        'Mumbai',
        'Maharashtra',
        '400050',
        19.0596,
        72.8295,
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=300&h=200',
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=800&h=400',
        'Italian, Pizza',
        35,
        200.00,
        30.00,
        4.3,
        320,
        'active',
        TRUE,
        '11:00:00',
        '23:30:00',
        FALSE,
        FALSE,
        500.00,
        5.00
    ),
    
    -- Restaurant 3: Biryani House (Hyderabad)
    (
        '33333333-3333-3333-3333-333333333333',
        'c3d4e5f6-a7b8-4c5d-0e1f-3a4b5c6d7e8f',
        'Biryani House',
        'Authentic Hyderabadi biryani cooked in dum style with premium basmati rice and tender meat. A taste of Nizami heritage.',
        '+914044556677',
        'contact@biryanihouse.com',
        '45, Paradise Circle',
        'Secunderabad',
        'Hyderabad',
        'Telangana',
        '500003',
        17.4435,
        78.5012,
        'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=300&h=200',
        'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=800&h=400',
        'Hyderabadi, Biryani',
        25,
        180.00,
        15.00,
        4.7,
        890,
        'active',
        TRUE,
        '11:00:00',
        '23:00:00',
        FALSE,
        FALSE,
        450.00,
        5.00
    ),
    
    -- Restaurant 4: Sweet Corner (Delhi)
    (
        '44444444-4444-4444-4444-444444444444',
        'd4e5f6a7-b8c9-4d5e-1f2a-4b5c6d7e8f9a',
        'Sweet Corner',
        'Traditional Indian sweets and desserts made with pure ghee and authentic recipes. Specializing in Bengali and North Indian sweets.',
        '+911144556677',
        'contact@sweetcorner.com',
        '12, Chandni Chowk',
        'Old Delhi',
        'New Delhi',
        'Delhi',
        '110006',
        28.6508,
        77.2318,
        'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=300&h=200',
        'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&h=400',
        'Desserts, Sweets',
        20,
        100.00,
        10.00,
        4.2,
        156,
        'active',
        TRUE,
        '08:00:00',
        '22:00:00',
        TRUE,
        TRUE,
        250.00,
        5.00
    ),
    
    -- Restaurant 5: Chai Point (Bangalore)
    (
        '55555555-5555-5555-5555-555555555555',
        'e5f6a7b8-c9d0-4e5f-2a3b-5c6d7e8f9a0b',
        'Chai Point',
        'Premium chai and coffee with fresh snacks. Perfect spot for your tea break with over 20 varieties of tea and coffee.',
        '+918044556677',
        'contact@chaipoint.com',
        '34, MG Road',
        'Near Brigade Road',
        'Bangalore',
        'Karnataka',
        '560001',
        12.9716,
        77.5946,
        'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=200',
        'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=800&h=400',
        'Beverages, Snacks',
        15,
        50.00,
        10.00,
        4.0,
        234,
        'active',
        TRUE,
        '07:00:00',
        '23:00:00',
        TRUE,
        FALSE,
        150.00,
        5.00
    ),
    
    -- Restaurant 6: Dhaba Express (Pune)
    (
        '66666666-6666-6666-6666-666666666666',
        'f6a7b8c9-d0e1-4f5a-3b4c-6d7e8f9a0b1c',
        'Dhaba Express',
        'Highway-style Punjabi dhaba bringing authentic flavors of Punjab to your doorstep. Famous for our tandoori items and parathas.',
        '+912044556677',
        'contact@dhabaexpress.com',
        '78, FC Road',
        'Deccan Gymkhana',
        'Pune',
        'Maharashtra',
        '411004',
        18.5204,
        73.8567,
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=400',
        'Punjabi, North Indian',
        35,
        120.00,
        15.00,
        4.4,
        567,
        'active',
        FALSE,
        '10:00:00',
        '23:00:00',
        FALSE,
        FALSE,
        350.00,
        5.00
    ),
    
    -- Restaurant 7: South Indian Delights (Chennai)
    (
        '77777777-7777-7777-7777-777777777777',
        'a7b8c9d0-e1f2-4a5b-4c5d-7e8f9a0b1c2d',
        'South Indian Delights',
        'Traditional South Indian breakfast and meals. Crispy dosas, fluffy idlis, and aromatic filter coffee prepared with authentic recipes.',
        '+914444556677',
        'contact@southindian.com',
        '56, T Nagar',
        'Near Pondy Bazaar',
        'Chennai',
        'Tamil Nadu',
        '600017',
        13.0418,
        80.2341,
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=300&h=200',
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=800&h=400',
        'South Indian',
        20,
        100.00,
        10.00,
        4.6,
        723,
        'active',
        TRUE,
        '06:00:00',
        '22:00:00',
        TRUE,
        TRUE,
        200.00,
        5.00
    ),
    
    -- Restaurant 8: Dragon Wok (Mumbai)
    (
        '88888888-8888-8888-8888-888888888888',
        'b8c9d0e1-f2a3-4b5c-5d6e-8f9a0b1c2d3e',
        'Dragon Wok',
        'Authentic Chinese cuisine with a modern twist. Specializing in Szechuan, Cantonese, and Indo-Chinese dishes.',
        '+912222333446',
        'contact@dragonwok.com',
        '89, Colaba Causeway',
        'South Mumbai',
        'Mumbai',
        'Maharashtra',
        '400005',
        18.9220,
        72.8347,
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=400',
        'Chinese, Asian',
        30,
        180.00,
        25.00,
        4.3,
        412,
        'active',
        TRUE,
        '12:00:00',
        '23:30:00',
        FALSE,
        FALSE,
        500.00,
        5.00
    ),
    
    -- Restaurant 9: Burger Nation (Delhi)
    (
        '99999999-9999-9999-9999-999999999999',
        'c9d0e1f2-a3b4-4c5d-6e7f-9a0b1c2d3e4f',
        'Burger Nation',
        'Gourmet burgers made with premium ingredients and fresh buns baked daily. American-style fast food with Indian flavors.',
        '+911144556678',
        'contact@burgernation.com',
        '23, Connaught Place',
        'Central Delhi',
        'New Delhi',
        'Delhi',
        '110001',
        28.6280,
        77.2193,
        'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=300&h=200',
        'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=800&h=400',
        'Fast Food, Burgers',
        25,
        150.00,
        20.00,
        4.1,
        289,
        'active',
        TRUE,
        '11:00:00',
        '00:00:00',
        FALSE,
        FALSE,
        400.00,
        5.00
    ),
    
    -- Restaurant 10: Pure Veg Kitchen (Ahmedabad)
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        'd0e1f2a3-b4c5-4d5e-7f8a-0b1c2d3e4f5a',
        'Pure Veg Kitchen',
        'Completely vegetarian restaurant serving Gujarati, Rajasthani, and North Indian thalis. Pure ghee and no onion-garlic options available.',
        '+917944556677',
        'contact@pureveg.com',
        '67, CG Road',
        'Navrangpura',
        'Ahmedabad',
        'Gujarat',
        '380009',
        23.0341,
        72.5502,
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=300&h=200',
        'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=400',
        'Gujarati, Rajasthani, North Indian',
        30,
        200.00,
        15.00,
        4.5,
        634,
        'active',
        TRUE,
        '11:00:00',
        '22:30:00',
        TRUE,
        TRUE,
        350.00,
        5.00
    );

-- ====================================================================
-- STEP 3: INSERT FOOD CATEGORIES (if not exists)
-- ====================================================================

INSERT INTO core_mstr_one_qlick_categories_tbl (name, description, image, is_active, sort_order)
VALUES
    ('Appetizers', 'Starters and appetizers', 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=200', TRUE, 1),
    ('Main Course', 'Main dishes and entrees', 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=200', TRUE, 2),
    ('Desserts', 'Sweet treats and desserts', 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200', TRUE, 3),
    ('Beverages', 'Drinks and beverages', 'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=200', TRUE, 4),
    ('Fast Food', 'Quick and fast food items', 'https://images.unsplash.com/photo-1571091718767-18b5b1457add?w=200', TRUE, 5),
    ('Biryani', 'Rice dishes and biryanis', 'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=200', TRUE, 6),
    ('Chinese', 'Chinese and Asian cuisine', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=200', TRUE, 7),
    ('South Indian', 'South Indian dishes', 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=200', TRUE, 8),
    ('Breads', 'Indian breads and rotis', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=200', TRUE, 9),
    ('Pizza', 'Pizzas and Italian', 'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=200', TRUE, 10),
    ('Sweets', 'Indian sweets and mithai', 'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=200', TRUE, 11),
    ('Street Food', 'Street food and chaat', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=200', TRUE, 12)
ON CONFLICT DO NOTHING;

-- ====================================================================
-- STEP 4: INSERT RESTAURANT OFFERS
-- ====================================================================

INSERT INTO core_mstr_one_qlick_restaurant_offers_tbl 
    (restaurant_id, title, description, discount_type, discount_value, min_order_amount, max_discount_amount, valid_from, valid_until, is_active)
VALUES
    -- Spice Garden Offers
    ('11111111-1111-1111-1111-111111111111', '20% OFF on First Order', 'Get 20% discount on your first order above ₹300', 'percentage', 20.00, 300.00, 100.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    ('11111111-1111-1111-1111-111111111111', 'Free Delivery', 'Free delivery on orders above ₹200', 'free_delivery', 0.00, 200.00, NULL, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Pizza Palace Offers
    ('22222222-2222-2222-2222-222222222222', 'Buy 1 Get 1', '50% off on second pizza of equal or lesser value', 'percentage', 50.00, 400.00, 200.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Biryani House Offers
    ('33333333-3333-3333-3333-333333333333', '15% OFF', 'Get 15% discount on orders above ₹250', 'percentage', 15.00, 250.00, 75.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    ('33333333-3333-3333-3333-333333333333', 'Weekend Special', '₹100 off on orders above ₹500', 'fixed_amount', 100.00, 500.00, 100.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Sweet Corner Offers
    ('44444444-4444-4444-4444-444444444444', 'Festival Special', '25% off on all sweets', 'percentage', 25.00, 150.00, 100.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Chai Point Offers
    ('55555555-5555-5555-5555-555555555555', 'Morning Delight', '10% off on orders before 12 PM', 'percentage', 10.00, 50.00, 30.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Dhaba Express Offers
    ('66666666-6666-6666-6666-666666666666', '30% OFF', 'Flat 30% off on orders above ₹400', 'percentage', 30.00, 400.00, 150.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- South Indian Delights Offers
    ('77777777-7777-7777-7777-777777777777', 'Breakfast Special', '15% off on breakfast combos', 'percentage', 15.00, 100.00, 50.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Dragon Wok Offers
    ('88888888-8888-8888-8888-888888888888', '₹75 OFF', 'Get ₹75 off on orders above ₹350', 'fixed_amount', 75.00, 350.00, 75.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Burger Nation Offers
    ('99999999-9999-9999-9999-999999999999', 'Combo Deal', '20% off on combo meals', 'percentage', 20.00, 250.00, 100.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE),
    
    -- Pure Veg Kitchen Offers
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Thali Special', '₹50 off on unlimited thalis', 'fixed_amount', 50.00, 300.00, 50.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', TRUE);

-- ====================================================================
-- STEP 5: INSERT RESTAURANT FEATURES
-- ====================================================================

INSERT INTO core_mstr_one_qlick_restaurant_features_tbl 
    (restaurant_id, feature_name, feature_value, is_active)
VALUES
    -- Spice Garden Features
    ('11111111-1111-1111-1111-111111111111', 'Free Delivery', 'On orders above ₹200', TRUE),
    ('11111111-1111-1111-1111-111111111111', 'Live Music', 'Every Friday & Saturday', TRUE),
    
    -- Pizza Palace Features
    ('22222222-2222-2222-2222-222222222222', 'Wood Fired Oven', 'Authentic Italian style', TRUE),
    ('22222222-2222-2222-2222-222222222222', 'Outdoor Seating', 'Available', TRUE),
    
    -- Biryani House Features
    ('33333333-3333-3333-3333-333333333333', 'Dum Cooking', 'Traditional method', TRUE),
    ('33333333-3333-3333-3333-333333333333', 'Halal Certified', 'Yes', TRUE),
    
    -- Sweet Corner Features
    ('44444444-4444-4444-4444-444444444444', 'Pure Ghee', 'Used in all sweets', TRUE),
    ('44444444-4444-4444-4444-444444444444', 'Sugar Free Options', 'Available', TRUE),
    
    -- Chai Point Features
    ('55555555-5555-5555-5555-555555555555', 'Fresh Brew', 'Made on order', TRUE),
    ('55555555-5555-5555-5555-555555555555', 'WiFi Available', 'Free for customers', TRUE),
    
    -- Dhaba Express Features
    ('66666666-6666-6666-6666-666666666666', 'Tandoor Special', 'Clay oven items', TRUE),
    ('66666666-6666-6666-6666-666666666666', 'Family Packs', 'Available', TRUE),
    
    -- South Indian Delights Features
    ('77777777-7777-7777-7777-777777777777', 'Filter Coffee', 'Authentic South Indian', TRUE),
    ('77777777-7777-7777-7777-777777777777', 'No Onion Garlic', 'Options available', TRUE),
    
    -- Dragon Wok Features
    ('88888888-8888-8888-8888-888888888888', 'Wok Tossed', 'Fresh and hot', TRUE),
    ('88888888-8888-8888-8888-888888888888', 'MSG Free', 'Yes', TRUE),
    
    -- Burger Nation Features
    ('99999999-9999-9999-9999-999999999999', 'Fresh Buns', 'Baked daily', TRUE),
    ('99999999-9999-9999-9999-999999999999', 'Premium Patties', '100% chicken/veg', TRUE),
    
    -- Pure Veg Kitchen Features
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', '100% Vegetarian', 'Jain options available', TRUE),
    ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa', 'Unlimited Thali', 'Available', TRUE);

-- ====================================================================
-- VERIFICATION QUERIES
-- ====================================================================

-- Count restaurant owners
SELECT COUNT(*) as total_restaurant_owners 
FROM core_mstr_one_qlick_users_tbl 
WHERE role = 'restaurant_owner';

-- Count restaurants
SELECT COUNT(*) as total_restaurants 
FROM core_mstr_one_qlick_restaurants_tbl;

-- View all restaurants with owner details
SELECT 
    r.name as restaurant_name,
    r.city,
    r.cuisine_type,
    r.rating,
    u.first_name || ' ' || u.last_name as owner_name,
    u.email as owner_email
FROM 
    core_mstr_one_qlick_restaurants_tbl r
    INNER JOIN core_mstr_one_qlick_users_tbl u ON r.owner_id = u.user_id
ORDER BY 
    r.city, r.name;

-- View restaurants with their offers count
SELECT 
    r.name as restaurant_name,
    r.city,
    COUNT(o.offer_id) as total_offers
FROM 
    core_mstr_one_qlick_restaurants_tbl r
    LEFT JOIN core_mstr_one_qlick_restaurant_offers_tbl o ON r.restaurant_id = o.restaurant_id
GROUP BY 
    r.restaurant_id, r.name, r.city
ORDER BY 
    total_offers DESC;

-- ====================================================================
-- END OF SCRIPT
-- ====================================================================

-- Total Records Inserted:
-- - 10 Restaurant Owners (Users)
-- - 10 Restaurants
-- - 12 Categories (if not exists)
-- - 12 Restaurant Offers
-- - 20+ Restaurant Features

COMMIT;

