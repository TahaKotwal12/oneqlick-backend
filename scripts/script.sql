-- ====================================================================
-- ENUM TYPES
-- ====================================================================

-- User related enums
CREATE TYPE user_role AS ENUM ('customer', 'admin', 'delivery_partner', 'restaurant_owner');
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');

-- Restaurant related enums
CREATE TYPE restaurant_status AS ENUM ('active', 'inactive', 'suspended');
CREATE TYPE food_status AS ENUM ('available', 'unavailable', 'out_of_stock');

-- Order related enums
CREATE TYPE order_status AS ENUM (
    'pending', 'confirmed', 'preparing', 'ready_for_pickup', 
    'picked_up', 'delivered', 'cancelled', 'refunded'
);
CREATE TYPE payment_status AS ENUM ('pending', 'paid', 'failed', 'refunded');
CREATE TYPE payment_method AS ENUM ('cash', 'card', 'upi', 'wallet');

-- Delivery related enums
CREATE TYPE vehicle_type AS ENUM ('bicycle', 'motorcycle', 'car');
CREATE TYPE availability_status AS ENUM ('available', 'busy', 'offline');

-- Coupon related enums
CREATE TYPE coupon_type AS ENUM ('percentage', 'fixed_amount', 'free_delivery');

-- Notification related enums
CREATE TYPE notification_type AS ENUM ('order_update', 'promotion', 'system');

-- ====================================================================
-- TABLES
-- ====================================================================

-- Users table (customers, admins, delivery partners, restaurant owners)
CREATE TABLE core_mstr_one_qlick_users_tbl (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role user_role NOT NULL,
    status user_status DEFAULT 'active',
    profile_image VARCHAR(500),
    email_verified BOOLEAN DEFAULT FALSE,
    phone_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User addresses
CREATE TABLE core_mstr_one_qlick_addresses_tbl (
    address_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    title VARCHAR(100) NOT NULL, -- Home, Office, etc.
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurants
CREATE TABLE core_mstr_one_qlick_restaurants_tbl (
    restaurant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    phone VARCHAR(20) NOT NULL,
    email VARCHAR(255),
    address_line1 VARCHAR(255) NOT NULL,
    address_line2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) NOT NULL,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    image VARCHAR(500),
    cover_image VARCHAR(500),
    cuisine_type VARCHAR(100),
    avg_delivery_time INTEGER, -- in minutes
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    delivery_fee DECIMAL(10, 2) DEFAULT 0,
    rating DECIMAL(3, 2) DEFAULT 0,
    total_ratings INTEGER DEFAULT 0,
    status restaurant_status DEFAULT 'active',
    is_open BOOLEAN DEFAULT TRUE,
    opening_time TIME,
    closing_time TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food categories
CREATE TABLE core_mstr_one_qlick_categories_tbl (
    category_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    image VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food items
CREATE TABLE core_mstr_one_qlick_food_items_tbl (
    food_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id) ON DELETE CASCADE,
    category_id UUID REFERENCES core_mstr_one_qlick_categories_tbl(category_id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    discount_price DECIMAL(10, 2),
    image VARCHAR(500),
    is_veg BOOLEAN DEFAULT TRUE,
    ingredients TEXT,
    allergens TEXT,
    calories INTEGER,
    prep_time INTEGER, -- in minutes
    status food_status DEFAULT 'available',
    rating DECIMAL(3, 2) DEFAULT 0,
    total_ratings INTEGER DEFAULT 0,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food item variants (size, extras, etc.)
CREATE TABLE core_mstr_one_qlick_food_variants_tbl (
    food_variant_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_item_id UUID REFERENCES core_mstr_one_qlick_food_items_tbl(food_item_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- Small, Medium, Large
    price_adjustment DECIMAL(10, 2) DEFAULT 0,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Orders
CREATE TABLE core_mstr_one_qlick_orders_tbl (
    order_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customer_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id),
    delivery_partner_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    delivery_address_id UUID REFERENCES core_mstr_one_qlick_addresses_tbl(address_id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) DEFAULT 0,
    delivery_fee DECIMAL(10, 2) DEFAULT 0,
    discount_amount DECIMAL(10, 2) DEFAULT 0,
    total_amount DECIMAL(10, 2) NOT NULL,
    payment_method payment_method,
    payment_status payment_status DEFAULT 'pending',
    payment_id VARCHAR(255), -- Payment gateway transaction ID
    order_status order_status DEFAULT 'pending',
    estimated_delivery_time TIMESTAMP,
    actual_delivery_time TIMESTAMP,
    special_instructions TEXT,
    cancellation_reason TEXT,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    review TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order items
CREATE TABLE core_mstr_one_qlick_order_items_tbl (
    order_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id) ON DELETE CASCADE,
    food_item_id UUID REFERENCES core_mstr_one_qlick_food_items_tbl(food_item_id),
    variant_id UUID REFERENCES core_mstr_one_qlick_food_variants_tbl(food_variant_id),
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Delivery partner details
CREATE TABLE core_mstr_one_qlick_delivery_partners_tbl (
    delivery_partner_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    vehicle_type vehicle_type NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL,
    license_number VARCHAR(50) NOT NULL,
    current_latitude DECIMAL(10, 8),
    current_longitude DECIMAL(11, 8),
    availability_status availability_status DEFAULT 'offline',
    rating DECIMAL(3, 2) DEFAULT 0,
    total_ratings INTEGER DEFAULT 0,
    total_deliveries INTEGER DEFAULT 0,
    documents_json JSONB, -- Store document URLs
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order tracking
CREATE TABLE core_mstr_one_qlick_order_tracking_tbl (
    order_tracking_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id) ON DELETE CASCADE,
    status order_status NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Coupons and discounts
CREATE TABLE core_mstr_one_qlick_coupons_tbl (
    coupon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code VARCHAR(50) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    coupon_type coupon_type NOT NULL,
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2),
    usage_limit INTEGER,
    used_count INTEGER DEFAULT 0,
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User coupon usage tracking
CREATE TABLE core_mstr_one_qlick_user_coupon_usage_tbl (
    user_coupon_usage_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    coupon_id UUID REFERENCES core_mstr_one_qlick_coupons_tbl(coupon_id),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id),
    used_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, coupon_id, order_id)
);

-- Reviews and ratings
CREATE TABLE core_mstr_one_qlick_reviews_tbl (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id),
    customer_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id),
    delivery_partner_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    review_type VARCHAR(20) NOT NULL, -- 'restaurant', 'delivery'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notifications
CREATE TABLE core_mstr_one_qlick_notifications_tbl (
    notification_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    notification_type notification_type DEFAULT 'system',
    is_read BOOLEAN DEFAULT FALSE,
    data_json JSONB, -- Additional data
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- AUTHENTICATION TABLES FOR JWT AND OAUTH
-- ====================================================================

-- Refresh tokens table for JWT refresh mechanism
CREATE TABLE core_mstr_one_qlick_refresh_tokens_tbl (
    refresh_token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_revoked BOOLEAN DEFAULT FALSE,
    device_info JSONB, -- Store device fingerprint for security
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- OAuth providers table for social login
CREATE TABLE core_mstr_one_qlick_oauth_providers_tbl (
    oauth_provider_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    provider VARCHAR(50) NOT NULL, -- 'google', 'facebook', 'apple'
    provider_user_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255),
    provider_name VARCHAR(255),
    provider_photo_url VARCHAR(500),
    access_token_hash VARCHAR(255), -- Encrypted access token
    refresh_token_hash VARCHAR(255), -- Encrypted refresh token
    token_expires_at TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(provider, provider_user_id)
);

-- OTP verification table for phone/email verification
CREATE TABLE core_mstr_one_qlick_otp_verifications_tbl (
    otp_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    phone VARCHAR(20),
    email VARCHAR(255),
    otp_code VARCHAR(10) NOT NULL,
    otp_type VARCHAR(20) NOT NULL, -- 'phone_verification', 'email_verification', 'password_reset'
    expires_at TIMESTAMP NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    attempts INTEGER DEFAULT 0,
    max_attempts INTEGER DEFAULT 3,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User sessions table for tracking active sessions
CREATE TABLE core_mstr_one_qlick_user_sessions_tbl (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    device_id VARCHAR(255) NOT NULL,
    device_name VARCHAR(255),
    device_type VARCHAR(50), -- 'mobile', 'web', 'tablet'
    platform VARCHAR(50), -- 'ios', 'android', 'web'
    app_version VARCHAR(20),
    is_active BOOLEAN DEFAULT TRUE,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, device_id)
);

-- Password reset tokens table
CREATE TABLE core_mstr_one_qlick_password_reset_tokens_tbl (
    reset_token_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    token_hash VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    is_used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- ====================================================================

-- User table indexes
CREATE INDEX idx_one_qlick_users_email ON core_mstr_one_qlick_users_tbl(email);
CREATE INDEX idx_one_qlick_users_phone ON core_mstr_one_qlick_users_tbl(phone);
CREATE INDEX idx_one_qlick_users_role ON core_mstr_one_qlick_users_tbl(role);
CREATE INDEX idx_one_qlick_users_status ON core_mstr_one_qlick_users_tbl(status);

-- Address table indexes
CREATE INDEX idx_one_qlick_addresses_user_id ON core_mstr_one_qlick_addresses_tbl(user_id);
CREATE INDEX idx_one_qlick_addresses_location ON core_mstr_one_qlick_addresses_tbl(latitude, longitude);

-- Restaurant table indexes
CREATE INDEX idx_one_qlick_restaurants_owner_id ON core_mstr_one_qlick_restaurants_tbl(owner_id);
CREATE INDEX idx_one_qlick_restaurants_location ON core_mstr_one_qlick_restaurants_tbl(latitude, longitude);
CREATE INDEX idx_one_qlick_restaurants_status ON core_mstr_one_qlick_restaurants_tbl(status);
CREATE INDEX idx_one_qlick_restaurants_cuisine ON core_mstr_one_qlick_restaurants_tbl(cuisine_type);

-- Food items table indexes
CREATE INDEX idx_one_qlick_food_items_restaurant ON core_mstr_one_qlick_food_items_tbl(restaurant_id);
CREATE INDEX idx_one_qlick_food_items_category ON core_mstr_one_qlick_food_items_tbl(category_id);
CREATE INDEX idx_one_qlick_food_items_status ON core_mstr_one_qlick_food_items_tbl(status);

-- Order table indexes
CREATE INDEX idx_one_qlick_orders_customer ON core_mstr_one_qlick_orders_tbl(customer_id);
CREATE INDEX idx_one_qlick_orders_restaurant ON core_mstr_one_qlick_orders_tbl(restaurant_id);
CREATE INDEX idx_one_qlick_orders_delivery_partner ON core_mstr_one_qlick_orders_tbl(delivery_partner_id);
CREATE INDEX idx_one_qlick_orders_status ON core_mstr_one_qlick_orders_tbl(order_status);
CREATE INDEX idx_one_qlick_orders_payment_status ON core_mstr_one_qlick_orders_tbl(payment_status);
CREATE INDEX idx_one_qlick_orders_created_at ON core_mstr_one_qlick_orders_tbl(created_at);
CREATE INDEX idx_one_qlick_orders_order_number ON core_mstr_one_qlick_orders_tbl(order_number);

-- Order items table indexes
CREATE INDEX idx_one_qlick_order_items_order_id ON core_mstr_one_qlick_order_items_tbl(order_id);
CREATE INDEX idx_one_qlick_order_items_food_item_id ON core_mstr_one_qlick_order_items_tbl(food_item_id);

-- Delivery partners table indexes
CREATE INDEX idx_one_qlick_delivery_partners_user_id ON core_mstr_one_qlick_delivery_partners_tbl(user_id);
CREATE INDEX idx_one_qlick_delivery_partners_availability ON core_mstr_one_qlick_delivery_partners_tbl(availability_status);
CREATE INDEX idx_one_qlick_delivery_partners_location ON core_mstr_one_qlick_delivery_partners_tbl(current_latitude, current_longitude);

-- Order tracking table indexes
CREATE INDEX idx_one_qlick_order_tracking_order ON core_mstr_one_qlick_order_tracking_tbl(order_id);
CREATE INDEX idx_one_qlick_order_tracking_status ON core_mstr_one_qlick_order_tracking_tbl(status);

-- Coupon table indexes
CREATE INDEX idx_one_qlick_coupons_code ON core_mstr_one_qlick_coupons_tbl(code);
CREATE INDEX idx_one_qlick_coupons_active ON core_mstr_one_qlick_coupons_tbl(is_active);
CREATE INDEX idx_one_qlick_coupons_validity ON core_mstr_one_qlick_coupons_tbl(valid_from, valid_until);

-- User coupon usage table indexes
CREATE INDEX idx_one_qlick_user_coupon_usage_user_id ON core_mstr_one_qlick_user_coupon_usage_tbl(user_id);
CREATE INDEX idx_one_qlick_user_coupon_usage_coupon_id ON core_mstr_one_qlick_user_coupon_usage_tbl(coupon_id);

-- Reviews table indexes
CREATE INDEX idx_one_qlick_reviews_order_id ON core_mstr_one_qlick_reviews_tbl(order_id);
CREATE INDEX idx_one_qlick_reviews_customer_id ON core_mstr_one_qlick_reviews_tbl(customer_id);
CREATE INDEX idx_one_qlick_reviews_restaurant_id ON core_mstr_one_qlick_reviews_tbl(restaurant_id);
CREATE INDEX idx_one_qlick_reviews_delivery_partner_id ON core_mstr_one_qlick_reviews_tbl(delivery_partner_id);

-- Notifications table indexes
CREATE INDEX idx_one_qlick_notifications_user_id ON core_mstr_one_qlick_notifications_tbl(user_id);
CREATE INDEX idx_one_qlick_notifications_read_status ON core_mstr_one_qlick_notifications_tbl(is_read);
CREATE INDEX idx_one_qlick_notifications_type ON core_mstr_one_qlick_notifications_tbl(notification_type);

-- Authentication tables indexes
CREATE INDEX idx_one_qlick_refresh_tokens_user_id ON core_mstr_one_qlick_refresh_tokens_tbl(user_id);
CREATE INDEX idx_one_qlick_refresh_tokens_token_hash ON core_mstr_one_qlick_refresh_tokens_tbl(token_hash);
CREATE INDEX idx_one_qlick_refresh_tokens_expires_at ON core_mstr_one_qlick_refresh_tokens_tbl(expires_at);

CREATE INDEX idx_one_qlick_oauth_providers_user_id ON core_mstr_one_qlick_oauth_providers_tbl(user_id);
CREATE INDEX idx_one_qlick_oauth_providers_provider ON core_mstr_one_qlick_oauth_providers_tbl(provider);
CREATE INDEX idx_one_qlick_oauth_providers_provider_user_id ON core_mstr_one_qlick_oauth_providers_tbl(provider, provider_user_id);

CREATE INDEX idx_one_qlick_otp_verifications_user_id ON core_mstr_one_qlick_otp_verifications_tbl(user_id);
CREATE INDEX idx_one_qlick_otp_verifications_phone ON core_mstr_one_qlick_otp_verifications_tbl(phone);
CREATE INDEX idx_one_qlick_otp_verifications_email ON core_mstr_one_qlick_otp_verifications_tbl(email);
CREATE INDEX idx_one_qlick_otp_verifications_expires_at ON core_mstr_one_qlick_otp_verifications_tbl(expires_at);

CREATE INDEX idx_one_qlick_user_sessions_user_id ON core_mstr_one_qlick_user_sessions_tbl(user_id);
CREATE INDEX idx_one_qlick_user_sessions_device_id ON core_mstr_one_qlick_user_sessions_tbl(device_id);
CREATE INDEX idx_one_qlick_user_sessions_active ON core_mstr_one_qlick_user_sessions_tbl(is_active);

CREATE INDEX idx_one_qlick_password_reset_tokens_user_id ON core_mstr_one_qlick_password_reset_tokens_tbl(user_id);
CREATE INDEX idx_one_qlick_password_reset_tokens_token_hash ON core_mstr_one_qlick_password_reset_tokens_tbl(token_hash);
CREATE INDEX idx_one_qlick_password_reset_tokens_expires_at ON core_mstr_one_qlick_password_reset_tokens_tbl(expires_at);

-- ====================================================================
-- TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- ====================================================================

-- Function to update the updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply the trigger to tables with updated_at column
CREATE TRIGGER update_one_qlick_users_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_users_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_restaurants_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_restaurants_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_food_items_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_food_items_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_orders_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_orders_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_delivery_partners_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_delivery_partners_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Authentication tables triggers
CREATE TRIGGER update_one_qlick_refresh_tokens_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_refresh_tokens_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_oauth_providers_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_oauth_providers_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_sessions_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_sessions_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ====================================================================
-- SAMPLE DATA INSERTION (OPTIONAL)
-- ====================================================================

-- Insert sample categories
INSERT INTO core_mstr_one_qlick_categories_tbl (name, description, is_active, sort_order) VALUES
('Appetizers', 'Starters and appetizers', TRUE, 1),
('Main Course', 'Main dishes and entrees', TRUE, 2),
('Desserts', 'Sweet treats and desserts', TRUE, 3),
('Beverages', 'Drinks and beverages', TRUE, 4),
('Fast Food', 'Quick and fast food items', TRUE, 5);

-- ====================================================================
-- ADDITIONAL TABLES FOR ENHANCED FUNCTIONALITY
-- ====================================================================

-- Food item add-ons table
CREATE TABLE core_mstr_one_qlick_food_addons_tbl (
    addon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_item_id UUID REFERENCES core_mstr_one_qlick_food_items_tbl(food_item_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    is_available BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Food item customization options table
CREATE TABLE core_mstr_one_qlick_food_customizations_tbl (
    customization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    food_item_id UUID REFERENCES core_mstr_one_qlick_food_items_tbl(food_item_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- e.g., "Spice Level", "Size"
    is_required BOOLEAN DEFAULT FALSE,
    max_selections INTEGER DEFAULT 1,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Customization options values
CREATE TABLE core_mstr_one_qlick_customization_options_tbl (
    option_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    customization_id UUID REFERENCES core_mstr_one_qlick_food_customizations_tbl(customization_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL, -- e.g., "Mild", "Medium", "Spicy"
    price_adjustment DECIMAL(10, 2) DEFAULT 0,
    is_available BOOLEAN DEFAULT TRUE,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Shopping cart table
CREATE TABLE core_mstr_one_qlick_cart_tbl (
    cart_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart items table
CREATE TABLE core_mstr_one_qlick_cart_items_tbl (
    cart_item_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_id UUID REFERENCES core_mstr_one_qlick_cart_tbl(cart_id) ON DELETE CASCADE,
    food_item_id UUID REFERENCES core_mstr_one_qlick_food_items_tbl(food_item_id),
    quantity INTEGER NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart item customizations
CREATE TABLE core_mstr_one_qlick_cart_item_customizations_tbl (
    cart_item_customization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_item_id UUID REFERENCES core_mstr_one_qlick_cart_items_tbl(cart_item_id) ON DELETE CASCADE,
    customization_id UUID REFERENCES core_mstr_one_qlick_food_customizations_tbl(customization_id),
    option_id UUID REFERENCES core_mstr_one_qlick_customization_options_tbl(option_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cart item add-ons
CREATE TABLE core_mstr_one_qlick_cart_item_addons_tbl (
    cart_item_addon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cart_item_id UUID REFERENCES core_mstr_one_qlick_cart_items_tbl(cart_item_id) ON DELETE CASCADE,
    addon_id UUID REFERENCES core_mstr_one_qlick_food_addons_tbl(addon_id),
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order item customizations (to store selected customizations)
CREATE TABLE core_mstr_one_qlick_order_item_customizations_tbl (
    order_item_customization_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_item_id UUID REFERENCES core_mstr_one_qlick_order_items_tbl(order_item_id) ON DELETE CASCADE,
    customization_id UUID REFERENCES core_mstr_one_qlick_food_customizations_tbl(customization_id),
    option_id UUID REFERENCES core_mstr_one_qlick_customization_options_tbl(option_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order item add-ons
CREATE TABLE core_mstr_one_qlick_order_item_addons_tbl (
    order_item_addon_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_item_id UUID REFERENCES core_mstr_one_qlick_order_items_tbl(order_item_id) ON DELETE CASCADE,
    addon_id UUID REFERENCES core_mstr_one_qlick_food_addons_tbl(addon_id),
    quantity INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User preferences table
CREATE TABLE core_mstr_one_qlick_user_preferences_tbl (
    preference_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    notifications_enabled BOOLEAN DEFAULT TRUE,
    location_services_enabled BOOLEAN DEFAULT TRUE,
    language VARCHAR(10) DEFAULT 'en',
    currency VARCHAR(3) DEFAULT 'INR',
    dark_mode BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User favorite restaurants
CREATE TABLE core_mstr_one_qlick_user_favorites_tbl (
    favorite_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, restaurant_id)
);

-- User payment methods table
CREATE TABLE core_mstr_one_qlick_user_payment_methods_tbl (
    payment_method_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    payment_type payment_method NOT NULL,
    name VARCHAR(100) NOT NULL, -- e.g., "HDFC Credit Card", "Google Pay"
    last_four_digits VARCHAR(4),
    upi_id VARCHAR(100),
    bank_name VARCHAR(100),
    is_default BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User wallet table
CREATE TABLE core_mstr_one_qlick_user_wallets_tbl (
    wallet_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    balance DECIMAL(10, 2) DEFAULT 0,
    currency VARCHAR(3) DEFAULT 'INR',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Wallet transactions
CREATE TABLE core_mstr_one_qlick_wallet_transactions_tbl (
    transaction_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    wallet_id UUID REFERENCES core_mstr_one_qlick_user_wallets_tbl(wallet_id) ON DELETE CASCADE,
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id),
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(20) NOT NULL, -- 'credit', 'debit', 'refund'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Order status history table (more detailed than current tracking)
CREATE TABLE core_mstr_one_qlick_order_status_history_tbl (
    status_history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id) ON DELETE CASCADE,
    status order_status NOT NULL,
    status_message TEXT,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    updated_by UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Driver location tracking
CREATE TABLE core_mstr_one_qlick_driver_locations_tbl (
    location_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    delivery_partner_id UUID REFERENCES core_mstr_one_qlick_delivery_partners_tbl(delivery_partner_id) ON DELETE CASCADE,
    order_id UUID REFERENCES core_mstr_one_qlick_orders_tbl(order_id),
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurant features table
CREATE TABLE core_mstr_one_qlick_restaurant_features_tbl (
    feature_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL, -- e.g., "Free Delivery", "Fast Delivery"
    feature_value VARCHAR(255),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Restaurant offers table
CREATE TABLE core_mstr_one_qlick_restaurant_offers_tbl (
    offer_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    restaurant_id UUID REFERENCES core_mstr_one_qlick_restaurants_tbl(restaurant_id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    discount_type VARCHAR(20) NOT NULL, -- 'percentage', 'fixed', 'free_delivery'
    discount_value DECIMAL(10, 2) NOT NULL,
    min_order_amount DECIMAL(10, 2) DEFAULT 0,
    max_discount_amount DECIMAL(10, 2),
    valid_from TIMESTAMP NOT NULL,
    valid_until TIMESTAMP NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search history table
CREATE TABLE core_mstr_one_qlick_search_history_tbl (
    search_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    search_query VARCHAR(255) NOT NULL,
    search_type VARCHAR(20) NOT NULL, -- 'restaurant', 'food', 'general'
    results_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User analytics table
CREATE TABLE core_mstr_one_qlick_user_analytics_tbl (
    analytics_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES core_mstr_one_qlick_users_tbl(user_id) ON DELETE CASCADE,
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0,
    loyalty_points INTEGER DEFAULT 0,
    favorite_cuisine VARCHAR(100),
    last_order_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ====================================================================
-- SCHEMA ENHANCEMENTS
-- ====================================================================

-- Add missing columns to users table
ALTER TABLE core_mstr_one_qlick_users_tbl 
ADD COLUMN date_of_birth DATE,
ADD COLUMN gender VARCHAR(10) CHECK (gender IN ('male', 'female', 'other')),
ADD COLUMN loyalty_points INTEGER DEFAULT 0;

-- Add missing columns to addresses table
ALTER TABLE core_mstr_one_qlick_addresses_tbl 
ADD COLUMN address_type VARCHAR(20) DEFAULT 'home' CHECK (address_type IN ('home', 'work', 'restaurant', 'other')),
ADD COLUMN landmark VARCHAR(255);

-- Add missing columns to food items table
ALTER TABLE core_mstr_one_qlick_food_items_tbl 
ADD COLUMN is_popular BOOLEAN DEFAULT FALSE,
ADD COLUMN is_recommended BOOLEAN DEFAULT FALSE,
ADD COLUMN nutrition_info JSONB,
ADD COLUMN preparation_time VARCHAR(20);

-- Add missing columns to restaurants table
ALTER TABLE core_mstr_one_qlick_restaurants_tbl 
ADD COLUMN is_veg BOOLEAN DEFAULT FALSE,
ADD COLUMN is_pure_veg BOOLEAN DEFAULT FALSE,
ADD COLUMN cost_for_two DECIMAL(10, 2),
ADD COLUMN platform_fee DECIMAL(10, 2) DEFAULT 5;

-- Add new order status to enum
ALTER TYPE order_status ADD VALUE 'out_for_delivery';

-- Add new payment methods to enum
ALTER TYPE payment_method ADD VALUE 'netbanking';
ALTER TYPE payment_method ADD VALUE 'cod';

-- ====================================================================
-- ADDITIONAL INDEXES FOR PERFORMANCE OPTIMIZATION
-- ====================================================================

-- Food add-ons and customizations indexes
CREATE INDEX idx_one_qlick_food_addons_food_item ON core_mstr_one_qlick_food_addons_tbl(food_item_id);
CREATE INDEX idx_one_qlick_customizations_food_item ON core_mstr_one_qlick_food_customizations_tbl(food_item_id);
CREATE INDEX idx_one_qlick_customization_options_customization ON core_mstr_one_qlick_customization_options_tbl(customization_id);

-- Cart related indexes
CREATE INDEX idx_one_qlick_cart_user ON core_mstr_one_qlick_cart_tbl(user_id);
CREATE INDEX idx_one_qlick_cart_items_cart ON core_mstr_one_qlick_cart_items_tbl(cart_id);
CREATE INDEX idx_one_qlick_cart_item_customizations_cart_item ON core_mstr_one_qlick_cart_item_customizations_tbl(cart_item_id);
CREATE INDEX idx_one_qlick_cart_item_addons_cart_item ON core_mstr_one_qlick_cart_item_addons_tbl(cart_item_id);

-- Order item customizations and add-ons indexes
CREATE INDEX idx_one_qlick_order_item_customizations_order_item ON core_mstr_one_qlick_order_item_customizations_tbl(order_item_id);
CREATE INDEX idx_one_qlick_order_item_addons_order_item ON core_mstr_one_qlick_order_item_addons_tbl(order_item_id);

-- User preferences and favorites indexes
CREATE INDEX idx_one_qlick_user_preferences_user ON core_mstr_one_qlick_user_preferences_tbl(user_id);
CREATE INDEX idx_one_qlick_user_favorites_user ON core_mstr_one_qlick_user_favorites_tbl(user_id);
CREATE INDEX idx_one_qlick_user_favorites_restaurant ON core_mstr_one_qlick_user_favorites_tbl(restaurant_id);

-- Payment methods and wallet indexes
CREATE INDEX idx_one_qlick_user_payment_methods_user ON core_mstr_one_qlick_user_payment_methods_tbl(user_id);
CREATE INDEX idx_one_qlick_user_wallets_user ON core_mstr_one_qlick_user_wallets_tbl(user_id);
CREATE INDEX idx_one_qlick_wallet_transactions_wallet ON core_mstr_one_qlick_wallet_transactions_tbl(wallet_id);
CREATE INDEX idx_one_qlick_wallet_transactions_order ON core_mstr_one_qlick_wallet_transactions_tbl(order_id);

-- Order tracking and driver location indexes
CREATE INDEX idx_one_qlick_order_status_history_order ON core_mstr_one_qlick_order_status_history_tbl(order_id);
CREATE INDEX idx_one_qlick_driver_locations_partner ON core_mstr_one_qlick_driver_locations_tbl(delivery_partner_id);
CREATE INDEX idx_one_qlick_driver_locations_order ON core_mstr_one_qlick_driver_locations_tbl(order_id);

-- Restaurant features and offers indexes
CREATE INDEX idx_one_qlick_restaurant_features_restaurant ON core_mstr_one_qlick_restaurant_features_tbl(restaurant_id);
CREATE INDEX idx_one_qlick_restaurant_offers_restaurant ON core_mstr_one_qlick_restaurant_offers_tbl(restaurant_id);
CREATE INDEX idx_one_qlick_restaurant_offers_active ON core_mstr_one_qlick_restaurant_offers_tbl(is_active);

-- Search and analytics indexes
CREATE INDEX idx_one_qlick_search_history_user ON core_mstr_one_qlick_search_history_tbl(user_id);
CREATE INDEX idx_one_qlick_user_analytics_user ON core_mstr_one_qlick_user_analytics_tbl(user_id);

-- Composite indexes for common query patterns
CREATE INDEX idx_one_qlick_orders_customer_status ON core_mstr_one_qlick_orders_tbl(customer_id, order_status);
CREATE INDEX idx_one_qlick_orders_restaurant_status ON core_mstr_one_qlick_orders_tbl(restaurant_id, order_status);
CREATE INDEX idx_one_qlick_food_items_restaurant_status ON core_mstr_one_qlick_food_items_tbl(restaurant_id, status);
CREATE INDEX idx_one_qlick_restaurants_location_status ON core_mstr_one_qlick_restaurants_tbl(latitude, longitude, status);

-- Partial indexes for active records
CREATE INDEX idx_one_qlick_restaurants_active ON core_mstr_one_qlick_restaurants_tbl(restaurant_id) WHERE status = 'active';
CREATE INDEX idx_one_qlick_food_items_available ON core_mstr_one_qlick_food_items_tbl(food_item_id) WHERE status = 'available';
CREATE INDEX idx_one_qlick_orders_active ON core_mstr_one_qlick_orders_tbl(order_id) WHERE order_status IN ('pending', 'confirmed', 'preparing', 'ready_for_pickup', 'out_for_delivery');

-- ====================================================================
-- ADDITIONAL TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- ====================================================================

-- Add triggers for new tables with updated_at columns
CREATE TRIGGER update_one_qlick_cart_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_cart_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_cart_items_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_cart_items_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_preferences_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_preferences_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_payment_methods_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_payment_methods_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_wallets_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_wallets_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_one_qlick_user_analytics_updated_at
    BEFORE UPDATE ON core_mstr_one_qlick_user_analytics_tbl
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ====================================================================
-- DATA VALIDATION CONSTRAINTS
-- ====================================================================

-- Add validation constraints
ALTER TABLE core_mstr_one_qlick_food_items_tbl 
ADD CONSTRAINT chk_food_price_positive CHECK (price >= 0);

ALTER TABLE core_mstr_one_qlick_orders_tbl 
ADD CONSTRAINT chk_order_amount_positive CHECK (total_amount >= 0);

ALTER TABLE core_mstr_one_qlick_user_wallets_tbl 
ADD CONSTRAINT chk_wallet_balance_non_negative CHECK (balance >= 0);

ALTER TABLE core_mstr_one_qlick_cart_items_tbl 
ADD CONSTRAINT chk_cart_quantity_positive CHECK (quantity > 0);

ALTER TABLE core_mstr_one_qlick_food_addons_tbl 
ADD CONSTRAINT chk_addon_price_non_negative CHECK (price >= 0);

-- ====================================================================
-- CLEANUP FUNCTIONS FOR EXPIRED TOKENS
-- ====================================================================

-- Function to clean up expired refresh tokens
CREATE OR REPLACE FUNCTION cleanup_expired_refresh_tokens()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_refresh_tokens_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Function to clean up expired OTP codes
CREATE OR REPLACE FUNCTION cleanup_expired_otp_codes()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_otp_verifications_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- Function to clean up expired password reset tokens
CREATE OR REPLACE FUNCTION cleanup_expired_password_reset_tokens()
RETURNS void AS $$
BEGIN
    DELETE FROM core_mstr_one_qlick_password_reset_tokens_tbl 
    WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================

-- Script execution completed successfully
SELECT 'oneQlick enhanced database setup with authentication completed successfully!' as status;