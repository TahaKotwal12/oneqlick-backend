# 🎯 COMPLETE RESTAURANT SIGNUP FLOW - IMPLEMENTATION SUMMARY

## **📊 PROBLEM ANALYSIS**

### **Issue:**
- Partner App collects restaurant data during signup (`restaurant_name`, `cuisine_type`)
- Backend was ignoring this data and hardcoding role as `customer`
- After OTP verification, no restaurant was created
- Same backend serves both User App (customers) and Partner App (partners)

---

## **✅ SOLUTION IMPLEMENTED**

### **1. Made Signup Schema Flexible**
**File:** `app/api/schemas/auth_schemas.py`

**Changes:**
```python
class SignupRequest(BaseModel):
    # ... existing fields ...
    role: Optional[str] = Field(default="customer", pattern="^(customer|restaurant_owner|delivery_partner|admin)$")
    additional_data: Optional[Dict[str, Any]] = None
```

**Benefits:**
- ✅ User App: Sends no role → defaults to `customer`
- ✅ Partner App: Sends role + additional_data → stored properly
- ✅ Backward compatible with existing User App

---

### **2. Updated Pending User Model**
**File:** `app/infra/db/postgres/models/pending_user.py`

**Changes:**
```python
additional_data = Column(String)  # JSON string for partner-specific data
```

---

### **3. Updated Signup Endpoint**
**File:** `app/api/routes/auth.py`

**Changes:**
```python
# Serialize additional_data to JSON
additional_data_json = json.dumps(request.additional_data) if request.additional_data else None

# Create pending user with role and additional_data
pending_user = PendingUserUtils.create_pending_user(
    db=db,
    # ... other fields ...
    role=request.role or UserRole.CUSTOMER.value,
    additional_data=additional_data_json
)
```

---

### **4. Updated Pending User Utils**
**File:** `app/utils/pending_user_utils.py`

**Changes:**

#### **A. create_pending_user:**
```python
def create_pending_user(
    # ... existing params ...
    additional_data: Optional[str] = None
) -> PendingUser:
    # Stores additional_data in pending user
```

#### **B. verify_pending_user:**
```python
def verify_pending_user(db: Session, verification_token: str) -> Optional[User]:
    # ... create user ...
    
    # If restaurant owner, create restaurant automatically
    if pending_user.role == UserRole.RESTAURANT_OWNER.value and pending_user.additional_data:
        additional_data = json.loads(pending_user.additional_data)
        
        restaurant = Restaurant(
            owner_id=user.user_id,
            name=additional_data.get('restaurant_name'),
            cuisine_type=additional_data.get('cuisine_type'),
            # ... default values for other fields ...
        )
        db.add(restaurant)
```

---

### **5. Created Database Migration**
**File:** `alembic/versions/001_add_additional_data_to_pending_users.py`

**Purpose:**
- Adds `additional_data` column to `core_mstr_one_qlick_pending_users_tbl`

---

## **📱 COMPLETE USER FLOW**

### **Restaurant Owner Signup:**

1. **Partner App - Signup Screen:**
   - User fills: Name, Email, Phone, Password
   - **Restaurant fields:** Restaurant Name, Cuisine Type
   - Submits form

2. **Frontend sends to backend:**
   ```json
   {
     "first_name": "Taha",
     "last_name": "Kotwal",
     "email": "codisisofficial@gmail.com",
     "phone": "+917219342956",
     "password": "******",
     "role": "restaurant_owner",
     "additional_data": {
       "restaurant_name": "Taha's Spice Kitchen",
       "cuisine_type": "North Indian",
       "fssai_license": "12345678901234"
     }
   }
   ```

3. **Backend - Signup Endpoint:**
   - Creates `PendingUser` with role=`restaurant_owner`
   - Stores `additional_data` as JSON string
   - Sends OTP to email

4. **User verifies OTP:**
   - Frontend sends OTP code
   - Backend calls `verify_pending_user()`

5. **Backend - OTP Verification:**
   - Creates `User` with role=`restaurant_owner`
   - **Automatically creates `Restaurant`** using data from `additional_data`:
     - Name: "Taha's Spice Kitchen"
     - Cuisine: "North Indian"
     - Phone/Email: From user data
     - Default values: Address, timings, fees

6. **User logs in:**
   - Restaurant already exists!
   - Profile shows restaurant data
   - Can edit details in Restaurant Settings

---

## **🔄 DATABASE MIGRATION STEPS**

### **Run Migration:**
```bash
cd oneqlick-backend
alembic upgrade head
```

This will add the `additional_data` column to the pending_users table.

---

## **✅ BENEFITS OF THIS APPROACH**

1. ✅ **Single Backend** - Same auth endpoints for User App & Partner App
2. ✅ **Backward Compatible** - User App still works (role defaults to customer)
3. ✅ **Automatic** - Restaurant created during OTP verification
4. ✅ **Flexible** - Can add more partner types (delivery_partner) easily
5. ✅ **Clean** - No manual SQL scripts needed
6. ✅ **User-Friendly** - Restaurant owners don't need separate onboarding

---

## **🚀 DEPLOYMENT CHECKLIST**

### **Backend:**
- [x] Update schema (SignupRequest)
- [x] Update model (PendingUser)
- [x] Update signup endpoint
- [x] Update pending_user_utils
- [x] Create migration file
- [ ] Run migration on Railway
- [ ] Build & push Docker image
- [ ] Deploy to Railway

### **Frontend:**
- [x] Already sending role & additional_data
- [x] No changes needed!

---

## **🧪 TESTING**

### **Test Case 1: Restaurant Owner Signup**
1. Open Partner App
2. Tap "Sign Up"
3. Select "Restaurant Owner"
4. Fill all fields including restaurant name
5. Submit
6. Verify OTP
7. Login
8. Check Profile → Should show restaurant name
9. Go to Restaurant Settings → Should show all restaurant details

### **Test Case 2: Customer Signup (User App)**
1. Open User App
2. Sign up normally (no role field)
3. Verify OTP
4. Login
5. Should work as before (role=customer, no restaurant)

---

## **📝 NOTES**

- Restaurant is created with **default values** for address, timings, etc.
- Restaurant owner can update these in **Restaurant Settings** screen
- If restaurant creation fails, user is still created (logged as error)
- Additional data is stored as JSON string for flexibility

---

**Status:** ✅ **READY TO DEPLOY**

After running the migration and deploying, restaurant owners will automatically get their restaurant created during signup!
