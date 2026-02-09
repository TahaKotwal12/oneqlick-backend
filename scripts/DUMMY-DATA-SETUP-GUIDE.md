# 🎯 Partner App Dummy Data Setup Guide

## **📋 Overview**

This guide explains how to set up test data for the OneQlick Partner App using the provided SQL script.

---

## **📁 Script Location**

```
oneqlick-backend/scripts/setup_partner_dummy_data.sql
```

---

## **🎯 What This Script Creates**

### **1. Test Users (3)**

#### **Restaurant Owner**
- **Email:** `restaurant@oneqlick.com`
- **Password:** `Restaurant@123`
- **Phone:** `+919876543210`
- **Name:** Rajesh Kumar
- **Role:** `restaurant_owner`
- **Status:** Active, Email Verified

#### **Delivery Partner**
- **Email:** `partner@oneqlick.com`
- **Password:** `Partner@123`
- **Phone:** `+919876543211`
- **Name:** Amit Sharma
- **Role:** `delivery_partner`
- **Status:** Active, Email Verified
- **Vehicle:** Motorcycle (MH02AB1234)
- **License:** DL1234567890

#### **Customer**
- **Email:** `customer@oneqlick.com`
- **Password:** `Customer@123`
- **Phone:** `+919876543212`
- **Name:** Priya Patel
- **Role:** `customer`
- **Status:** Active, Email Verified

---

### **2. Restaurant**

**Spice Kitchen - Mumbai**
- **Location:** Bandra West, Mumbai
- **Cuisine:** Indian, North Indian, South Indian
- **Rating:** 4.5 ⭐ (250 ratings)
- **Delivery Time:** 30 minutes
- **Min Order:** ₹100
- **Delivery Fee:** ₹40
- **Hours:** 9:00 AM - 11:00 PM
- **Status:** Active & Open

---

### **3. Food Categories (6)**

1. **Starters** - Appetizers and starters
2. **Main Course** - Main dishes and curries
3. **Breads** - Naan, roti, and other breads
4. **Rice & Biryani** - Rice dishes and biryani
5. **Desserts** - Sweet dishes and desserts
6. **Beverages** - Drinks and beverages

---

### **4. Menu Items (14)**

#### **Starters (3)**
- Paneer Tikka - ₹220
- Chicken Tikka - ₹250 (₹230 discounted)
- Veg Spring Rolls - ₹180

#### **Main Course (3)**
- Butter Chicken - ₹320 ⭐ 4.9
- Paneer Butter Masala - ₹280 (₹260 discounted)
- Dal Makhani - ₹240

#### **Breads (2)**
- Butter Naan - ₹50
- Garlic Naan - ₹60

#### **Rice & Biryani (2)**
- Chicken Biryani - ₹280 ⭐ 4.8
- Veg Biryani - ₹220 (₹200 discounted)

#### **Desserts (2)**
- Gulab Jamun - ₹80
- Rasmalai - ₹100

#### **Beverages (2)**
- Mango Lassi - ₹80
- Masala Chai - ₹40

---

### **5. Sample Orders (4)**

#### **Order 1: ORD-1001** (Pending)
- **Status:** Pending
- **Items:** Butter Chicken, Chicken Biryani
- **Total:** ₹694
- **Payment:** UPI (Paid)
- **Special Instructions:** "Extra spicy please"
- **Created:** 5 minutes ago

#### **Order 2: ORD-1002** (Preparing)
- **Status:** Preparing
- **Items:** Paneer Butter Masala, Paneer Tikka
- **Total:** ₹535
- **Payment:** Card (Paid)
- **Special Instructions:** "Less oil"
- **Created:** 15 minutes ago

#### **Order 3: ORD-1003** (Ready for Pickup)
- **Status:** Ready for Pickup
- **Items:** Veg Biryani, Gulab Jamun (x2)
- **Total:** ₹454.20
- **Payment:** UPI (Paid)
- **Assigned to:** Amit Sharma (Delivery Partner)
- **Created:** 25 minutes ago

#### **Order 4: ORD-1004** (Delivered)
- **Status:** Delivered
- **Items:** Butter Chicken (x2), Mango Lassi
- **Total:** ₹824.80
- **Payment:** UPI (Paid)
- **Rating:** 5 ⭐
- **Review:** "Excellent food and fast delivery!"
- **Delivered:** 30 minutes ago

---

## **🚀 How to Run the Script**

### **Method 1: Using psql (Command Line)**

```bash
# Connect to your PostgreSQL database
psql -h <host> -U <username> -d <database_name>

# Run the script
\i /path/to/oneqlick-backend/scripts/setup_partner_dummy_data.sql

# Or in one command:
psql -h <host> -U <username> -d <database_name> -f /path/to/setup_partner_dummy_data.sql
```

### **Method 2: Using Railway Dashboard**

1. Go to your Railway project
2. Click on your PostgreSQL database
3. Click "Query" tab
4. Copy and paste the entire SQL script
5. Click "Run Query"

### **Method 3: Using pgAdmin**

1. Open pgAdmin
2. Connect to your database
3. Right-click on your database → Query Tool
4. Open the SQL file or paste the content
5. Click Execute (F5)

### **Method 4: Using DBeaver**

1. Open DBeaver
2. Connect to your database
3. Open SQL Editor (SQL Editor button or Ctrl+])
4. Paste the script
5. Execute (Ctrl+Enter)

---

## **✅ Verification**

After running the script, you should see:

```
✅ Dummy data setup complete!

📧 Login Credentials:
   Restaurant Owner: restaurant@oneqlick.com / Restaurant@123
   Delivery Partner: partner@oneqlick.com / Partner@123
   Customer: customer@oneqlick.com / Customer@123

🏪 Restaurant: Spice Kitchen - Mumbai
   - 14 menu items across 6 categories
   - 4 sample orders (pending, preparing, ready, delivered)

🚀 You can now test the Partner App!
```

### **Verify Data Created**

Run these queries to verify:

```sql
-- Check users
SELECT email, first_name, last_name, role, status
FROM core_mstr_one_qlick_users_tbl
WHERE email LIKE '%oneqlick.com'
ORDER BY role;

-- Check restaurant
SELECT name, city, cuisine_type, rating, is_open
FROM core_mstr_one_qlick_restaurants_tbl
WHERE name = 'Spice Kitchen - Mumbai';

-- Check menu items
SELECT COUNT(*) as total_items
FROM core_mstr_one_qlick_food_items_tbl
WHERE restaurant_id IN (
    SELECT restaurant_id 
    FROM core_mstr_one_qlick_restaurants_tbl 
    WHERE name = 'Spice Kitchen - Mumbai'
);

-- Check orders
SELECT order_number, order_status, total_amount
FROM core_mstr_one_qlick_orders_tbl
WHERE restaurant_id IN (
    SELECT restaurant_id 
    FROM core_mstr_one_qlick_restaurants_tbl 
    WHERE name = 'Spice Kitchen - Mumbai'
)
ORDER BY created_at DESC;
```

---

## **🧪 Testing the Partner App**

### **Step 1: Login as Restaurant Owner**

1. Open Partner App
2. Enter credentials:
   - Email: `restaurant@oneqlick.com`
   - Password: `Restaurant@123`
3. You should see the Restaurant Dashboard

### **Step 2: Test Order Management**

1. Navigate to **Orders** tab
2. You should see:
   - **New Orders (1):** ORD-1001
   - **Active Orders (2):** ORD-1002, ORD-1003
   - **Completed Orders (1):** ORD-1004

3. Click on an order to view details
4. Try updating order status:
   - ORD-1001: pending → preparing
   - ORD-1002: preparing → ready_for_pickup

### **Step 3: Test Menu Management**

1. Navigate to **Menu** tab
2. You should see 14 menu items across 6 categories
3. Try:
   - Toggling item availability
   - Editing item details
   - Adding a new item
   - Deleting an item

### **Step 4: Test Statistics**

1. Navigate to **Dashboard** or **Stats**
2. You should see:
   - Today's Orders: 3
   - Pending Orders: 1
   - Revenue Today: ₹1,683.20
   - Monthly Orders: 4
   - Monthly Revenue: ₹2,508.00

### **Step 5: Login as Delivery Partner**

1. Logout from restaurant account
2. Login with:
   - Email: `partner@oneqlick.com`
   - Password: `Partner@123`
3. You should see the Delivery Dashboard

### **Step 6: Test Delivery Management**

1. Navigate to **Deliveries** tab
2. You should see:
   - Active Delivery: ORD-1003 (Ready for Pickup)
3. Try:
   - Updating delivery status
   - Viewing delivery details
   - Toggling online/offline status

---

## **🔧 Customization**

### **Change Passwords**

To generate a new bcrypt hash for a different password:

```python
import bcrypt
password = "YourNewPassword123"
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print(hashed.decode('utf-8'))
```

Then update the `password_hash` in the script.

### **Add More Menu Items**

Copy the INSERT statement for food items and modify:
- `food_item_id` (new UUID)
- `name`, `description`, `price`
- `category_id` (use existing category)
- `image` URL

### **Add More Orders**

Copy the INSERT statement for orders and modify:
- `order_id` (new UUID)
- `order_number` (e.g., ORD-1005)
- `order_status`, `total_amount`
- Add corresponding order items

---

## **🗑️ Cleanup (Optional)**

To remove all dummy data:

```sql
-- Delete in reverse order of dependencies
DELETE FROM core_mstr_one_qlick_order_items_tbl 
WHERE order_id IN (
    SELECT order_id FROM core_mstr_one_qlick_orders_tbl 
    WHERE order_number LIKE 'ORD-100%'
);

DELETE FROM core_mstr_one_qlick_orders_tbl 
WHERE order_number LIKE 'ORD-100%';

DELETE FROM core_mstr_one_qlick_food_items_tbl 
WHERE restaurant_id = '55555555-5555-5555-5555-555555555555';

DELETE FROM core_mstr_one_qlick_restaurants_tbl 
WHERE restaurant_id = '55555555-5555-5555-5555-555555555555';

DELETE FROM core_mstr_one_qlick_delivery_partners_tbl 
WHERE user_id = '22222222-2222-2222-2222-222222222222';

DELETE FROM core_mstr_one_qlick_addresses_tbl 
WHERE user_id = '33333333-3333-3333-3333-333333333333';

DELETE FROM core_mstr_one_qlick_categories_tbl 
WHERE category_id LIKE '66666666-6666-6666-6666-66666666666%';

DELETE FROM core_mstr_one_qlick_users_tbl 
WHERE email IN (
    'restaurant@oneqlick.com', 
    'partner@oneqlick.com', 
    'customer@oneqlick.com'
);
```

---

## **📊 Data Summary**

| Entity | Count | Details |
|--------|-------|---------|
| Users | 3 | 1 Restaurant Owner, 1 Delivery Partner, 1 Customer |
| Restaurants | 1 | Spice Kitchen - Mumbai |
| Categories | 6 | Starters, Main Course, Breads, Rice, Desserts, Beverages |
| Menu Items | 14 | Across all categories |
| Orders | 4 | 1 Pending, 1 Preparing, 1 Ready, 1 Delivered |
| Order Items | 9 | Total items across all orders |
| Addresses | 1 | Customer delivery address |
| Delivery Partners | 1 | With vehicle and license details |

---

## **🎯 Use Cases Covered**

✅ Restaurant owner login and dashboard
✅ Order management (view, update status)
✅ Menu management (view, edit, toggle availability)
✅ Statistics and analytics
✅ Delivery partner login
✅ Delivery request management
✅ Order tracking
✅ Customer orders
✅ Payment processing
✅ Reviews and ratings

---

## **🚨 Important Notes**

1. **UUIDs are fixed** - This makes it easier to reference in tests
2. **Passwords are hashed** - Using bcrypt with salt
3. **Timestamps are relative** - Orders created at different times for realism
4. **ON CONFLICT DO NOTHING** - Script is idempotent (can run multiple times)
5. **All users are verified** - email_verified and phone_verified are true

---

## **🎉 Success!**

You now have a fully populated database ready for testing the Partner App!

**Next Steps:**
1. Run the script in your database
2. Start the Partner App
3. Login with test credentials
4. Test all features
5. Report any issues

---

**Happy Testing! 🚀**
