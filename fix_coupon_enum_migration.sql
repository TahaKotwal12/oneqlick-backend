-- Migration: Fix CouponType Enum Case Mismatch
-- This script updates the coupontype enum to use lowercase values to match the Python application

-- Step 1: Create a temporary column with text type
ALTER TABLE core_mstr_one_qlick_coupons_tbl 
ADD COLUMN coupon_type_temp TEXT;

-- Step 2: Copy existing data, converting to lowercase
UPDATE core_mstr_one_qlick_coupons_tbl 
SET coupon_type_temp = LOWER(coupon_type::TEXT);

-- Step 3: Drop the old enum column
ALTER TABLE core_mstr_one_qlick_coupons_tbl 
DROP COLUMN coupon_type;

-- Step 4: Drop the old enum type
DROP TYPE IF EXISTS coupontype;

-- Step 5: Create new enum type with lowercase values
CREATE TYPE coupontype AS ENUM ('percentage', 'fixed_amount', 'free_delivery');

-- Step 6: Rename temp column and set it as the new enum type
ALTER TABLE core_mstr_one_qlick_coupons_tbl 
RENAME COLUMN coupon_type_temp TO coupon_type;

-- Step 7: Convert the text column to the new enum type
ALTER TABLE core_mstr_one_qlick_coupons_tbl 
ALTER COLUMN coupon_type TYPE coupontype USING coupon_type::coupontype;

-- Step 8: Set NOT NULL constraint
ALTER TABLE core_mstr_one_qlick_coupons_tbl 
ALTER COLUMN coupon_type SET NOT NULL;

-- Verify the migration
SELECT 
    code,
    coupon_type,
    title
FROM core_mstr_one_qlick_coupons_tbl
LIMIT 5;

-- Show the enum values
SELECT enumlabel 
FROM pg_enum 
WHERE enumtypid = 'coupontype'::regtype
ORDER BY enumsortorder;
