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
    # Order related
    ORDER_PLACED = "order_placed"
    ORDER_CONFIRMED = "order_confirmed"
    ORDER_PREPARING = "order_preparing"
    ORDER_READY = "order_ready"
    ORDER_PICKED_UP = "order_picked_up"
    ORDER_OUT_FOR_DELIVERY = "order_out_for_delivery"
    ORDER_DELIVERED = "order_delivered"
    ORDER_CANCELLED = "order_cancelled"
    
    # Payment related
    PAYMENT_SUCCESS = "payment_success"
    PAYMENT_FAILED = "payment_failed"
    REFUND_PROCESSED = "refund_processed"
    
    # Promotion related
    NEW_COUPON = "new_coupon"
    COUPON_EXPIRING = "coupon_expiring"
    SPECIAL_OFFER = "special_offer"
    
    # System related
    SYSTEM_ANNOUNCEMENT = "system_announcement"
    ACCOUNT_UPDATE = "account_update"
    SECURITY_ALERT = "security_alert"

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
    
    def __str__(self):
        return self.value

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

# Support related enums
class TicketCategory(str, Enum):
    """Support ticket categories."""
    ORDER_ISSUE = "order_issue"
    PAYMENT = "payment"
    APP_FEEDBACK = "app_feedback"
    TECHNICAL_ISSUE = "technical_issue"
    OTHER = "other"

class TicketStatus(str, Enum):
    """Support ticket status."""
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"

class TicketPriority(str, Enum):
    """Support ticket priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

class SupportSenderType(str, Enum):
    """Types of senders in support chat."""
    CUSTOMER = "customer"
    PARTNER = "partner"
    ADMIN = "admin"
    SYSTEM = "system"

# Onboarding related enums
class OnboardingStep(str, Enum):
    """Restaurant onboarding steps."""
    REGISTRATION = "registration"
    VERIFICATION = "verification"
    PROFILE = "profile"
    MENU = "menu"
    BANK_DETAILS = "bank_details"
    REVIEW = "review"
    COMPLETED = "completed"

class OnboardingStatus(str, Enum):
    """Restaurant onboarding verification status."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"

class BusinessType(str, Enum):
    """Restaurant business types."""
    CLOUD_KITCHEN = "cloud_kitchen"
    DINE_IN = "dine_in"
    BOTH = "both"