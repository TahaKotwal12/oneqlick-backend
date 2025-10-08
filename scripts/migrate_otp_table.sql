-- Migration script to update OTP verification table for pending users support
-- Run this script to add pending_user_id column to existing OTP verification table

-- Add pending_user_id column to OTP verification table
ALTER TABLE core_mstr_one_qlick_otp_verifications_tbl 
ADD COLUMN pending_user_id UUID REFERENCES core_mstr_one_qlick_pending_users_tbl(pending_user_id) ON DELETE CASCADE;

-- Make user_id nullable (it was already nullable in the model, but let's ensure it)
ALTER TABLE core_mstr_one_qlick_otp_verifications_tbl 
ALTER COLUMN user_id DROP NOT NULL;

-- Convert TIMESTAMP columns to TIMESTAMPTZ for timezone support
-- This fixes the "can't compare offset-naive and offset-aware datetimes" error

-- Update OTP verification table
ALTER TABLE core_mstr_one_qlick_otp_verifications_tbl 
ALTER COLUMN expires_at TYPE TIMESTAMPTZ USING expires_at AT TIME ZONE 'UTC';

ALTER TABLE core_mstr_one_qlick_otp_verifications_tbl 
ALTER COLUMN created_at TYPE TIMESTAMPTZ USING created_at AT TIME ZONE 'UTC';

-- Update pending users table
ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ALTER COLUMN expires_at TYPE TIMESTAMPTZ USING expires_at AT TIME ZONE 'UTC';

ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ALTER COLUMN created_at TYPE TIMESTAMPTZ USING created_at AT TIME ZONE 'UTC';

ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ALTER COLUMN updated_at TYPE TIMESTAMPTZ USING updated_at AT TIME ZONE 'UTC';

-- Add index for pending_user_id
CREATE INDEX idx_one_qlick_otp_verifications_pending_user_id ON core_mstr_one_qlick_otp_verifications_tbl(pending_user_id);

-- Add constraint to ensure either user_id or pending_user_id is set (but not both)
ALTER TABLE core_mstr_one_qlick_otp_verifications_tbl 
ADD CONSTRAINT check_user_reference CHECK (
    (user_id IS NOT NULL AND pending_user_id IS NULL) OR 
    (user_id IS NULL AND pending_user_id IS NOT NULL)
);

-- Verify the changes
SELECT column_name, data_type, is_nullable 
FROM information_schema.columns 
WHERE table_name = 'core_mstr_one_qlick_otp_verifications_tbl' 
ORDER BY ordinal_position;
