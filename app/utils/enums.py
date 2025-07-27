from enum import Enum

class Status(str, Enum):
    """
    General status enum for records.
    """
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class OrderStatus(str, Enum):
    """
    Order status for food delivery orders.
    """
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY_FOR_PICKUP = "ready_for_pickup"
    PICKED_UP = "picked_up"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentStatus(str, Enum):
    """
    Payment status for orders.
    """
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    """
    Payment methods available.
    """
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    WALLET = "wallet"

class UserRole(str, Enum):
    """
    User roles in the food delivery system.
    """
    CUSTOMER = "customer"
    ADMIN = "admin"
    DELIVERY_PARTNER = "delivery_partner"
    RESTAURANT_OWNER = "restaurant_owner"

class DeliveryStatus(str, Enum):
    """
    Delivery tracking status.
    """
    ASSIGNED = "assigned"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"