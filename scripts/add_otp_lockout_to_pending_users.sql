-- Add OTP lockout system columns to pending users table
-- This migration adds the necessary columns for implementing OTP rate limiting with lockout

ALTER TABLE core_mstr_one_qlick_pending_users_tbl 
ADD COLUMN IF NOT EXISTS otp_attempts INTEGER DEFAULT 0,
ADD COLUMN IF NOT EXISTS max_otp_attempts INTEGER DEFAULT 3,
ADD COLUMN IF NOT EXISTS otp_locked_until TIMESTAMP WITH TIME ZONE,
ADD COLUMN IF NOT EXISTS lockout_duration_minutes INTEGER DEFAULT 10;

-- Add comments for documentation
COMMENT ON COLUMN core_mstr_one_qlick_pending_users_tbl.otp_attempts IS 'Number of OTP attempts made by this user';
COMMENT ON COLUMN core_mstr_one_qlick_pending_users_tbl.max_otp_attempts IS 'Maximum OTP attempts allowed before lockout';
COMMENT ON COLUMN core_mstr_one_qlick_pending_users_tbl.otp_locked_until IS 'Timestamp when the OTP lockout expires';
COMMENT ON COLUMN core_mstr_one_qlick_pending_users_tbl.lockout_duration_minutes IS 'Duration of lockout in minutes';

-- Create index for efficient lockout queries
CREATE INDEX IF NOT EXISTS idx_pending_users_otp_lockout 
ON core_mstr_one_qlick_pending_users_tbl (otp_locked_until) 
WHERE otp_locked_until IS NOT NULL;

