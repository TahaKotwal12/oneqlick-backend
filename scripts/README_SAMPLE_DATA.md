# Sample Data Scripts - OneQlick Restaurant Management

## Overview
This folder contains SQL scripts to populate the OneQlick database with sample restaurant data for testing and development.

---

## 📋 Scripts Available

### 1. `script.sql`
**Purpose:** Main database schema creation
- Creates all tables, enums, indexes, triggers
- Must be run FIRST before any data insertion
- Only run once during initial setup

### 2. `insert_sample_restaurants.sql`
**Purpose:** Insert restaurant owners and restaurants
- Creates 10 restaurant owner users
- Creates 10 restaurants across different Indian cities
- Adds restaurant offers and features
- **Must run AFTER** `script.sql`

### 3. `insert_sample_food_items.sql`
**Purpose:** Insert food items for all restaurants
- Creates 40+ food items across all restaurants
- Includes appetizers, main courses, desserts, beverages
- Mix of vegetarian and non-vegetarian items
- **Must run AFTER** `insert_sample_restaurants.sql`

---

## 🚀 Quick Start

### Option 1: Run All Scripts Together (Recommended)

```bash
# Using psql command line
psql -U your_username -d your_database_name -f run_all_sample_data.sql
```

### Option 2: Run Scripts Individually

```bash
# Step 1: Create schema (only if not created)
psql -U your_username -d your_database_name -f script.sql

# Step 2: Insert restaurants and owners
psql -U your_username -d your_database_name -f insert_sample_restaurants.sql

# Step 3: Insert food items
psql -U your_username -d your_database_name -f insert_sample_food_items.sql
```

### Option 3: Using Python with psycopg2

```python
import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="oneqlick_db",
    user="your_username",
    password="your_password"
)

# Execute scripts in order
with conn.cursor() as cur:
    # Read and execute each script
    with open('insert_sample_restaurants.sql', 'r') as f:
        cur.execute(f.read())
    
    with open('insert_sample_food_items.sql', 'r') as f:
        cur.execute(f.read())
    
    conn.commit()

print("Sample data inserted successfully!")
conn.close()
```

---

## 📊 Sample Data Overview

### Restaurant Owners (10 Users)
All owners have:
- **Email:** `owner.{restaurantname}@oneqlick.com`
- **Password:** `Restaurant@123` (bcrypt hashed)
- **Role:** `restaurant_owner`
- **Status:** `active`
- **Email & Phone Verified:** `TRUE`

**List of Owners:**
1. Rajesh Sharma - Spice Garden (Mumbai)
2. Giuseppe Rossi - Pizza Palace (Mumbai)
3. Mohammed Khan - Biryani House (Hyderabad)
4. Priya Mehta - Sweet Corner (Delhi)
5. Amit Patel - Chai Point (Bangalore)
6. Gurpreet Singh - Dhaba Express (Pune)
7. Lakshmi Iyer - South Indian Delights (Chennai)
8. Wei Chen - Dragon Wok (Mumbai)
9. Arjun Malhotra - Burger Nation (Delhi)
10. Meera Gupta - Pure Veg Kitchen (Ahmedabad)

### Restaurants (10 Restaurants)

| Restaurant Name | City | Cuisine | Rating | Cost for Two |
|-----------------|------|---------|--------|--------------|
| Spice Garden | Mumbai | North Indian, Mughlai | 4.5 | ₹400 |
| Pizza Palace | Mumbai | Italian, Pizza | 4.3 | ₹500 |
| Biryani House | Hyderabad | Hyderabadi, Biryani | 4.7 | ₹450 |
| Sweet Corner | Delhi | Desserts, Sweets | 4.2 | ₹250 |
| Chai Point | Bangalore | Beverages, Snacks | 4.0 | ₹150 |
| Dhaba Express | Pune | Punjabi, North Indian | 4.4 | ₹350 |
| South Indian Delights | Chennai | South Indian | 4.6 | ₹200 |
| Dragon Wok | Mumbai | Chinese, Asian | 4.3 | ₹500 |
| Burger Nation | Delhi | Fast Food, Burgers | 4.1 | ₹400 |
| Pure Veg Kitchen | Ahmedabad | Gujarati, Rajasthani | 4.5 | ₹350 |

### Food Items (40+ Items)

**Categories Covered:**
- Appetizers (Paneer Tikka, Chicken 65, Samosa, etc.)
- Main Course (Butter Chicken, Dal Makhani, Biryani, etc.)
- Pizza (Margherita, Pepperoni, Veggie Supreme)
- Desserts (Gulab Jamun, Rasgulla, Jalebi)
- Beverages (Masala Chai, Filter Coffee)
- South Indian (Masala Dosa, Idli, Vada)
- Chinese (Hakka Noodles, Manchurian)
- Fast Food (Burgers)
- Thalis (Gujarati, Rajasthani)

---

## 🔑 Login Credentials

### Restaurant Owners
- **Email:** See table above (e.g., `owner.spicegarden@oneqlick.com`)
- **Password:** `Restaurant@123`
- **Role:** `restaurant_owner`

### Note on Password Hash
The password hash used is:
```
$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYKKIgCRM9W
```

This is generated using bcrypt with:
- Algorithm: bcrypt
- Rounds: 12
- Plain text: `Restaurant@123`

---

## 🗺️ Location Coordinates

All restaurants have real coordinates from major Indian cities:

| City | Latitude | Longitude |
|------|----------|-----------|
| Mumbai | 19.0760 | 72.8777 |
| Hyderabad | 17.4435 | 78.5012 |
| Delhi | 28.6508 | 77.2318 |
| Bangalore | 12.9716 | 77.5946 |
| Pune | 18.5204 | 73.8567 |
| Chennai | 13.0418 | 80.2341 |
| Ahmedabad | 23.0341 | 72.5502 |

---

## ✅ Verification Queries

After running the scripts, verify the data:

### Check Restaurant Owners
```sql
SELECT COUNT(*) as total_restaurant_owners 
FROM core_mstr_one_qlick_users_tbl 
WHERE role = 'restaurant_owner';
-- Expected: 10
```

### Check Restaurants
```sql
SELECT COUNT(*) as total_restaurants 
FROM core_mstr_one_qlick_restaurants_tbl;
-- Expected: 10
```

### Check Food Items
```sql
SELECT COUNT(*) as total_food_items 
FROM core_mstr_one_qlick_food_items_tbl;
-- Expected: 40+
```

### View Restaurant Details
```sql
SELECT 
    r.name as restaurant_name,
    r.city,
    r.cuisine_type,
    r.rating,
    u.first_name || ' ' || u.last_name as owner_name
FROM 
    core_mstr_one_qlick_restaurants_tbl r
    INNER JOIN core_mstr_one_qlick_users_tbl u ON r.owner_id = u.user_id
ORDER BY 
    r.city, r.name;
```

### View Menu Items Count
```sql
SELECT 
    r.name as restaurant_name,
    COUNT(f.food_item_id) as total_menu_items
FROM 
    core_mstr_one_qlick_restaurants_tbl r
    LEFT JOIN core_mstr_one_qlick_food_items_tbl f ON r.restaurant_id = f.restaurant_id
GROUP BY 
    r.restaurant_id, r.name
ORDER BY 
    total_menu_items DESC;
```

---

## 🧹 Clean Up (Remove Sample Data)

If you want to remove all sample data:

```sql
-- WARNING: This will delete all data!

-- Delete food items
DELETE FROM core_mstr_one_qlick_food_items_tbl;

-- Delete restaurant offers and features
DELETE FROM core_mstr_one_qlick_restaurant_offers_tbl;
DELETE FROM core_mstr_one_qlick_restaurant_features_tbl;

-- Delete restaurants
DELETE FROM core_mstr_one_qlick_restaurants_tbl;

-- Delete restaurant owners
DELETE FROM core_mstr_one_qlick_users_tbl WHERE role = 'restaurant_owner';
```

---

## 🎯 Testing APIs

After inserting sample data, you can test these APIs:

### 1. Get Nearby Restaurants
```bash
GET /api/restaurants/nearby?latitude=19.0760&longitude=72.8777&radius_km=10
```

### 2. Get Restaurant Details
```bash
GET /api/restaurants/11111111-1111-1111-1111-111111111111
```

### 3. Get Restaurant Menu
```bash
GET /api/restaurants/11111111-1111-1111-1111-111111111111/menu
```

### 4. Get Popular Dishes
```bash
GET /api/food-items/popular?latitude=19.0760&longitude=72.8777&limit=10
```

### 5. Search Restaurants
```bash
GET /api/restaurants/search?query=biryani&latitude=17.4435&longitude=78.5012
```

---

## 📝 Notes

1. **UUIDs are fixed** in these scripts for consistency and easier testing
2. **Images use Unsplash URLs** - replace with your CDN URLs in production
3. **Passwords are identical** for all owners for testing convenience
4. **Ratings and review counts** are sample data
5. **All restaurants are marked as `active` and `open`**

---

## 🐛 Troubleshooting

### Error: "duplicate key value violates unique constraint"
**Solution:** Data already exists. Run cleanup script first or use different UUIDs.

### Error: "violates foreign key constraint"
**Solution:** Run scripts in correct order: schema → restaurants → food items

### Error: "role user_role does not exist"
**Solution:** Run `script.sql` first to create enums and tables

### Error: "column does not exist"
**Solution:** Ensure all ALTER TABLE statements from `script.sql` are executed

---

## 🚀 Next Steps

After inserting sample data:

1. **Test Authentication:** Login with restaurant owner credentials
2. **Test APIs:** Use the restaurant IDs to test all endpoints
3. **Add More Data:** Use these scripts as templates for more restaurants
4. **Update Images:** Replace Unsplash URLs with actual restaurant images
5. **Add Real Reviews:** Insert sample reviews for restaurants

---

## 📞 Support

For issues or questions:
- Check the main `RESTAURANT_API_DOCUMENTATION.md`
- Verify database schema matches `script.sql`
- Ensure all foreign key relationships are correct

---

**Last Updated:** January 2025  
**Version:** 1.0  
**Status:** Ready for Testing

