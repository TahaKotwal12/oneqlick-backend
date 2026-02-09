-- Migration: Add variant_id, unit_price, and total_price to cart_items table
-- Date: 2026-01-07
-- Description: Adds missing columns to support cart item variants and pricing

-- Add variant_id column (nullable, references food_variants table)
ALTER TABLE core_mstr_one_qlick_cart_items_tbl 
ADD COLUMN IF NOT EXISTS variant_id UUID NULL;

-- Add foreign key constraint for variant_id
ALTER TABLE core_mstr_one_qlick_cart_items_tbl
ADD CONSTRAINT fk_cart_items_variant 
FOREIGN KEY (variant_id) 
REFERENCES core_mstr_one_qlick_food_variants_tbl(food_variant_id)
ON DELETE SET NULL;

-- Add unit_price column (not null, default 0.00)
ALTER TABLE core_mstr_one_qlick_cart_items_tbl 
ADD COLUMN IF NOT EXISTS unit_price NUMERIC(10, 2) NOT NULL DEFAULT 0.00;

-- Add total_price column (not null, default 0.00)
ALTER TABLE core_mstr_one_qlick_cart_items_tbl 
ADD COLUMN IF NOT EXISTS total_price NUMERIC(10, 2) NOT NULL DEFAULT 0.00;

-- Create index on variant_id for better query performance
CREATE INDEX IF NOT EXISTS idx_cart_items_variant_id 
ON core_mstr_one_qlick_cart_items_tbl(variant_id);

-- Verify the changes
SELECT column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_name = 'core_mstr_one_qlick_cart_items_tbl'
ORDER BY ordinal_position;
