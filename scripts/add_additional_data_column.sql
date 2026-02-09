-- Add additional_data column to pending_users table
-- Run this on Railway PostgreSQL database

ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ADD COLUMN IF NOT EXISTS additional_data TEXT;

-- Verify the column was added
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'core_mstr_one_qlick_pending_users_tbl' 
AND column_name = 'additional_data';
