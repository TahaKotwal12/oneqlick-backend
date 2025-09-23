from enum import Enum


# User related enums
class UserRole(str, Enum):
    """User roles in the food delivery system."""
    CUSTOMER = "customer"
    ADMIN = "admin"
    DELIVERY_PARTNER = "delivery_partner"
    RESTAURANT_OWNER = "restaurant_owner"

class UserStatus(str, Enum):
    """User status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

# Restaurant related enums
class RestaurantStatus(str, Enum):
    """Restaurant status enum."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class FoodStatus(str, Enum):
    """Food item status enum."""
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    OUT_OF_STOCK = "out_of_stock"

# Order related enums
class OrderStatus(str, Enum):
    """Order status for food delivery orders."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY_FOR_PICKUP = "ready_for_pickup"
    PICKED_UP = "picked_up"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(str, Enum):
    """Payment status for orders."""
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    """Payment methods available."""
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    WALLET = "wallet"
    NETBANKING = "netbanking"
    COD = "cod"

# Delivery related enums
class VehicleType(str, Enum):
    """Vehicle types for delivery partners."""
    BICYCLE = "bicycle"
    MOTORCYCLE = "motorcycle"
    CAR = "car"

class AvailabilityStatus(str, Enum):
    """Delivery partner availability status."""
    AVAILABLE = "available"
    BUSY = "busy"
    OFFLINE = "offline"

# Coupon related enums
class CouponType(str, Enum):
    """Coupon types."""
    PERCENTAGE = "percentage"
    FIXED_AMOUNT = "fixed_amount"
    FREE_DELIVERY = "free_delivery"

# Notification related enums
class NotificationType(str, Enum):
    """Notification types."""
    ORDER_UPDATE = "order_update"
    PROMOTION = "promotion"
    SYSTEM = "system"

# Additional enums for enhanced functionality
class AddressType(str, Enum):
    """Address types."""
    HOME = "home"
    WORK = "work"
    RESTAURANT = "restaurant"
    OTHER = "other"

class Gender(str, Enum):
    """Gender options."""
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

class TransactionType(str, Enum):
    """Wallet transaction types."""
    CREDIT = "credit"
    DEBIT = "debit"
    REFUND = "refund"

class SearchType(str, Enum):
    """Search types."""
    RESTAURANT = "restaurant"
    FOOD = "food"
    GENERAL = "general"

class ReviewType(str, Enum):
    """Review types."""
    RESTAURANT = "restaurant"
    DELIVERY = "delivery"