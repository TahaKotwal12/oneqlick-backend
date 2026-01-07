-- ============================================================================
-- CREATE ADMIN USER FOR ONEQLICK ADMIN PORTAL
-- ============================================================================
-- Purpose: Create the first admin user for accessing the admin portal
-- Date: 2026-01-06
-- Usage: Run this script in your PostgreSQL database
-- ============================================================================

-- Step 1: Check if admin user already exists
SELECT 
    user_id, 
    email, 
    first_name, 
    last_name, 
    role, 
    status,
    email_verified,
    created_at
FROM core_mstr_one_qlick_users_tbl
WHERE role = 'admin';

-- If no admin exists, proceed with Step 2

-- ============================================================================
-- Step 2: Create Admin User
-- ============================================================================
-- Password: Admin@123
-- Email: admin@oneqlick.com
-- Phone: +919876543210
-- ============================================================================

INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id,
    email,
    phone,
    password_hash,
    first_name,
    last_name,
    role,
    status,
    email_verified,
    phone_verified,
    loyalty_points,
    created_at,
    updated_at
) VALUES (
    gen_random_uuid(),
    'taha@oneqlick.com',
    '+919999999999',  -- Changed to unique phone number
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpXHGvzxu',  -- Password: Admin@123
    'Taha',
    'Kotwal',
    'admin',
    'active',
    true,
    true,
    0,
    NOW(),
    NOW()
);

-- ============================================================================
-- Step 3: Verify Admin User Created
-- ============================================================================

SELECT 
    user_id, 
    email, 
    first_name, 
    last_name, 
    role, 
    status,
    email_verified,
    phone_verified,
    created_at
FROM core_mstr_one_qlick_users_tbl
WHERE email = 'taha@oneqlick.com';

-- ============================================================================
-- OPTIONAL: Create Additional Admin Users
-- ============================================================================

-- Example: Create a second admin user
-- Uncomment and modify as needed

/*
INSERT INTO core_mstr_one_qlick_users_tbl (
    user_id,
    email,
    phone,
    password_hash,
    first_name,
    last_name,
    role,
    status,
    email_verified,
    phone_verified,
    loyalty_points,
    created_at,
    updated_at
) VALUES (
    gen_random_uuid(),
    'admin2@oneqlick.com',
    '+919876543211',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpXHGvzxu',  -- Password: Admin@123
    'Admin',
    'Two',
    'admin',
    'active',
    true,
    true,
    0,
    NOW(),
    NOW()
);
*/

-- ============================================================================
-- OPTIONAL: Promote Existing User to Admin
-- ============================================================================

-- If you want to make an existing user an admin:
-- Uncomment and replace with actual email

/*
UPDATE core_mstr_one_qlick_users_tbl
SET 
    role = 'admin',
    updated_at = NOW()
WHERE email = 'your-existing-user@example.com';
*/

-- ============================================================================
-- Step 4: View All Admin Users
-- ============================================================================

SELECT 
    user_id, 
    email, 
    phone,
    first_name, 
    last_name, 
    role, 
    status,
    email_verified,
    phone_verified,
    created_at,
    updated_at
FROM core_mstr_one_qlick_users_tbl
WHERE role = 'admin'
ORDER BY created_at DESC;

-- ============================================================================
-- CREDENTIALS FOR LOGIN
-- ============================================================================
-- Email: admin@oneqlick.com
-- Password: Admin@123
-- 
-- Use these credentials to login via:
-- POST /api/v1/auth/login
-- 
-- Body:
-- {
--   "email": "admin@oneqlick.com",
--   "password": "Admin@123"
-- }
-- ============================================================================

-- ============================================================================
-- SECURITY NOTES
-- ============================================================================
-- 1. Change the default password immediately after first login
-- 2. Use strong passwords for production
-- 3. Enable 2FA for admin accounts (when implemented)
-- 4. Regularly audit admin user access
-- 5. Never share admin credentials
-- ============================================================================

-- ============================================================================
-- PASSWORD HASH GENERATION (For Custom Passwords)
-- ============================================================================
-- To generate a hash for a different password, use Python:
--
-- from passlib.context import CryptContext
-- pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
-- password_hash = pwd_context.hash("YourPasswordHere")
-- print(password_hash)
--
-- Then replace the password_hash value in the INSERT statement above
-- ============================================================================
