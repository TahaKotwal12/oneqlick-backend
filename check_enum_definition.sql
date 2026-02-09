-- Check the actual enum values in the database
SELECT enumlabel 
FROM pg_enum 
WHERE enumtypid = 'coupontype'::regtype
ORDER BY enumsortorder;

-- Check the data type of the coupon_type column
SELECT 
    column_name,
    data_type,
    udt_name
FROM information_schema.columns
WHERE table_name = 'core_mstr_one_qlick_coupons_tbl' 
AND column_name = 'coupon_type';

-- Check existing coupon data
SELECT code, coupon_type::TEXT as coupon_type_value
FROM core_mstr_one_qlick_coupons_tbl
LIMIT 5;
