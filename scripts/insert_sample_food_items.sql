-- ====================================================================
-- INSERT SAMPLE FOOD ITEMS FOR RESTAURANTS
-- OneQlick Food Delivery Application
-- ====================================================================

-- This script inserts food items for all 10 restaurants
-- Run this AFTER running insert_sample_restaurants.sql

-- ====================================================================
-- RESTAURANT 1: SPICE GARDEN (North Indian, Mughlai)
-- Restaurant ID: 11111111-1111-1111-1111-111111111111
-- ====================================================================

-- Get category IDs first (we'll use these in INSERT statements)
-- You may need to adjust these based on actual category_ids from your database

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    -- Appetizers
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Appetizers' LIMIT 1),
        'Paneer Tikka',
        'Cottage cheese cubes marinated in spiced yogurt and grilled to perfection',
        180.00,
        160.00,
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
        TRUE,
        'Paneer, Yogurt, Spices, Bell Peppers, Onions',
        'Dairy',
        250,
        15,
        'available',
        4.6,
        120,
        TRUE,
        TRUE,
        '12-15 mins'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Appetizers' LIMIT 1),
        'Chicken 65',
        'Spicy deep-fried chicken with curry leaves and aromatic spices',
        200.00,
        NULL,
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
        FALSE,
        'Chicken, Curry Leaves, Spices, Yogurt',
        'Gluten',
        320,
        18,
        'available',
        4.5,
        98,
        TRUE,
        FALSE,
        '15-18 mins'
    ),
    
    -- Main Course
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Butter Chicken',
        'Tender chicken in rich tomato butter gravy with cream and aromatic spices',
        280.00,
        250.00,
        'https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=400',
        FALSE,
        'Chicken, Tomato, Butter, Cream, Spices, Fenugreek',
        'Dairy, Gluten',
        450,
        25,
        'available',
        4.8,
        234,
        TRUE,
        TRUE,
        '20-25 mins'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Dal Makhani',
        'Slow-cooked black lentils in creamy tomato gravy',
        160.00,
        NULL,
        'https://images.unsplash.com/photo-1546833999-b9f581a1996d?w=400',
        TRUE,
        'Black Lentils, Kidney Beans, Tomato, Cream, Butter',
        'Dairy',
        280,
        15,
        'available',
        4.4,
        156,
        FALSE,
        TRUE,
        '12-15 mins'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Paneer Butter Masala',
        'Cottage cheese cubes in rich creamy tomato gravy',
        240.00,
        220.00,
        'https://images.unsplash.com/photo-1631452180519-c014fe946bc7?w=400',
        TRUE,
        'Paneer, Tomato, Cashews, Cream, Butter, Spices',
        'Dairy, Nuts',
        380,
        20,
        'available',
        4.7,
        189,
        TRUE,
        TRUE,
        '18-20 mins'
    ),
    
    -- Breads
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads' LIMIT 1),
        'Butter Naan',
        'Soft leavened bread brushed with butter, baked in tandoor',
        40.00,
        NULL,
        'https://images.unsplash.com/photo-1619888714543-f80f93fe3a60?w=400',
        TRUE,
        'Refined Flour, Yogurt, Milk, Butter',
        'Gluten, Dairy',
        150,
        8,
        'available',
        4.5,
        245,
        TRUE,
        FALSE,
        '6-8 mins'
    ),
    (
        '11111111-1111-1111-1111-111111111111',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads' LIMIT 1),
        'Garlic Naan',
        'Naan topped with fresh garlic and butter',
        50.00,
        NULL,
        'https://images.unsplash.com/photo-1619888714543-f80f93fe3a60?w=400',
        TRUE,
        'Refined Flour, Garlic, Butter, Coriander',
        'Gluten, Dairy',
        170,
        8,
        'available',
        4.6,
        178,
        TRUE,
        FALSE,
        '6-8 mins'
    );

-- ====================================================================
-- RESTAURANT 2: PIZZA PALACE (Italian, Pizza)
-- Restaurant ID: 22222222-2222-2222-2222-222222222222
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '22222222-2222-2222-2222-222222222222',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Pizza' LIMIT 1),
        'Margherita Pizza',
        'Classic Italian pizza with fresh tomato sauce, mozzarella, and basil',
        320.00,
        280.00,
        'https://images.unsplash.com/photo-1565299624946-b28f40a0ca4b?w=400',
        TRUE,
        'Pizza Dough, Tomato Sauce, Mozzarella Cheese, Basil, Olive Oil',
        'Gluten, Dairy',
        450,
        20,
        'available',
        4.7,
        267,
        TRUE,
        TRUE,
        '18-22 mins'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Pizza' LIMIT 1),
        'Pepperoni Pizza',
        'Loaded with pepperoni, mozzarella cheese, and pizza sauce',
        420.00,
        380.00,
        'https://images.unsplash.com/photo-1628840042765-356cda07504e?w=400',
        FALSE,
        'Pizza Dough, Pepperoni, Mozzarella, Tomato Sauce',
        'Gluten, Dairy, Pork',
        580,
        22,
        'available',
        4.6,
        198,
        TRUE,
        TRUE,
        '20-25 mins'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Pizza' LIMIT 1),
        'Veggie Supreme',
        'Loaded with fresh vegetables, olives, and cheese',
        380.00,
        350.00,
        'https://images.unsplash.com/photo-1571997478779-2adcbbe9ab2f?w=400',
        TRUE,
        'Bell Peppers, Onions, Mushrooms, Olives, Tomatoes, Cheese',
        'Gluten, Dairy',
        420,
        22,
        'available',
        4.5,
        145,
        FALSE,
        TRUE,
        '20-25 mins'
    ),
    (
        '22222222-2222-2222-2222-222222222222',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Appetizers' LIMIT 1),
        'Garlic Bread',
        'Crispy bread topped with garlic butter and herbs',
        120.00,
        NULL,
        'https://images.unsplash.com/photo-1573140401552-3fab0b24306f?w=400',
        TRUE,
        'Bread, Garlic, Butter, Herbs',
        'Gluten, Dairy',
        180,
        10,
        'available',
        4.3,
        89,
        FALSE,
        FALSE,
        '8-10 mins'
    );

-- ====================================================================
-- RESTAURANT 3: BIRYANI HOUSE (Hyderabadi, Biryani)
-- Restaurant ID: 33333333-3333-3333-3333-333333333333
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '33333333-3333-3333-3333-333333333333',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Biryani' LIMIT 1),
        'Hyderabadi Chicken Biryani',
        'Aromatic basmati rice with tender chicken cooked in dum style',
        350.00,
        320.00,
        'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=400',
        FALSE,
        'Basmati Rice, Chicken, Yogurt, Spices, Saffron, Mint',
        'Dairy',
        650,
        35,
        'available',
        4.9,
        567,
        TRUE,
        TRUE,
        '30-35 mins'
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Biryani' LIMIT 1),
        'Hyderabadi Mutton Biryani',
        'Premium mutton pieces with fragrant basmati rice',
        420.00,
        400.00,
        'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=400',
        FALSE,
        'Basmati Rice, Mutton, Yogurt, Spices, Saffron, Mint',
        'Dairy',
        720,
        40,
        'available',
        4.8,
        423,
        TRUE,
        TRUE,
        '35-40 mins'
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Biryani' LIMIT 1),
        'Veg Biryani',
        'Mixed vegetables with aromatic spices and basmati rice',
        220.00,
        200.00,
        'https://images.unsplash.com/photo-1563379091339-03246963d8a9?w=400',
        TRUE,
        'Basmati Rice, Mixed Vegetables, Yogurt, Spices, Saffron',
        'Dairy',
        450,
        25,
        'available',
        4.4,
        234,
        FALSE,
        FALSE,
        '22-25 mins'
    ),
    (
        '33333333-3333-3333-3333-333333333333',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Appetizers' LIMIT 1),
        'Chicken Kebab',
        'Grilled chicken kebab with mint chutney',
        240.00,
        NULL,
        'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400',
        FALSE,
        'Chicken, Yogurt, Spices, Herbs',
        'Dairy',
        280,
        20,
        'available',
        4.6,
        178,
        TRUE,
        FALSE,
        '18-20 mins'
    );

-- ====================================================================
-- RESTAURANT 4: SWEET CORNER (Desserts, Sweets)
-- Restaurant ID: 44444444-4444-4444-4444-444444444444
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '44444444-4444-4444-4444-444444444444',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts' LIMIT 1),
        'Gulab Jamun',
        'Soft milk solids dumplings soaked in rose-flavored sugar syrup',
        80.00,
        NULL,
        'https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=400',
        TRUE,
        'Milk Solids, Sugar, Ghee, Rose Water, Cardamom',
        'Dairy',
        220,
        5,
        'available',
        4.7,
        312,
        TRUE,
        TRUE,
        '2-5 mins'
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts' LIMIT 1),
        'Rasgulla',
        'Soft cottage cheese balls in sugar syrup',
        70.00,
        NULL,
        'https://images.unsplash.com/photo-1606313564558-b8e0e1d79cee?w=400',
        TRUE,
        'Cottage Cheese, Sugar, Cardamom',
        'Dairy',
        180,
        5,
        'available',
        4.5,
        245,
        TRUE,
        FALSE,
        '2-5 mins'
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts' LIMIT 1),
        'Jalebi',
        'Crispy sweet spirals soaked in sugar syrup',
        60.00,
        NULL,
        'https://images.unsplash.com/photo-1626132647523-66f5bf380027?w=400',
        TRUE,
        'Refined Flour, Sugar, Ghee, Saffron',
        'Gluten',
        250,
        10,
        'available',
        4.3,
        189,
        FALSE,
        FALSE,
        '8-10 mins'
    ),
    (
        '44444444-4444-4444-4444-444444444444',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Desserts' LIMIT 1),
        'Kaju Katli',
        'Premium cashew fudge with silver leaf',
        400.00,
        380.00,
        'https://images.unsplash.com/photo-1599599810769-bcde5a160d32?w=400',
        TRUE,
        'Cashews, Sugar, Ghee, Silver Leaf',
        'Nuts',
        420,
        5,
        'available',
        4.8,
        156,
        TRUE,
        TRUE,
        '2-5 mins'
    );

-- ====================================================================
-- RESTAURANT 5: CHAI POINT (Beverages, Snacks)
-- Restaurant ID: 55555555-5555-5555-5555-555555555555
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '55555555-5555-5555-5555-555555555555',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Beverages' LIMIT 1),
        'Masala Chai',
        'Spiced Indian tea with milk, ginger, and aromatic spices',
        30.00,
        NULL,
        'https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400',
        TRUE,
        'Tea, Milk, Ginger, Cardamom, Cloves, Cinnamon',
        'Dairy',
        80,
        5,
        'available',
        4.6,
        423,
        TRUE,
        TRUE,
        '3-5 mins'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Beverages' LIMIT 1),
        'Filter Coffee',
        'South Indian style filter coffee',
        40.00,
        NULL,
        'https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=400',
        TRUE,
        'Coffee, Milk, Sugar',
        'Dairy',
        90,
        5,
        'available',
        4.5,
        267,
        TRUE,
        FALSE,
        '3-5 mins'
    ),
    (
        '55555555-5555-5555-5555-555555555555',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Appetizers' LIMIT 1),
        'Veg Samosa',
        'Crispy pastry filled with spiced potatoes and peas',
        20.00,
        NULL,
        'https://images.unsplash.com/photo-1601050690597-df0568f70950?w=400',
        TRUE,
        'Refined Flour, Potato, Peas, Spices',
        'Gluten',
        150,
        10,
        'available',
        4.4,
        312,
        TRUE,
        FALSE,
        '8-10 mins'
    );

-- ====================================================================
-- RESTAURANT 6: DHABA EXPRESS (Punjabi, North Indian)
-- Restaurant ID: 66666666-6666-6666-6666-666666666666
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '66666666-6666-6666-6666-666666666666',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Tandoori Chicken',
        'Whole chicken marinated in yogurt and spices, cooked in tandoor',
        380.00,
        350.00,
        'https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=400',
        FALSE,
        'Chicken, Yogurt, Tandoori Spices, Lemon',
        'Dairy',
        520,
        30,
        'available',
        4.7,
        298,
        TRUE,
        TRUE,
        '25-30 mins'
    ),
    (
        '66666666-6666-6666-6666-666666666666',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Breads' LIMIT 1),
        'Laccha Paratha',
        'Layered whole wheat bread with crispy texture',
        50.00,
        NULL,
        'https://images.unsplash.com/photo-1619888714543-f80f93fe3a60?w=400',
        TRUE,
        'Whole Wheat Flour, Ghee, Salt',
        'Gluten, Dairy',
        200,
        12,
        'available',
        4.5,
        234,
        TRUE,
        FALSE,
        '10-12 mins'
    );

-- ====================================================================
-- RESTAURANT 7: SOUTH INDIAN DELIGHTS (South Indian)
-- Restaurant ID: 77777777-7777-7777-7777-777777777777
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '77777777-7777-7777-7777-777777777777',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'South Indian' LIMIT 1),
        'Masala Dosa',
        'Crispy rice crepe filled with spiced potato masala',
        90.00,
        NULL,
        'https://images.unsplash.com/photo-1630383249896-424e482df921?w=400',
        TRUE,
        'Rice, Urad Dal, Potato, Spices, Curry Leaves',
        NULL,
        220,
        15,
        'available',
        4.8,
        512,
        TRUE,
        TRUE,
        '12-15 mins'
    ),
    (
        '77777777-7777-7777-7777-777777777777',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'South Indian' LIMIT 1),
        'Idli Sambar',
        'Steamed rice cakes with lentil vegetable stew',
        70.00,
        NULL,
        'https://images.unsplash.com/photo-1589301760014-d929f3979dbc?w=400',
        TRUE,
        'Rice, Urad Dal, Sambar, Coconut Chutney',
        NULL,
        180,
        10,
        'available',
        4.6,
        389,
        TRUE,
        TRUE,
        '8-10 mins'
    ),
    (
        '77777777-7777-7777-7777-777777777777',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'South Indian' LIMIT 1),
        'Vada',
        'Crispy lentil donuts served with chutney and sambar',
        50.00,
        NULL,
        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
        TRUE,
        'Urad Dal, Curry Leaves, Ginger, Chili',
        NULL,
        160,
        12,
        'available',
        4.4,
        267,
        FALSE,
        FALSE,
        '10-12 mins'
    );

-- ====================================================================
-- RESTAURANT 8: DRAGON WOK (Chinese, Asian)
-- Restaurant ID: 88888888-8888-8888-8888-888888888888
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '88888888-8888-8888-8888-888888888888',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Chinese' LIMIT 1),
        'Veg Hakka Noodles',
        'Stir-fried noodles with fresh vegetables and sauces',
        160.00,
        NULL,
        'https://images.unsplash.com/photo-1555126634-323283e090fa?w=400',
        TRUE,
        'Noodles, Cabbage, Carrots, Bell Peppers, Soy Sauce',
        'Gluten, Soy',
        320,
        15,
        'available',
        4.5,
        198,
        TRUE,
        TRUE,
        '12-15 mins'
    ),
    (
        '88888888-8888-8888-8888-888888888888',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Chinese' LIMIT 1),
        'Chicken Manchurian',
        'Crispy chicken balls in spicy Manchurian sauce',
        220.00,
        200.00,
        'https://images.unsplash.com/photo-1585032226651-759b368d7246?w=400',
        FALSE,
        'Chicken, Cornflour, Soy Sauce, Chili Sauce, Ginger-Garlic',
        'Gluten, Soy',
        380,
        20,
        'available',
        4.6,
        234,
        TRUE,
        TRUE,
        '18-20 mins'
    );

-- ====================================================================
-- RESTAURANT 9: BURGER NATION (Fast Food, Burgers)
-- Restaurant ID: 99999999-9999-9999-9999-999999999999
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        '99999999-9999-9999-9999-999999999999',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Fast Food' LIMIT 1),
        'Classic Chicken Burger',
        'Juicy chicken patty with lettuce, tomato, and special sauce',
        180.00,
        160.00,
        'https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=400',
        FALSE,
        'Chicken Patty, Bun, Lettuce, Tomato, Mayo, Cheese',
        'Gluten, Dairy, Egg',
        450,
        15,
        'available',
        4.4,
        267,
        TRUE,
        TRUE,
        '12-15 mins'
    ),
    (
        '99999999-9999-9999-9999-999999999999',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Fast Food' LIMIT 1),
        'Veg Cheese Burger',
        'Crispy veg patty with cheese and fresh vegetables',
        150.00,
        140.00,
        'https://images.unsplash.com/photo-1550547660-d9450f859349?w=400',
        TRUE,
        'Veg Patty, Bun, Cheese, Lettuce, Tomato, Mayo',
        'Gluten, Dairy, Egg',
        380,
        12,
        'available',
        4.3,
        198,
        TRUE,
        FALSE,
        '10-12 mins'
    );

-- ====================================================================
-- RESTAURANT 10: PURE VEG KITCHEN (Gujarati, Rajasthani)
-- Restaurant ID: aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa
-- ====================================================================

INSERT INTO core_mstr_one_qlick_food_items_tbl 
    (restaurant_id, category_id, name, description, price, discount_price, image, is_veg, ingredients, allergens, calories, prep_time, status, rating, total_ratings, is_popular, is_recommended, preparation_time)
VALUES
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Gujarati Thali',
        'Unlimited authentic Gujarati thali with variety of dishes',
        250.00,
        230.00,
        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
        TRUE,
        'Dal, Kadhi, Vegetables, Roti, Rice, Papad, Pickle, Sweet',
        'Dairy, Gluten',
        550,
        20,
        'available',
        4.7,
        412,
        TRUE,
        TRUE,
        '18-20 mins'
    ),
    (
        'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa',
        (SELECT category_id FROM core_mstr_one_qlick_categories_tbl WHERE name = 'Main Course' LIMIT 1),
        'Rajasthani Thali',
        'Royal Rajasthani thali with traditional dishes',
        280.00,
        260.00,
        'https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=400',
        TRUE,
        'Dal Bati Churma, Gatte Ki Sabzi, Ker Sangri, Bajra Roti',
        'Dairy, Gluten',
        620,
        25,
        'available',
        4.6,
        345,
        TRUE,
        TRUE,
        '22-25 mins'
    );

-- ====================================================================
-- VERIFICATION QUERIES
-- ====================================================================

-- Count total food items
SELECT COUNT(*) as total_food_items 
FROM core_mstr_one_qlick_food_items_tbl;

-- Count food items per restaurant
SELECT 
    r.name as restaurant_name,
    COUNT(f.food_item_id) as total_items
FROM 
    core_mstr_one_qlick_restaurants_tbl r
    LEFT JOIN core_mstr_one_qlick_food_items_tbl f ON r.restaurant_id = f.restaurant_id
GROUP BY 
    r.restaurant_id, r.name
ORDER BY 
    total_items DESC;

-- View popular items
SELECT 
    r.name as restaurant_name,
    f.name as food_item_name,
    f.price,
    f.rating,
    f.total_ratings,
    f.is_popular
FROM 
    core_mstr_one_qlick_food_items_tbl f
    INNER JOIN core_mstr_one_qlick_restaurants_tbl r ON f.restaurant_id = r.restaurant_id
WHERE 
    f.is_popular = TRUE
ORDER BY 
    f.rating DESC, f.total_ratings DESC;

-- ====================================================================
-- END OF SCRIPT
-- ====================================================================

-- Total Records Inserted:
-- - Approximately 40+ Food Items across all restaurants
-- - Mix of Vegetarian and Non-Vegetarian items
-- - Items across various categories

COMMIT;

