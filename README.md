# OneQlick Backend - Clean Startup

A clean FastAPI-based backend startup project with database connections, exception handling, and common response schemas.

## ✅ **Current Status: Clean Startup Ready**

### 🎯 **Core Features**

- ✅ **Database Setup**: PostgreSQL connection with SQLAlchemy
- ✅ **Redis Integration**: Caching and session management
- ✅ **Exception Handling**: Custom exception classes and handlers
- ✅ **Common Response Schema**: Standardized API response format
- ✅ **Health Check**: Database and Redis connection monitoring
- ✅ **Clean Architecture**: Minimal, focused structure
- ✅ **Complete Database Models**: All tables from SQL script implemented

### 🚀 **Available Endpoints**

| Endpoint    | Method | Description                    | Status     |
| ----------- | ------ | ------------------------------ | ---------- |
| `/`         | GET    | Root endpoint                  | ✅ Working |
| `/health`   | GET    | Health check with DB/Redis     | ✅ Working |

### 📊 **Database Models**

The application includes comprehensive database models based on the SQL script:

**Core Models:**
- `User` - Users with different roles (customer, admin, delivery_partner, restaurant_owner)
- `Address` - User delivery addresses
- `Restaurant` - Restaurant information and settings
- `Category` - Food categories
- `FoodItem` - Menu items with variants
- `FoodVariant` - Food item variants (size, extras)
- `Order` - Order management with status tracking
- `OrderItem` - Individual items in orders
- `DeliveryPartner` - Delivery partner details
- `OrderTracking` - Order status tracking
- `Coupon` - Discount and promotional codes
- `UserCouponUsage` - Coupon usage tracking
- `Review` - Customer reviews and ratings
- `Notification` - System notifications

**Authentication Models:**
- `RefreshToken` - JWT refresh token management
- `OAuthProvider` - OAuth provider integration
- `OTPVerification` - OTP verification system
- `UserSession` - User session management
- `PasswordResetToken` - Password reset functionality

**Additional Models:**
- `Cart` - Shopping cart
- `CartItem` - Cart items
- `UserWallet` - User wallet for payments

## 🗄️ **Database Configuration**

**Connected to:** Supabase PostgreSQL  
**Status:** ✅ Connection ready and tested

## 📖 **Health Check**

The `/health` endpoint provides:
- Database connection status
- Redis connection status
- Overall service health

## 🛠️ **Setup & Installation**

1. **Install dependencies:**

   ```shell
   pip install -r requirements.txt
   ```

2. **Environment Configuration:**

   Create a `.env` file with:
   ```env
   DATABASE_URL=postgresql+psycopg://user:password@host:port/database
   REDIS_HOST=localhost
   REDIS_PORT=6379
   REDIS_PASSWORD=your_redis_password
   ```

3. **Run the development server:**

   ```shell
   uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

4. **Access the API documentation:**

   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

5. **Test the health check:**
   ```shell
   curl http://localhost:8000/health
   ```

## 📁 **Project Structure**

```
app/
├── api/
│   ├── exception.py                       # ✅ Custom exception classes
│   └── schemas/
│       └── common_schemas.py              # ✅ Common response schemas
├── config/
│   ├── config.py                          # ✅ Configuration management
│   └── logger.py                          # ✅ Logging setup
├── infra/
│   ├── db/postgres/
│   │   ├── base.py                        # ✅ SQLAlchemy base
│   │   ├── postgres_config.py             # ✅ Database configuration
│   │   └── models/                        # ✅ All database models
│   │       ├── user.py                    # ✅ User model
│   │       ├── address.py                 # ✅ Address model
│   │       ├── restaurant.py              # ✅ Restaurant model
│   │       ├── category.py                # ✅ Category model
│   │       ├── food_item.py               # ✅ Food item model
│   │       ├── food_variant.py            # ✅ Food variant model
│   │       ├── order.py                   # ✅ Order model
│   │       ├── order_item.py              # ✅ Order item model
│   │       ├── delivery_partner.py        # ✅ Delivery partner model
│   │       ├── order_tracking.py          # ✅ Order tracking model
│   │       ├── coupon.py                  # ✅ Coupon model
│   │       ├── user_coupon_usage.py       # ✅ User coupon usage model
│   │       ├── review.py                  # ✅ Review model
│   │       ├── notification.py            # ✅ Notification model
│   │       ├── refresh_token.py           # ✅ Refresh token model
│   │       ├── oauth_provider.py          # ✅ OAuth provider model
│   │       ├── otp_verification.py        # ✅ OTP verification model
│   │       ├── user_session.py            # ✅ User session model
│   │       ├── password_reset_token.py    # ✅ Password reset token model
│   │       ├── cart.py                    # ✅ Cart model
│   │       ├── cart_item.py               # ✅ Cart item model
│   │       └── user_wallet.py             # ✅ User wallet model
│   └── redis/
│       └── repositories/
│           └── redis_repositories.py      # ✅ Redis operations
├── utils/
│   ├── date_utils.py                      # ✅ Date utilities
│   └── enums.py                           # ✅ All database enums
└── main.py                                # ✅ FastAPI application
```

## 🎯 **Next Development Steps**

1. **Add API Routes** - RESTful endpoints for your business logic
2. **Add Business Logic** - Domain services and repositories
3. **Add Authentication APIs** - Login, register, JWT tokens
4. **Add More Features** - Based on your specific requirements

## 🧪 **Testing**

**Health Check Results:**
- ✅ Database connection: Working
- ✅ Redis connection: Working (if configured)
- ✅ Exception handling: Working
- ✅ Common response format: Working
- ✅ All database models: Ready

---

**🎉 OneQlick Backend is ready for development with complete database models!**