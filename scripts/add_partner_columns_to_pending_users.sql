-- Add partner-specific columns to pending_users table
-- Run this on Railway PostgreSQL database

ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ADD COLUMN IF NOT EXISTS restaurant_name VARCHAR(255),
ADD COLUMN IF NOT EXISTS cuisine_type VARCHAR(100),
ADD COLUMN IF NOT EXISTS vehicle_type VARCHAR(50),
ADD COLUMN IF NOT EXISTS license_number VARCHAR(50);

-- Verify the columns were added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'core_mstr_one_qlick_pending_users_tbl' 
AND column_name IN ('restaurant_name', 'cuisine_type', 'vehicle_type', 'license_number')
ORDER BY column_name;
