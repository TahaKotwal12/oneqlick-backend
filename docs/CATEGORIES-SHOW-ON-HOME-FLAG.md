# Categories with show_on_home Flag - Implementation Summary

## Overview
Added `show_on_home` flag to categories table to control which categories appear on home/search screens. This allows you to have many categories in the database but only show selected/featured ones on the frontend.

---

## 🎯 Problem Solved

**Before:** All categories in the database would be shown on home/search screens.

**After:** Only categories with `show_on_home = TRUE` are displayed on home/search screens. Other categories can still be searched and used, but won't clutter the main screens.

---

## 📊 Database Changes

### New Column Added
```sql
show_on_home BOOLEAN DEFAULT FALSE
```

**Purpose:** Controls whether a category appears on home/search screens
- `TRUE` = Show on home/search (featured categories)
- `FALSE` = Available for search only (not featured)

---

## 🔧 Backend Changes

### 1. **Model Updated** - `app/infra/db/postgres/models/category.py`
```python
show_on_home = Column(Boolean, default=False)  # Show on home/search screens
```

### 2. **Schemas Updated** - `app/api/schemas/category_schemas.py`
- Added `show_on_home` to `CategoryBase`
- Added `show_on_home` to `CategoryUpdate`
- Added `show_on_home` to `CategoryResponse`

### 3. **API Routes Updated** - `app/api/routes/categories.py`
**New Query Parameter:**
```python
GET /api/v1/categories?show_on_home=true
```

**Example Requests:**
```bash
# Get all categories
GET /api/v1/categories

# Get only active categories
GET /api/v1/categories?is_active=true

# Get only featured categories (for home/search screens)
GET /api/v1/categories?is_active=true&show_on_home=true

# Get all categories including non-featured
GET /api/v1/categories?is_active=true&show_on_home=false
```

---

## 📱 Frontend Changes

### 1. **API Service Updated** - `services/api.ts`
```typescript
categoryAPI.getCategories({
  is_active: true,
  show_on_home: true  // Get only featured categories
});
```

### 2. **Hook Updated** - `hooks/useCategories.ts`
Now fetches only featured categories:
```typescript
const response = await categoryAPI.getCategories({ 
  is_active: true,
  show_on_home: true  // Only get featured categories
});
```

### 3. **Screens Updated**
- `app/(tabs)/home.tsx` - Uses `useCategories()` hook
- `app/(tabs)/search.tsx` - Uses `useCategories()` hook

Both screens now automatically show only featured categories!

---

## 💾 SQL Script Updated

### File: `scripts/setup_food_categories.sql`

**What Changed:**
1. Added `show_on_home` column to ALTER TABLE
2. Set `show_on_home = TRUE` for the 8 featured categories

**The 8 Featured Categories:**
1. South Indian
2. North Indian
3. Chinese
4. Beverages
5. Fast Food
6. Breakfast
7. Kokani
8. Desserts

---

## 🚀 How to Use

### For Admins (Future Admin Panel):

#### **Add a Featured Category:**
```json
POST /api/v1/categories
{
  "name": "Italian",
  "description": "Authentic Italian cuisine",
  "icon": "pasta",
  "color": "#FF6B6B",
  "is_active": true,
  "show_on_home": true,  // ← Show on home screen
  "sort_order": 9
}
```

#### **Add a Non-Featured Category:**
```json
POST /api/v1/categories
{
  "name": "Mexican",
  "description": "Spicy Mexican food",
  "icon": "taco",
  "color": "#FFA500",
  "is_active": true,
  "show_on_home": false,  // ← Don't show on home, but searchable
  "sort_order": 10
}
```

#### **Toggle Featured Status:**
```json
PUT /api/v1/categories/{category_id}
{
  "show_on_home": true  // Make it featured
}
```

---

## 📋 Example Scenarios

### Scenario 1: Add 50 Categories
You can add 50 different cuisine categories to your database:
- Set `show_on_home = TRUE` for 8-10 popular ones
- Set `show_on_home = FALSE` for the rest
- **Result:** Home screen shows only 8-10 categories, but users can search all 50

### Scenario 2: Seasonal Categories
- During Diwali: Set "Sweets" category `show_on_home = TRUE`
- After Diwali: Set it back to `FALSE`
- **Result:** Dynamic featured categories based on season/events

### Scenario 3: Regional Categories
- In Mumbai: Show "Vada Pav", "Pav Bhaji" on home
- In Delhi: Show "Chole Bhature", "Parathas" on home
- **Result:** Location-based featured categories (future enhancement)

---

## ✅ Testing

### 1. Run SQL Script
```bash
psql -U your_username -d your_database -f scripts/setup_food_categories.sql
```

### 2. Test Backend API
```bash
# Get featured categories
curl http://localhost:8000/api/v1/categories?show_on_home=true

# Get all categories
curl http://localhost:8000/api/v1/categories
```

### 3. Test Frontend
```bash
cd oneQlick-User-App
npx expo start
```

**Expected Result:**
- Home screen shows only 8 featured categories
- Search screen shows only 8 featured categories
- All categories are searchable via search API

---

## 🎯 Benefits

1. **Clean UI:** Home screen not cluttered with too many categories
2. **Flexible:** Easy to add/remove featured categories from admin panel
3. **Scalable:** Can have 100+ categories in DB, show only top 10
4. **Dynamic:** Change featured categories based on trends, seasons, location
5. **Searchable:** All categories still accessible via search

---

## 📝 Next Steps

1. ✅ Run the updated SQL script
2. ✅ Deploy backend with new changes
3. ✅ Test frontend integration
4. 🔜 Build admin panel to manage `show_on_home` flag
5. 🔜 Add analytics to track which categories are most popular
6. 🔜 Implement location-based featured categories

---

## 🔑 Key Points

- **Default:** New categories have `show_on_home = FALSE`
- **Featured:** Only categories with `show_on_home = TRUE` appear on home/search
- **Searchable:** All active categories are searchable regardless of `show_on_home`
- **Admin Control:** Admins can toggle this flag via API
- **No Breaking Changes:** Existing functionality remains intact

---

**Perfect solution for managing featured vs. all categories!** 🎉
