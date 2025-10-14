-- ============================================
-- PUNE & MUMBAI RESTAURANTS DATA
-- 50 Restaurants with Owner Users
-- ============================================

-- First, insert restaurant owner users
-- ============================================

-- Pune Restaurant Owners (25 owners)
INSERT INTO core_mstr_one_qlick_users_tbl (user_id, email, phone, password_hash, first_name, last_name, role, status, email_verified, phone_verified, loyalty_points, created_at, updated_at)
VALUES
-- Pune Owners
('11111111-1111-1111-1111-111111111111', 'raj.deshmukh.pune@oneqlick.com', '+919123456701', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Raj', 'Deshmukh', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111112', 'priya.kulkarni.misal@oneqlick.com', '+919123456702', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Priya', 'Kulkarni', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111113', 'amit.chitale.sweets@oneqlick.com', '+919123456703', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Amit', 'Chitale', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111114', 'fatima.sheikh.biryani@oneqlick.com', '+919123456704', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Fatima', 'Sheikh', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111115', 'harpreet.singh.punjab@oneqlick.com', '+919123456705', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Harpreet', 'Singh', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111116', 'david.chen.chinese@oneqlick.com', '+919123456706', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'David', 'Chen', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111117', 'marco.rossi.pizza@oneqlick.com', '+919123456707', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Marco', 'Rossi', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111118', 'lakshmi.iyer.saravana@oneqlick.com', '+919123456708', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Lakshmi', 'Iyer', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111119', 'rohan.mehta.coffee@oneqlick.com', '+919123456709', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Rohan', 'Mehta', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111120', 'neha.patil.rajdhani@oneqlick.com', '+919123456710', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Neha', 'Patil', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111121', 'vikram.rao.burger@oneqlick.com', '+919123456711', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Vikram', 'Rao', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111122', 'ayesha.khan.nawabi@oneqlick.com', '+919123456712', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Ayesha', 'Khan', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111123', 'arjun.sharma.kathi@oneqlick.com', '+919123456713', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Arjun', 'Sharma', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111124', 'shreya.joshi.sweet@oneqlick.com', '+919123456714', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Shreya', 'Joshi', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111125', 'suresh.naik.coastal@oneqlick.com', '+919123456715', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Suresh', 'Naik', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111126', 'sophia.dsouza.urban@oneqlick.com', '+919123456716', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Sophia', 'D''Souza', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111127', 'karan.bakshi.karachi@oneqlick.com', '+919123456717', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Karan', 'Bakshi', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111128', 'maria.garcia.taco@oneqlick.com', '+919123456718', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Maria', 'Garcia', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111129', 'anjali.verma.juice@oneqlick.com', '+919123456719', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Anjali', 'Verma', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111130', 'tenzin.sherpa.momo@oneqlick.com', '+919123456720', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Tenzin', 'Sherpa', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111131', 'imran.ahmed.kebab@oneqlick.com', '+919123456721', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Imran', 'Ahmed', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111132', 'simran.kaur.paratha@oneqlick.com', '+919123456722', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Simran', 'Kaur', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111133', 'ravi.gupta.healthy@oneqlick.com', '+919123456723', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Ravi', 'Gupta', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111134', 'balwinder.singh.dhaba@oneqlick.com', '+919123456724', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Balwinder', 'Singh', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('11111111-1111-1111-1111-111111111135', 'pooja.agarwal.tandoor@oneqlick.com', '+919123456725', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Pooja', 'Agarwal', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- Mumbai Owners (25 owners)
('22222222-2222-2222-2222-222222222221', 'anil.kapoor.leopold@oneqlick.com', '+919223456726', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Anil', 'Kapoor', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222222', 'deepika.malhotra.pali@oneqlick.com', '+919223456727', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Deepika', 'Malhotra', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222223', 'sanjay.thakur.bbq@oneqlick.com', '+919223456728', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Sanjay', 'Thakur', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222224', 'priyanka.shah.mainland@oneqlick.com', '+919223456729', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Priyanka', 'Shah', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222225', 'rahul.khanna.bombay@oneqlick.com', '+919223456730', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Rahul', 'Khanna', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222226', 'ananya.bhat.prithvi@oneqlick.com', '+919223456731', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Ananya', 'Bhat', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222227', 'vijay.nair.britannia@oneqlick.com', '+919223456732', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Vijay', 'Nair', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222228', 'kavita.reddy.crab@oneqlick.com', '+919223456733', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Kavita', 'Reddy', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222229', 'aryan.desai.behrouz@oneqlick.com', '+919223456734', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Aryan', 'Desai', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222230', 'isha.patel.sigree@oneqlick.com', '+919223456735', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Isha', 'Patel', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222231', 'mohit.chopra.thaker@oneqlick.com', '+919223456736', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Mohit', 'Chopra', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222232', 'nisha.rao.social@oneqlick.com', '+919223456737', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Nisha', 'Rao', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222233', 'karthik.menon.kyani@oneqlick.com', '+919223456738', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Karthik', 'Menon', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222234', 'divya.sinha.taftoon@oneqlick.com', '+919223456739', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Divya', 'Sinha', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222235', 'tarun.jain.sealounge@oneqlick.com', '+919223456740', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Tarun', 'Jain', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222236', 'meera.pillai.yellow@oneqlick.com', '+919223456741', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Meera', 'Pillai', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222237', 'rohan.khosla.copper@oneqlick.com', '+919223456742', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Rohan', 'Khosla', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222238', 'swati.dutta.mahesh@oneqlick.com', '+919223456743', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Swati', 'Dutta', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222239', 'abhishek.roy.sanman@oneqlick.com', '+919223456744', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Abhishek', 'Roy', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222240', 'tanvi.bhatt.woodside@oneqlick.com', '+919223456745', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Tanvi', 'Bhatt', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222241', 'gaurav.mittal.pratap@oneqlick.com', '+919223456746', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Gaurav', 'Mittal', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222242', 'prerna.saxena.chinagarden@oneqlick.com', '+919223456747', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Prerna', 'Saxena', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222243', 'nikhil.pandey.cream@oneqlick.com', '+919223456748', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Nikhil', 'Pandey', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222244', 'ritika.bansal.persian@oneqlick.com', '+919223456749', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Ritika', 'Bansal', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('22222222-2222-2222-2222-222222222245', 'aditya.kumar.olive@oneqlick.com', '+919223456750', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/lewSIxk1wJxdx5LB6', 'Aditya', 'Kumar', 'restaurant_owner', 'active', true, true, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Insert 50 Restaurants (25 in Pune, 25 in Mumbai)
-- ============================================

-- PUNE RESTAURANTS (25)
-- ============================================

INSERT INTO core_mstr_one_qlick_restaurants_tbl (
    restaurant_id, owner_id, name, description, phone, email,
    address_line1, address_line2, city, state, postal_code,
    latitude, longitude, image, cover_image, cuisine_type,
    avg_delivery_time, min_order_amount, delivery_fee, rating, total_ratings,
    status, is_open, opening_time, closing_time, is_veg, is_pure_veg,
    cost_for_two, platform_fee, created_at, updated_at
) VALUES
-- 1. Pune - Koregaon Park
('a1111111-1111-1111-1111-111111111111', '11111111-1111-1111-1111-111111111111', 'Pune Food Paradise', 'Authentic Maharashtrian cuisine with traditional flavors', '+912026123456', 'contact@punefoodparadise.com',
'Shop 15, North Main Road', 'Koregaon Park', 'Pune', 'Maharashtra', '411001',
18.5362, 73.8937, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'Maharashtrian, Indian',
35, 200, 30, 4.5, 1250, 'active', true, '10:00:00', '23:00:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 2. Pune - Shivajinagar
('a1111111-1111-1111-1111-111111111112', '11111111-1111-1111-1111-111111111112', 'Misal House', 'Best Misal Pav in town with authentic taste', '+912026123457', 'info@misalhouse.com',
'Lane 5, FC Road', 'Shivajinagar', 'Pune', 'Maharashtra', '411005',
18.5304, 73.8397, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1552566626-52f8b828add9', 'Maharashtrian, Fast Food',
20, 100, 15, 4.7, 2100, 'active', true, '07:00:00', '22:00:00', true, true, 250, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 3. Pune - Deccan
('a1111111-1111-1111-1111-111111111113', '11111111-1111-1111-1111-111111111113', 'Chitale Bandhu Mithaiwale', 'Famous for sweets and Maharashtrian snacks', '+912025532198', 'orders@chitalebandhu.com',
'1013, Deccan Gymkhana', 'Opposite Ferguson College', 'Pune', 'Maharashtra', '411004',
18.5074, 73.8393, 'https://images.unsplash.com/photo-1559314809-0d155014e29e', 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e', 'Sweets, Desserts, Maharashtrian',
25, 150, 20, 4.8, 3500, 'active', true, '08:00:00', '22:00:00', true, true, 350, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 4. Pune - Hinjewadi
('a1111111-1111-1111-1111-111111111114', '11111111-1111-1111-1111-111111111114', 'Royal Biryani House', 'Hyderabadi and Lucknowi Biryani specialists', '+912066123456', 'royal@biryanihouse.com',
'Phase 1, Rajiv Gandhi Infotech Park', 'Hinjewadi', 'Pune', 'Maharashtra', '411057',
18.5912, 73.7389, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8', 'https://images.unsplash.com/photo-1633945274309-a62d4cfc6c90', 'Biryani, Mughlai, North Indian',
40, 300, 40, 4.6, 1850, 'active', true, '11:00:00', '23:30:00', false, false, 600, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 5. Pune - Viman Nagar
('a1111111-1111-1111-1111-111111111115', '11111111-1111-1111-1111-111111111115', 'Punjab Grill', 'Premium North Indian and Punjabi cuisine', '+912026695432', 'info@punjabgrill.com',
'Phoenix Market City', 'Viman Nagar', 'Pune', 'Maharashtra', '411014',
18.5679, 73.9145, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'North Indian, Punjabi, Tandoor',
35, 400, 35, 4.5, 980, 'active', true, '12:00:00', '23:00:00', false, false, 800, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 6. Pune - Baner
('a1111111-1111-1111-1111-111111111116', '11111111-1111-1111-1111-111111111116', 'China Bowl', 'Authentic Chinese and Asian fusion', '+912027291234', 'orders@chinabowl.com',
'Baner Road, Opposite D-Mart', 'Baner', 'Pune', 'Maharashtra', '411045',
18.5590, 73.7769, 'https://images.unsplash.com/photo-1558030006-450675393462', 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43', 'Chinese, Asian, Thai',
30, 250, 25, 4.4, 1320, 'active', true, '12:00:00', '23:00:00', false, false, 550, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 7. Pune - Camp Area
('a1111111-1111-1111-1111-111111111117', '11111111-1111-1111-1111-111111111117', 'La Pizzeria', 'Wood-fired authentic Italian pizzas', '+912026346789', 'hello@lapizzeria.com',
'East Street, Camp', 'Near Railway Station', 'Pune', 'Maharashtra', '411001',
18.5196, 73.8743, 'https://images.unsplash.com/photo-1574126154517-d1e0d89ef734', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'Italian, Pizza, Pasta',
35, 300, 30, 4.6, 1680, 'active', true, '11:30:00', '23:00:00', false, false, 700, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 8. Pune - Hadapsar
('a1111111-1111-1111-1111-111111111118', '11111111-1111-1111-1111-111111111118', 'Saravana Bhavan', 'Authentic South Indian vegetarian food', '+912026881234', 'info@saravanabhavan-pune.com',
'Magarpatta City', 'Hadapsar', 'Pune', 'Maharashtra', '411028',
18.5175, 73.9288, 'https://images.unsplash.com/photo-1567337710282-00832b415979', 'https://images.unsplash.com/photo-1630409346315-e758c16e7e0f', 'South Indian, Dosa, Idli',
25, 150, 20, 4.7, 2450, 'active', true, '07:00:00', '22:30:00', true, true, 300, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 9. Pune - Kalyani Nagar
('a1111111-1111-1111-1111-111111111119', '11111111-1111-1111-1111-111111111119', 'The Coffee Culture', 'Premium cafe with continental food', '+912066554321', 'hello@coffeculture.com',
'Nagar Road', 'Kalyani Nagar', 'Pune', 'Maharashtra', '411006',
18.5485, 73.9028, 'https://images.unsplash.com/photo-1554118811-1e0d58224f24', 'https://images.unsplash.com/photo-1521017432531-fbd92d768814', 'Cafe, Continental, Coffee',
20, 200, 25, 4.5, 890, 'active', true, '08:00:00', '23:00:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 10. Pune - Kothrud
('a1111111-1111-1111-1111-111111111120', '11111111-1111-1111-1111-111111111120', 'Rajdhani Thali', 'Unlimited authentic Gujarati and Rajasthani thali', '+912025385678', 'contact@rajdhanithali.com',
'Paud Road', 'Kothrud', 'Pune', 'Maharashtra', '411038',
18.5024, 73.8113, 'https://images.unsplash.com/photo-1546833998-877b37c2e5c6', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84', 'Gujarati, Rajasthani, Thali',
30, 250, 25, 4.6, 1560, 'active', true, '11:30:00', '22:30:00', true, true, 450, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 11. Pune - Wakad
('a1111111-1111-1111-1111-111111111121', '11111111-1111-1111-1111-111111111121', 'Burger Street', 'Gourmet burgers and fast food', '+912066778899', 'orders@burgerstreet.com',
'Shankar Kalat Nagar', 'Wakad', 'Pune', 'Maharashtra', '411057',
18.6008, 73.7647, 'https://images.unsplash.com/photo-1571091718767-18b5b1457add', 'https://images.unsplash.com/photo-1550547660-d9450f859349', 'Fast Food, Burgers, Fries',
25, 150, 20, 4.3, 1120, 'active', true, '11:00:00', '23:30:00', false, false, 400, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 12. Pune - Pimpri
('a1111111-1111-1111-1111-111111111122', '11111111-1111-1111-1111-111111111122', 'Nawabi Zaika', 'Authentic Mughlai and Awadhi cuisine', '+912027441234', 'info@nawabizaika.com',
'Pimpri Main Road', 'Near Pimpri Station', 'Pune', 'Maharashtra', '411018',
18.6298, 73.8070, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Mughlai, North Indian, Kebab',
35, 300, 30, 4.5, 980, 'active', true, '12:00:00', '23:30:00', false, false, 650, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 13. Pune - Aundh
('a1111111-1111-1111-1111-111111111123', '11111111-1111-1111-1111-111111111123', 'Kathi Roll Express', 'Best Kolkata-style rolls and wraps', '+912025884567', 'rolls@kathiroll.com',
'IT Park Road', 'Aundh', 'Pune', 'Maharashtra', '411007',
18.5645, 73.8090, 'https://images.unsplash.com/photo-1551024506-0bccd828d307', 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec', 'Rolls, Fast Food, Street Food',
20, 120, 15, 4.4, 1540, 'active', true, '11:00:00', '23:00:00', false, false, 300, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 14. Pune - Hadapsar
('a1111111-1111-1111-1111-111111111124', '11111111-1111-1111-1111-111111111124', 'Sweet Tooth', 'Premium desserts and ice creams', '+912026776543', 'orders@sweettooth.com',
'Seasons Mall', 'Hadapsar', 'Pune', 'Maharashtra', '411028',
18.5014, 73.9265, 'https://images.unsplash.com/photo-1488477181946-6428a0291777', 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e', 'Desserts, Ice Cream, Bakery',
20, 150, 20, 4.6, 1890, 'active', true, '10:00:00', '23:00:00', true, true, 400, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 15. Pune - Kharadi
('a1111111-1111-1111-1111-111111111125', '11111111-1111-1111-1111-111111111125', 'Coastal Delights', 'Fresh seafood and coastal cuisine', '+912066992211', 'info@coastaldelights.com',
'EON Free Zone', 'Kharadi', 'Pune', 'Maharashtra', '411014',
18.5511, 73.9475, 'https://images.unsplash.com/photo-1559847844-5315695dadae', 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62', 'Seafood, Coastal, Fish',
40, 350, 40, 4.5, 720, 'active', true, '12:00:00', '23:00:00', false, false, 750, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 16. Pune - Bavdhan
('a1111111-1111-1111-1111-111111111126', '11111111-1111-1111-1111-111111111126', 'Urban Bites', 'Multi-cuisine continental restaurant', '+912066554422', 'hello@urbanbites.com',
'Chandani Chowk', 'Bavdhan', 'Pune', 'Maharashtra', '411021',
18.5074, 73.7696, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'Continental, Multi-Cuisine',
30, 250, 30, 4.4, 890, 'active', true, '11:00:00', '23:00:00', false, false, 600, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 17. Pune - Swargate
('a1111111-1111-1111-1111-111111111127', '11111111-1111-1111-1111-111111111127', 'Karachi Bakery', 'Famous bakery with biscuits and cakes', '+912024443322', 'orders@karachibakery.com',
'Swargate Plaza', 'Near Bus Stand', 'Pune', 'Maharashtra', '411042',
18.5018, 73.8636, 'https://images.unsplash.com/photo-1509440159596-0249088772ff', 'https://images.unsplash.com/photo-1517433670267-08bbd4be890f', 'Bakery, Desserts, Snacks',
25, 200, 20, 4.7, 2340, 'active', true, '09:00:00', '22:00:00', true, false, 350, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 18. Pune - Kondhwa
('a1111111-1111-1111-1111-111111111128', '11111111-1111-1111-1111-111111111128', 'Taco Fiesta', 'Mexican food and tacos', '+912026557788', 'fiesta@tacofiesta.com',
'NIBM Road', 'Kondhwa', 'Pune', 'Maharashtra', '411048',
18.4621, 73.8964, 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47', 'https://images.unsplash.com/photo-1613514785940-daed07799d3b', 'Mexican, Tacos, Fast Food',
30, 200, 25, 4.3, 670, 'active', true, '12:00:00', '23:00:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 19. Pune - Karve Nagar
('a1111111-1111-1111-1111-111111111129', '11111111-1111-1111-1111-111111111129', 'Fresh Juice Bar', 'Fresh juices and healthy smoothies', '+912025443322', 'health@freshjuice.com',
'Karve Road', 'Karve Nagar', 'Pune', 'Maharashtra', '411052',
18.4889, 73.8186, 'https://images.unsplash.com/photo-1600271886742-f049cd451bba', 'https://images.unsplash.com/photo-1622597467836-f3285f2131b8', 'Juices, Smoothies, Healthy',
15, 80, 10, 4.5, 1230, 'active', true, '07:00:00', '22:00:00', true, true, 200, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 20. Pune - Pimple Saudagar
('a1111111-1111-1111-1111-111111111130', '11111111-1111-1111-1111-111111111130', 'Momo Point', 'Steamed and fried momos specialist', '+912027665544', 'orders@momopoint.com',
'Pimple Saudagar', 'Near Rahatani', 'Pune', 'Maharashtra', '411027',
18.5978, 73.8014, 'https://images.unsplash.com/photo-1534422298391-e4f8c172dddb', 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec', 'Momos, Chinese, Street Food',
20, 100, 15, 4.6, 1890, 'active', true, '11:00:00', '23:00:00', false, false, 250, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 21. Pune - Nigdi
('a1111111-1111-1111-1111-111111111131', '11111111-1111-1111-1111-111111111131', 'Kebab Corner', 'Authentic kebabs and tandoori', '+912027334455', 'info@kebabcorner.com',
'Nigdi Main Road', 'Near Akurdi', 'Pune', 'Maharashtra', '411044',
18.6592, 73.7688, 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783', 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143', 'Kebab, Tandoor, North Indian',
30, 200, 25, 4.5, 1120, 'active', true, '12:00:00', '23:30:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 22. Pune - Warje
('a1111111-1111-1111-1111-111111111132', '11111111-1111-1111-1111-111111111132', 'Punjabi Paratha House', 'Stuffed parathas and Punjabi food', '+912025662233', 'parathas@punjabifood.com',
'Karve Road', 'Warje', 'Pune', 'Maharashtra', '411058',
18.4774, 73.8102, 'https://images.unsplash.com/photo-1601050690597-df0568f70950', 'https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec', 'Punjabi, Paratha, North Indian',
25, 150, 20, 4.4, 980, 'active', true, '07:00:00', '22:30:00', false, false, 300, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 23. Pune - Chinchwad
('a1111111-1111-1111-1111-111111111133', '11111111-1111-1111-1111-111111111133', 'Healthy Bowls', 'Salads, quinoa bowls, healthy food', '+912027889900', 'eat@healthybowls.com',
'Chinchwad East', 'Near Maratha Mandir', 'Pune', 'Maharashtra', '411033',
18.6480, 73.8009, 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd', 'https://images.unsplash.com/photo-1547592180-85f173990554', 'Healthy, Salads, Bowls',
25, 200, 25, 4.6, 670, 'active', true, '09:00:00', '22:00:00', true, true, 450, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 24. Pune - Katraj
('a1111111-1111-1111-1111-111111111134', '11111111-1111-1111-1111-111111111134', 'Highway Dhaba', 'Authentic dhaba-style Punjabi food', '+912024337788', 'info@highwaydhaba.com',
'Mumbai-Pune Highway', 'Katraj', 'Pune', 'Maharashtra', '411046',
18.4388, 73.8657, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Punjabi, Dhaba, Tandoor',
35, 200, 25, 4.5, 1450, 'active', true, '10:00:00', '23:00:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 25. Pune - Yerawada
('a1111111-1111-1111-1111-111111111135', '11111111-1111-1111-1111-111111111135', 'Tandoori Nights', 'Premium tandoori and grills', '+912026776655', 'book@tandoorinights.com',
'Nagar Road', 'Yerawada', 'Pune', 'Maharashtra', '411006',
18.5533, 73.8782, 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143', 'https://images.unsplash.com/photo-1529006557810-274b9b2fc783', 'Tandoor, Grill, North Indian',
30, 300, 30, 4.7, 1780, 'active', true, '12:00:00', '23:30:00', false, false, 700, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- MUMBAI RESTAURANTS (25)
-- ============================================

-- 26. Mumbai - Colaba
('a2222222-2222-2222-2222-222222222221', '22222222-2222-2222-2222-222222222221', 'Leopold Cafe', 'Iconic Mumbai cafe since 1871', '+912222843678', 'info@leopoldcafe.com',
'Shahid Bhagat Singh Road', 'Colaba', 'Mumbai', 'Maharashtra', '400001',
18.9216, 72.8318, 'https://images.unsplash.com/photo-1521017432531-fbd92d768814', 'https://images.unsplash.com/photo-1554118811-1e0d58224f24', 'Continental, Cafe, Multi-Cuisine',
30, 300, 35, 4.6, 4500, 'active', true, '08:00:00', '00:00:00', false, false, 800, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 27. Mumbai - Bandra West
('a2222222-2222-2222-2222-222222222222', '22222222-2222-2222-2222-222222222222', 'Pali Village Cafe', 'Premium European and Continental', '+912226423456', 'hello@palivillage.com',
'Pali Hill, Union Park', 'Bandra West', 'Mumbai', 'Maharashtra', '400050',
19.0565, 72.8299, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'European, Continental, Cafe',
35, 400, 40, 4.7, 2890, 'active', true, '08:00:00', '23:30:00', false, false, 900, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 28. Mumbai - Andheri West
('a2222222-2222-2222-2222-222222222223', '22222222-2222-2222-2222-222222222223', 'Barbeque Nation', 'Live grill and buffet restaurant', '+912266777888', 'andheri@barbeque.com',
'Lokhandwala Complex', 'Andheri West', 'Mumbai', 'Maharashtra', '400053',
19.1387, 72.8366, 'https://images.unsplash.com/photo-1544025162-d76694265947', 'https://images.unsplash.com/photo-1559339352-11d035aa65de', 'Barbecue, Grill, North Indian',
40, 500, 40, 4.5, 3200, 'active', true, '12:00:00', '23:30:00', false, false, 1000, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 29. Mumbai - Powai
('a2222222-2222-2222-2222-222222222224', '22222222-2222-2222-2222-222222222224', 'Mainland China', 'Authentic Chinese cuisine', '+912225707654', 'powai@mainlandchina.com',
'R City Mall', 'Powai', 'Mumbai', 'Maharashtra', '400076',
19.1176, 72.9060, 'https://images.unsplash.com/photo-1558030006-450675393462', 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43', 'Chinese, Asian, Dim Sum',
35, 400, 40, 4.6, 2100, 'active', true, '12:00:00', '23:00:00', false, false, 850, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 30. Mumbai - Lower Parel
('a2222222-2222-2222-2222-222222222225', '22222222-2222-2222-2222-222222222225', 'The Bombay Canteen', 'Modern Indian cuisine', '+912249666666', 'reservations@thebombaycanteen.com',
'Kamala Mills Compound', 'Lower Parel', 'Mumbai', 'Maharashtra', '400013',
19.0001, 72.8305, 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Indian, Modern Cuisine',
35, 500, 45, 4.8, 3500, 'active', true, '12:00:00', '00:00:00', false, false, 1200, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 31. Mumbai - Juhu
('a2222222-2222-2222-2222-222222222226', '22222222-2222-2222-2222-222222222226', 'Prithvi Cafe', 'Famous Juhu cafe with variety', '+912226149546', 'contact@prithvicafe.com',
'Prithvi Theatre, Juhu Church Road', 'Juhu', 'Mumbai', 'Maharashtra', '400049',
19.1075, 72.8263, 'https://images.unsplash.com/photo-1554118811-1e0d58224f24', 'https://images.unsplash.com/photo-1521017432531-fbd92d768814', 'Cafe, Continental, Snacks',
25, 200, 30, 4.5, 1890, 'active', true, '09:00:00', '23:00:00', false, false, 500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 32. Mumbai - Fort
('a2222222-2222-2222-2222-222222222227', '22222222-2222-2222-2222-222222222227', 'Britannia & Co.', 'Iconic Parsi restaurant since 1923', '+912222616264', 'info@britannia.com',
'Wakefield House, Ballard Estate', 'Fort', 'Mumbai', 'Maharashtra', '400001',
18.9359, 72.8363, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0', 'Parsi, Iranian, Cafe',
25, 200, 25, 4.7, 2670, 'active', true, '11:30:00', '16:00:00', false, false, 600, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 33. Mumbai - Worli
('a2222222-2222-2222-2222-222222222228', '22222222-2222-2222-2222-222222222228', 'Ministry of Crab', 'Premium seafood restaurant', '+912240545444', 'worli@ministryofcrab.com',
'Bombay Dyeing Compound', 'Worli', 'Mumbai', 'Maharashtra', '400025',
19.0119, 72.8183, 'https://images.unsplash.com/photo-1559847844-5315695dadae', 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62', 'Seafood, Crab, Asian',
40, 800, 50, 4.8, 1560, 'active', true, '12:00:00', '23:30:00', false, false, 1500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 34. Mumbai - Malad West
('a2222222-2222-2222-2222-222222222229', '22222222-2222-2222-2222-222222222229', 'Behrouz Biryani', 'Royal Biryani experience', '+912228772233', 'orders@behrouz.com',
'Infinity Mall', 'Malad West', 'Mumbai', 'Maharashtra', '400064',
19.1766, 72.8356, 'https://images.unsplash.com/photo-1563379091339-03b21ab4a4f8', 'https://images.unsplash.com/photo-1633945274309-a62d4cfc6c90', 'Biryani, Persian, Mughlai',
35, 300, 35, 4.6, 1890, 'active', true, '12:00:00', '23:00:00', false, false, 650, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 35. Mumbai - Goregaon
('a2222222-2222-2222-2222-222222222230', '22222222-2222-2222-2222-222222222230', 'Sigree Global Grill', 'Global cuisine live grill', '+912226878900', 'goregaon@sigree.com',
'Oberoi Mall', 'Goregaon East', 'Mumbai', 'Maharashtra', '400063',
19.1696, 72.8647, 'https://images.unsplash.com/photo-1544025162-d76694265947', 'https://images.unsplash.com/photo-1559339352-11d035aa65de', 'Grill, Multi-Cuisine, Barbecue',
40, 450, 40, 4.5, 1450, 'active', true, '12:00:00', '23:30:00', false, false, 900, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 36. Mumbai - Dadar
('a2222222-2222-2222-2222-222222222231', '22222222-2222-2222-2222-222222222231', 'Shree Thaker Bhojanalay', 'Authentic Gujarati thali', '+912224308919', 'info@shreethaker.com',
'Dadabhai Naoroji Road', 'Dadar West', 'Mumbai', 'Maharashtra', '400028',
19.0178, 72.8393, 'https://images.unsplash.com/photo-1546833998-877b37c2e5c6', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84', 'Gujarati, Thali, Vegetarian',
25, 200, 25, 4.7, 3200, 'active', true, '11:00:00', '22:30:00', true, true, 400, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 37. Mumbai - Khar
('a2222222-2222-2222-2222-222222222232', '22222222-2222-2222-2222-222222222232', 'Social', 'Cafe, bar and co-working space', '+912226487777', 'khar@socialoffline.in',
'Khar-Danda Road', 'Khar West', 'Mumbai', 'Maharashtra', '400052',
19.0726, 72.8349, 'https://images.unsplash.com/photo-1521017432531-fbd92d768814', 'https://images.unsplash.com/photo-1554118811-1e0d58224f24', 'Cafe, Continental, Asian',
30, 300, 35, 4.4, 2100, 'active', true, '09:00:00', '01:00:00', false, false, 700, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 38. Mumbai - Churchgate
('a2222222-2222-2222-2222-222222222233', '22222222-2222-2222-2222-222222222233', 'Kyani & Co.', 'Heritage Irani cafe since 1904', '+912222667856', 'info@kyani.com',
'JSS Road, Dhobi Talao', 'Churchgate', 'Mumbai', 'Maharashtra', '400020',
18.9320, 72.8292, 'https://images.unsplash.com/photo-1554118811-1e0d58224f24', 'https://images.unsplash.com/photo-1514933651103-005eec06c04b', 'Irani Cafe, Bakery, Parsi',
20, 150, 20, 4.6, 1890, 'active', true, '06:00:00', '20:00:00', false, false, 300, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 39. Mumbai - Santacruz
('a2222222-2222-2222-2222-222222222234', '22222222-2222-2222-2222-222222222234', 'Taftoon Bar & Kitchen', 'Modern Indian bar & kitchen', '+912226608820', 'hello@taftoon.com',
'Nehru Road', 'Santacruz East', 'Mumbai', 'Maharashtra', '400055',
19.0820, 72.8420, 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Indian, North Indian, Bar',
35, 400, 40, 4.5, 1670, 'active', true, '12:00:00', '00:00:00', false, false, 850, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 40. Mumbai - Nariman Point
('a2222222-2222-2222-2222-222222222235', '22222222-2222-2222-2222-222222222235', 'Sea Lounge', 'Taj Mahal Palace hotel lounge', '+912266653366', 'sealounge@tajhotels.com',
'Apollo Bunder', 'Nariman Point', 'Mumbai', 'Maharashtra', '400001',
18.9217, 72.8330, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'Continental, High Tea, Cafe',
30, 800, 50, 4.9, 2890, 'active', true, '07:00:00', '23:00:00', false, false, 1500, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 41. Mumbai - Thane
('a2222222-2222-2222-2222-222222222236', '22222222-2222-2222-2222-222222222236', 'The Yellow Chilli', 'Chef Sanjeev Kapoor restaurant', '+912225849777', 'thane@yellowchilli.com',
'Viviana Mall', 'Thane West', 'Mumbai', 'Maharashtra', '400606',
19.2183, 72.9781, 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0', 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'North Indian, Mughlai',
35, 400, 40, 4.6, 2100, 'active', true, '12:00:00', '23:00:00', false, false, 850, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 42. Mumbai - Borivali
('a2222222-2222-2222-2222-222222222237', '22222222-2222-2222-2222-222222222237', 'Copper Chimney', 'Classic North Indian cuisine', '+912228980808', 'borivali@copperchimney.com',
'IC Colony', 'Borivali West', 'Mumbai', 'Maharashtra', '400103',
19.2307, 72.8567, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143', 'North Indian, Tandoor, Mughlai',
35, 350, 35, 4.5, 1780, 'active', true, '12:00:00', '23:30:00', false, false, 750, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 43. Mumbai - Kandivali
('a2222222-2222-2222-2222-222222222238', '22222222-2222-2222-2222-222222222238', 'Mahesh Lunch Home', 'Famous for seafood and fish', '+912228075055', 'kandivali@maheshlunch.com',
'Thakur Complex', 'Kandivali East', 'Mumbai', 'Maharashtra', '400101',
19.2056, 72.8722, 'https://images.unsplash.com/photo-1559847844-5315695dadae', 'https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62', 'Seafood, Mangalorean, Coastal',
35, 400, 35, 4.7, 2340, 'active', true, '12:00:00', '23:00:00', false, false, 800, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 44. Mumbai - Vashi (Navi Mumbai)
('a2222222-2222-2222-2222-222222222239', '22222222-2222-2222-2222-222222222239', 'Sanman Restaurant', 'Authentic Maharashtrian food', '+912227893456', 'info@sanman.com',
'Sector 17', 'Vashi', 'Mumbai', 'Maharashtra', '400703',
19.0760, 72.9977, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Maharashtrian, Indian',
30, 200, 30, 4.5, 1560, 'active', true, '11:00:00', '22:30:00', false, false, 450, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 45. Mumbai - Mulund
('a2222222-2222-2222-2222-222222222240', '22222222-2222-2222-2222-222222222240', 'Woodside Inn', 'Sports bar and grill', '+912225631234', 'mulund@woodsideinn.com',
'R Mall', 'Mulund West', 'Mumbai', 'Maharashtra', '400080',
19.1859, 72.9564, 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'Continental, Bar, Grill',
35, 350, 35, 4.4, 1120, 'active', true, '12:00:00', '00:00:00', false, false, 750, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 46. Mumbai - Chembur
('a2222222-2222-2222-2222-222222222241', '22222222-2222-2222-2222-222222222241', 'Pratap Lunch Home', 'Classic Mumbai lunch home', '+912225284567', 'info@prataplunch.com',
'Sion Circle', 'Chembur', 'Mumbai', 'Maharashtra', '400022',
19.0433, 72.8637, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0', 'Indian, Thali, North Indian',
25, 200, 25, 4.5, 1450, 'active', true, '11:30:00', '22:00:00', false, false, 400, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 47. Mumbai - Ghatkopar
('a2222222-2222-2222-2222-222222222242', '22222222-2222-2222-2222-222222222242', 'China Garden', 'Indo-Chinese cuisine', '+912225168888', 'orders@chinagarden.com',
'R City Mall', 'Ghatkopar West', 'Mumbai', 'Maharashtra', '400086',
19.0883, 72.9080, 'https://images.unsplash.com/photo-1558030006-450675393462', 'https://images.unsplash.com/photo-1582878826629-29b7ad1cdc43', 'Chinese, Asian, Indo-Chinese',
30, 250, 30, 4.4, 1670, 'active', true, '12:00:00', '23:00:00', false, false, 550, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 48. Mumbai - Ville Parle
('a2222222-2222-2222-2222-222222222243', '22222222-2222-2222-2222-222222222243', 'Cream Centre', 'Multi-cuisine vegetarian', '+912226271111', 'info@creamcentre.com',
'Near Citi Mall', 'Ville Parle West', 'Mumbai', 'Maharashtra', '400056',
19.1029, 72.8383, 'https://images.unsplash.com/photo-1546833998-877b37c2e5c6', 'https://images.unsplash.com/photo-1606491956689-2ea866880c84', 'Vegetarian, Multi-Cuisine, Indian',
30, 300, 30, 4.6, 2100, 'active', true, '11:00:00', '23:00:00', true, true, 600, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 49. Mumbai - Kurla
('a2222222-2222-2222-2222-222222222244', '22222222-2222-2222-2222-222222222244', 'Persian Darbar', 'Authentic Mughlai and Persian', '+912226524567', 'info@persiandarbar.com',
'LBS Marg', 'Kurla West', 'Mumbai', 'Maharashtra', '400070',
19.0728, 72.8826, 'https://images.unsplash.com/photo-1585937421612-70a008356fbe', 'https://images.unsplash.com/photo-1603360946369-dc9bb6258143', 'Mughlai, Persian, Biryani',
35, 300, 30, 4.5, 1890, 'active', true, '12:00:00', '23:30:00', false, false, 650, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),

-- 50. Mumbai - Bhandup
('a2222222-2222-2222-2222-222222222245', '22222222-2222-2222-2222-222222222245', 'Olive & Twist', 'Cafe and fine dining', '+912225962345', 'hello@olivetwist.com',
'LBS Marg', 'Bhandup West', 'Mumbai', 'Maharashtra', '400078',
19.1513, 72.9359, 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4', 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5', 'Continental, Cafe, Italian',
35, 350, 35, 4.5, 980, 'active', true, '11:00:00', '23:00:00', false, false, 750, 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- Display summary
SELECT 
    city,
    COUNT(*) as total_restaurants,
    ROUND(AVG(rating), 2) as avg_rating,
    ROUND(AVG(cost_for_two), 0) as avg_cost_for_two
FROM core_mstr_one_qlick_restaurants_tbl
WHERE restaurant_id::text LIKE 'a%'
GROUP BY city
ORDER BY city;

-- Success message
SELECT '✅ Successfully inserted 50 restaurant owners and 50 restaurants!' as status,
       '25 restaurants in Pune, 25 in Mumbai' as distribution,
       'All restaurants are active and ready to accept orders' as note;

