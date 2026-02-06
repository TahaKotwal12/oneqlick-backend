-- Insert Carousel Coupons for OneQlick (UPPERCASE enum values)
-- These coupons will appear in the home screen carousel

-- First, delete any existing carousel coupons to avoid conflicts
DELETE FROM core_mstr_one_qlick_coupons_tbl WHERE show_in_carousel = TRUE;

-- 1. MEGA SALE - 60% OFF
INSERT INTO core_mstr_one_qlick_coupons_tbl (
    coupon_id, code, title, description, coupon_type, discount_value,
    min_order_amount, max_discount_amount, usage_limit, used_count,
    valid_from, valid_until, is_active, show_in_carousel, carousel_priority,
    carousel_title, carousel_subtitle, carousel_badge, carousel_icon,
    carousel_gradient_start, carousel_gradient_middle, carousel_gradient_end, carousel_action_text
) VALUES (
    gen_random_uuid(), 'MEGA60', 'Save 60% on your first 3 orders',
    'On your first 3 orders above ₹199', 'PERCENTAGE', 60.00, 199.00, 100.00,
    1000, 0, NOW(), NOW() + INTERVAL '30 days', TRUE, TRUE, 5,
    'MEGA SALE', 'Up to 60% OFF', 'LIMITED TIME', 'fire',
    '#4F46E5', '#6366F1', '#818CF8', 'Order Now'
);

-- 2. FREE DELIVERY
INSERT INTO core_mstr_one_qlick_coupons_tbl (
    coupon_id, code, title, description, coupon_type, discount_value,
    min_order_amount, max_discount_amount, usage_limit, used_count,
    valid_from, valid_until, is_active, show_in_carousel, carousel_priority,
    carousel_title, carousel_subtitle, carousel_badge, carousel_icon,
    carousel_gradient_start, carousel_gradient_middle, carousel_gradient_end, carousel_action_text
) VALUES (
    gen_random_uuid(), 'FREEDEL', 'Free Delivery on orders above ₹299',
    'On orders above ₹299 from top restaurants', 'FREE_DELIVERY', 0.00, 299.00, NULL,
    5000, 0, NOW(), NOW() + INTERVAL '30 days', TRUE, TRUE, 4,
    'FREE DELIVERY', 'No delivery charges', 'POPULAR', 'truck-delivery',
    '#10B981', '#34D399', '#6EE7B7', 'Browse Restaurants'
);

-- 3. FLAT ₹100 OFF - Weekend Special
INSERT INTO core_mstr_one_qlick_coupons_tbl (
    coupon_id, code, title, description, coupon_type, discount_value,
    min_order_amount, max_discount_amount, usage_limit, used_count,
    valid_from, valid_until, is_active, show_in_carousel, carousel_priority,
    carousel_title, carousel_subtitle, carousel_badge, carousel_icon,
    carousel_gradient_start, carousel_gradient_middle, carousel_gradient_end, carousel_action_text
) VALUES (
    gen_random_uuid(), 'WEEK100', 'Flat ₹100 OFF on weekend orders',
    'Valid on minimum order of ₹500', 'FIXED_AMOUNT', 100.00, 500.00, NULL,
    2000, 0, NOW(), NOW() + INTERVAL '30 days', TRUE, TRUE, 3,
    'FLAT ₹100 OFF', 'Weekend Special', 'WEEKEND', 'percent',
    '#3B82F6', '#60A5FA', '#93C5FD', 'Grab Deal'
);

-- 4. CASHBACK ₹50 - UPI Payment
INSERT INTO core_mstr_one_qlick_coupons_tbl (
    coupon_id, code, title, description, coupon_type, discount_value,
    min_order_amount, max_discount_amount, usage_limit, used_count,
    valid_from, valid_until, is_active, show_in_carousel, carousel_priority,
    carousel_title, carousel_subtitle, carousel_badge, carousel_icon,
    carousel_gradient_start, carousel_gradient_middle, carousel_gradient_end, carousel_action_text
) VALUES (
    gen_random_uuid(), 'UPI50', 'Get ₹50 cashback on UPI payments',
    'Get instant cashback on UPI payments', 'FIXED_AMOUNT', 50.00, 200.00, NULL,
    3000, 0, NOW(), NOW() + INTERVAL '30 days', TRUE, TRUE, 2,
    'CASHBACK ₹50', 'Pay with UPI', 'INSTANT', 'wallet',
    '#8B5CF6', '#A78BFA', '#C4B5FD', 'Pay Now'
);

-- 5. COMBO DEALS - Buy 1 Get 1
INSERT INTO core_mstr_one_qlick_coupons_tbl (
    coupon_id, code, title, description, coupon_type, discount_value,
    min_order_amount, max_discount_amount, usage_limit, used_count,
    valid_from, valid_until, is_active, show_in_carousel, carousel_priority,
    carousel_title, carousel_subtitle, carousel_badge, carousel_icon,
    carousel_gradient_start, carousel_gradient_middle, carousel_gradient_end, carousel_action_text
) VALUES (
    gen_random_uuid(), 'BOGO50', 'Buy 1 Get 1 - 50% OFF on second item',
    'On selected items from partner restaurants', 'PERCENTAGE', 50.00, 300.00, 150.00,
    1500, 0, NOW(), NOW() + INTERVAL '30 days', TRUE, TRUE, 1,
    'COMBO DEALS', 'Buy 1 Get 1 FREE', 'HOT DEAL', 'food-variant',
    '#FB923C', '#FDBA74', '#FED7AA', 'View Combos'
);

-- Verify the inserted coupons
SELECT code, carousel_title, coupon_type::TEXT
FROM core_mstr_one_qlick_coupons_tbl
WHERE show_in_carousel = TRUE
ORDER BY carousel_priority DESC;
