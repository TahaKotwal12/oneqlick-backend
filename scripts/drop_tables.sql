-- ====================================================================
-- DROP TABLES SCRIPT FOR ONEQLICK DATABASE
-- ====================================================================
-- This script drops all tables in the correct order to avoid foreign key constraint errors
-- Run this script to completely clean the database

-- ====================================================================
-- DROP TRIGGERS FIRST
-- ====================================================================

-- Drop all triggers
DROP TRIGGER IF EXISTS update_one_qlick_users_updated_at ON core_mstr_one_qlick_users_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_restaurants_updated_at ON core_mstr_one_qlick_restaurants_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_food_items_updated_at ON core_mstr_one_qlick_food_items_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_orders_updated_at ON core_mstr_one_qlick_orders_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_delivery_partners_updated_at ON core_mstr_one_qlick_delivery_partners_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_refresh_tokens_updated_at ON core_mstr_one_qlick_refresh_tokens_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_oauth_providers_updated_at ON core_mstr_one_qlick_oauth_providers_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_user_sessions_updated_at ON core_mstr_one_qlick_user_sessions_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_cart_updated_at ON core_mstr_one_qlick_cart_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_cart_items_updated_at ON core_mstr_one_qlick_cart_items_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_user_preferences_updated_at ON core_mstr_one_qlick_user_preferences_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_user_payment_methods_updated_at ON core_mstr_one_qlick_user_payment_methods_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_user_wallets_updated_at ON core_mstr_one_qlick_user_wallets_tbl;
DROP TRIGGER IF EXISTS update_one_qlick_user_analytics_updated_at ON core_mstr_one_qlick_user_analytics_tbl;

-- ====================================================================
-- DROP FUNCTIONS
-- ====================================================================

-- Drop custom functions
DROP FUNCTION IF EXISTS update_updated_at_column();
DROP FUNCTION IF EXISTS cleanup_expired_refresh_tokens();
DROP FUNCTION IF EXISTS cleanup_expired_otp_codes();
DROP FUNCTION IF EXISTS cleanup_expired_password_reset_tokens();

-- ====================================================================
-- DROP TABLES IN REVERSE ORDER (CHILDREN FIRST, PARENTS LAST)
-- ====================================================================

-- Drop all tables that have foreign key references first

-- Order item related tables
DROP TABLE IF EXISTS core_mstr_one_qlick_order_item_addons_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_order_item_customizations_tbl CASCADE;

-- Cart item related tables
DROP TABLE IF EXISTS core_mstr_one_qlick_cart_item_addons_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_cart_item_customizations_tbl CASCADE;

-- Order items and tracking
DROP TABLE IF EXISTS core_mstr_one_qlick_order_items_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_order_tracking_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_order_status_history_tbl CASCADE;

-- Cart tables
DROP TABLE IF EXISTS core_mstr_one_qlick_cart_items_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_cart_tbl CASCADE;

-- User related tables
DROP TABLE IF EXISTS core_mstr_one_qlick_user_coupon_usage_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_favorites_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_preferences_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_payment_methods_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_wallet_transactions_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_wallets_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_analytics_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_search_history_tbl CASCADE;

-- Authentication tables
DROP TABLE IF EXISTS core_mstr_one_qlick_refresh_tokens_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_oauth_providers_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_otp_verifications_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_user_sessions_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_password_reset_tokens_tbl CASCADE;

-- Reviews and notifications
DROP TABLE IF EXISTS core_mstr_one_qlick_reviews_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_notifications_tbl CASCADE;

-- Coupons
DROP TABLE IF EXISTS core_mstr_one_qlick_coupons_tbl CASCADE;

-- Orders
DROP TABLE IF EXISTS core_mstr_one_qlick_orders_tbl CASCADE;

-- Delivery partners and locations
DROP TABLE IF EXISTS core_mstr_one_qlick_driver_locations_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_delivery_partners_tbl CASCADE;

-- Food related tables
DROP TABLE IF EXISTS core_mstr_one_qlick_customization_options_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_food_customizations_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_food_addons_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_food_variants_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_food_items_tbl CASCADE;

-- Restaurant related tables
DROP TABLE IF EXISTS core_mstr_one_qlick_restaurant_offers_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_restaurant_features_tbl CASCADE;
DROP TABLE IF EXISTS core_mstr_one_qlick_restaurants_tbl CASCADE;

-- Categories
DROP TABLE IF EXISTS core_mstr_one_qlick_categories_tbl CASCADE;

-- Addresses
DROP TABLE IF EXISTS core_mstr_one_qlick_addresses_tbl CASCADE;

-- Users (main table - dropped last)
DROP TABLE IF EXISTS core_mstr_one_qlick_users_tbl CASCADE;

-- ====================================================================
-- DROP ENUMS
-- ====================================================================

-- Drop all custom enum types
DROP TYPE IF EXISTS user_role CASCADE;
DROP TYPE IF EXISTS user_status CASCADE;
DROP TYPE IF EXISTS restaurant_status CASCADE;
DROP TYPE IF EXISTS food_status CASCADE;
DROP TYPE IF EXISTS order_status CASCADE;
DROP TYPE IF EXISTS payment_status CASCADE;
DROP TYPE IF EXISTS payment_method CASCADE;
DROP TYPE IF EXISTS vehicle_type CASCADE;
DROP TYPE IF EXISTS availability_status CASCADE;
DROP TYPE IF EXISTS coupon_type CASCADE;
DROP TYPE IF EXISTS notification_type CASCADE;
DROP TYPE IF EXISTS address_type CASCADE;
DROP TYPE IF EXISTS gender CASCADE;
DROP TYPE IF EXISTS transaction_type CASCADE;
DROP TYPE IF EXISTS search_type CASCADE;
DROP TYPE IF EXISTS review_type CASCADE;

-- ====================================================================
-- DROP INDEXES (if any remain)
-- ====================================================================

-- Note: Indexes are automatically dropped when tables are dropped
-- This section is for any standalone indexes that might exist

-- ====================================================================
-- VERIFICATION
-- ====================================================================

-- Check if any tables remain
SELECT 
    schemaname,
    tablename 
FROM pg_tables 
WHERE tablename LIKE 'core_mstr_one_qlick_%'
ORDER BY tablename;

-- ====================================================================
-- COMPLETION MESSAGE
-- ====================================================================

SELECT 'All OneQlick tables, enums, triggers, and functions dropped successfully!' as status;
