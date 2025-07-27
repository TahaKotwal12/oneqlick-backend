# OneQlick Food Delivery Backend

A FastAPI-based backend for the OneQlick food delivery application, designed for Indian users.

## ✅ **Current Status: User APIs Complete**

### 🎯 **Completed Features**
- ✅ **Database Setup**: All tables created in Supabase PostgreSQL
- ✅ **User CRUD APIs**: Complete user management system
- ✅ **Clean Architecture**: Repository pattern, service layer, proper separation
- ✅ **API Documentation**: Complete with curl examples
- ✅ **No Legacy Dependencies**: Cleaned from old Enlight project

### 🚀 **User Management APIs**

| Endpoint | Method | Description | Status |
|----------|--------|-------------|---------|
| `/api/v1/users` | POST | Create new user | ✅ Working |
| `/api/v1/users/{user_id}` | GET | Get user by ID | ✅ Working |
| `/api/v1/users` | GET | List users (with filters) | ✅ Working |
| `/api/v1/users/{user_id}` | PUT | Update user | ✅ Working |
| `/api/v1/users/{user_id}` | DELETE | Soft delete user | ✅ Working |
| `/api/v1/users/{user_id}/verify-email` | POST | Verify email | ✅ Working |
| `/api/v1/users/{user_id}/verify-phone` | POST | Verify phone | ✅ Working |

### 📊 **Database Models**

The application includes the following core models:
- ✅ `User` - Users with different roles (customer, admin, delivery_partner, restaurant_owner)
- ✅ `Restaurant` - Restaurant information and settings
- ✅ `Order` - Order management with status tracking
- ✅ `FoodItem` - Menu items with variants
- ✅ `DeliveryPartner` - Delivery partner details
- ✅ `Address` - Customer delivery addresses
- ✅ `Coupon` - Discount and promotional codes
- ✅ `Review` - Customer reviews and ratings
- ✅ `Notification` - System notifications

## 🗄️ **Database Configuration**

**Connected to:** Supabase PostgreSQL  
**Status:** ✅ All tables created and working

## 📖 **API Documentation**

Complete API documentation with curl examples available in:
- `api_docs/user_api_docs.md` - User API documentation
- `api_docs/test_user_api.sh` - Test script for all user endpoints

## 🛠️ **Setup & Installation**

1. **Install dependencies using uv:**
   ```shell
   uv sync
   ```

2. **Database is already configured:**
   - Supabase PostgreSQL connection ready
   - All tables created and indexed

3. **Run the development server:**
   ```shell
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

5. **Test the APIs:**
   ```shell
   chmod +x api_docs/test_user_api.sh
   ./api_docs/test_user_api.sh
   ```

## 📁 **Project Structure**

```
app/
├── api/
│   ├── routes/user_controller.py          # ✅ Complete User CRUD
│   └── schemas/                           # ✅ User schemas
├── domain/services/user_service.py        # ✅ Business logic
├── infra/
│   ├── db/postgres/
│   │   ├── models/                        # ✅ All 14 food delivery models
│   │   └── repositories/user_repository.py # ✅ Database operations
│   └── redis/                             # 🔄 Ready for caching
├── config/                                # ✅ Clean configuration
└── main.py                                # ✅ OneQlick API server

api_docs/
├── user_api_docs.md                      # ✅ Complete documentation
└── test_user_api.sh                      # ✅ Test script
```

## 🎯 **Next Development Steps**

1. **Restaurant APIs** - Menu management, restaurant profiles
2. **Order APIs** - Order lifecycle management
3. **Authentication** - JWT tokens, login/logout
4. **Address APIs** - Delivery address management
5. **Payment Integration** - Razorpay/UPI integration

## 🧪 **Testing**

**User API Test Results:**
- ✅ Create User: Working (User ID: 401fee20-b126-49e2-bd18-7dc36bfa7e36)
- ✅ All endpoints functional
- ✅ Database operations successful
- ✅ No legacy header dependencies

## 📊 **User Roles Supported**

- `customer` - End users who order food
- `admin` - System administrators  
- `delivery_partner` - Delivery personnel
- `restaurant_owner` - Restaurant managers

---

**🎉 OneQlick Backend is ready for food delivery development!**