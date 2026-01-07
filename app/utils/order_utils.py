"""
Order utility functions for OneQlick food delivery platform.
Handles order number generation, price calculations, validations, and business logic.
"""

from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional, Tuple
import math
from app.utils.enums import OrderStatus, PaymentStatus


# ============================================
# ORDER NUMBER GENERATION
# ============================================

def generate_order_number() -> str:
    """
    Generate unique order number in format: ORD-YYYYMMDD-XXXX
    
    Example: ORD-20260107-0001
    
    Note: In production, this should use a database sequence or Redis counter
    to ensure uniqueness across multiple instances.
    """
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    time_part = now.strftime("%H%M%S")
    
    # In production, replace this with database sequence or Redis INCR
    # For now, using timestamp-based approach
    order_number = f"ORD-{date_part}-{time_part}"
    
    return order_number


# ============================================
# PRICE CALCULATIONS
# ============================================

def calculate_delivery_fee(distance_km: float, base_fee: Decimal = Decimal('20.00')) -> Decimal:
    """
    Calculate delivery fee based on distance.
    
    Args:
        distance_km: Distance in kilometers
        base_fee: Base delivery fee
    
    Returns:
        Calculated delivery fee
    
    Pricing logic:
        - 0-2 km: Base fee (₹20)
        - 2-5 km: Base fee + ₹5 per km
        - 5-10 km: Base fee + ₹8 per km
        - 10+ km: Base fee + ₹10 per km
    """
    if distance_km <= 2:
        return base_fee
    elif distance_km <= 5:
        additional = Decimal(str((distance_km - 2) * 5))
        return base_fee + additional
    elif distance_km <= 10:
        additional = Decimal(str((distance_km - 5) * 8 + 15))  # 15 from 2-5km range
        return base_fee + additional
    else:
        additional = Decimal(str((distance_km - 10) * 10 + 55))  # 55 from previous ranges
        return base_fee + additional


def calculate_tax(subtotal: Decimal, tax_rate: Decimal = Decimal('0.05')) -> Decimal:
    """
    Calculate tax amount (GST/VAT).
    
    Args:
        subtotal: Subtotal amount before tax
        tax_rate: Tax rate (default 5% = 0.05)
    
    Returns:
        Tax amount
    """
    tax_amount = subtotal * tax_rate
    # Round to 2 decimal places
    return tax_amount.quantize(Decimal('0.01'))


def calculate_platform_fee(subtotal: Decimal, fee_rate: Decimal = Decimal('0.02')) -> Decimal:
    """
    Calculate platform fee.
    
    Args:
        subtotal: Subtotal amount
        fee_rate: Platform fee rate (default 2% = 0.02)
    
    Returns:
        Platform fee amount
    """
    platform_fee = subtotal * fee_rate
    return platform_fee.quantize(Decimal('0.01'))


def calculate_order_totals(
    subtotal: Decimal,
    delivery_fee: Decimal,
    discount_amount: Decimal = Decimal('0.00'),
    tax_rate: Decimal = Decimal('0.05'),
    platform_fee: Optional[Decimal] = None
) -> Tuple[Decimal, Decimal, Decimal]:
    """
    Calculate order totals including tax and final amount.
    
    Args:
        subtotal: Subtotal of all items
        delivery_fee: Delivery fee
        discount_amount: Discount amount (if coupon applied)
        tax_rate: Tax rate
        platform_fee: Platform fee (optional, calculated if not provided)
    
    Returns:
        Tuple of (tax_amount, calculated_platform_fee, total_amount)
    """
    # Calculate platform fee if not provided
    if platform_fee is None:
        platform_fee = calculate_platform_fee(subtotal)
    
    # Calculate tax on subtotal (before discount)
    tax_amount = calculate_tax(subtotal, tax_rate)
    
    # Calculate total: subtotal + tax + delivery_fee + platform_fee - discount
    total_amount = subtotal + tax_amount + delivery_fee + platform_fee - discount_amount
    
    # Ensure total is not negative
    if total_amount < Decimal('0.00'):
        total_amount = Decimal('0.00')
    
    return tax_amount, platform_fee, total_amount


# ============================================
# DISTANCE CALCULATION
# ============================================

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula.
    
    Args:
        lat1: Latitude of point 1
        lon1: Longitude of point 1
        lat2: Latitude of point 2
        lon2: Longitude of point 2
    
    Returns:
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return round(distance, 2)


# ============================================
# ORDER STATUS VALIDATIONS
# ============================================

def validate_status_transition(current_status: OrderStatus, new_status: OrderStatus) -> bool:
    """
    Validate if order status transition is allowed.
    
    Args:
        current_status: Current order status
        new_status: New order status to transition to
    
    Returns:
        True if transition is valid, False otherwise
    """
    # Define valid status transitions
    valid_transitions = {
        OrderStatus.PENDING: [OrderStatus.CONFIRMED, OrderStatus.CANCELLED],
        OrderStatus.CONFIRMED: [OrderStatus.PREPARING, OrderStatus.CANCELLED],
        OrderStatus.PREPARING: [OrderStatus.READY_FOR_PICKUP, OrderStatus.CANCELLED],
        OrderStatus.READY_FOR_PICKUP: [OrderStatus.PICKED_UP, OrderStatus.CANCELLED],
        OrderStatus.PICKED_UP: [OrderStatus.DELIVERED, OrderStatus.CANCELLED],
        OrderStatus.DELIVERED: [OrderStatus.REFUNDED],  # Can refund delivered orders
        OrderStatus.CANCELLED: [OrderStatus.REFUNDED],
        OrderStatus.REFUNDED: [],  # Terminal state
    }
    
    allowed_statuses = valid_transitions.get(current_status, [])
    return new_status in allowed_statuses


def is_order_cancellable(order_status: OrderStatus, created_at: datetime) -> Tuple[bool, Optional[str]]:
    """
    Check if order can be cancelled.
    
    Args:
        order_status: Current order status
        created_at: Order creation timestamp
    
    Returns:
        Tuple of (can_cancel: bool, reason: Optional[str])
    """
    # Cannot cancel if already delivered or refunded
    if order_status in [OrderStatus.DELIVERED, OrderStatus.REFUNDED, OrderStatus.CANCELLED]:
        return False, f"Order cannot be cancelled in {order_status.value} status"
    
    # Cannot cancel if already picked up (delivery in progress)
    if order_status == OrderStatus.PICKED_UP:
        return False, "Order is already out for delivery and cannot be cancelled"
    
    # Check if order is too old (e.g., more than 1 hour in preparing state)
    if order_status == OrderStatus.PREPARING:
        time_since_creation = datetime.now(timezone.utc) - created_at
        if time_since_creation > timedelta(hours=1):
            return False, "Order is being prepared and cannot be cancelled at this stage"
    
    return True, None


def is_order_ratable(order_status: OrderStatus, delivery_time: Optional[datetime]) -> Tuple[bool, Optional[str]]:
    """
    Check if order can be rated.
    
    Args:
        order_status: Current order status
        delivery_time: Actual delivery timestamp
    
    Returns:
        Tuple of (can_rate: bool, reason: Optional[str])
    """
    # Can only rate delivered orders
    if order_status != OrderStatus.DELIVERED:
        return False, "Order must be delivered before rating"
    
    # Check if delivery time is set
    if not delivery_time:
        return False, "Order delivery time not recorded"
    
    # Check if rating window has expired (e.g., 7 days)
    time_since_delivery = datetime.now(timezone.utc) - delivery_time
    if time_since_delivery > timedelta(days=7):
        return False, "Rating period has expired (7 days after delivery)"
    
    return True, None


# ============================================
# TIME CALCULATIONS
# ============================================

def calculate_estimated_delivery_time(
    prep_time_minutes: int,
    distance_km: float,
    avg_speed_kmh: float = 30.0
) -> datetime:
    """
    Calculate estimated delivery time.
    
    Args:
        prep_time_minutes: Restaurant preparation time in minutes
        distance_km: Distance to delivery location in km
        avg_speed_kmh: Average delivery speed in km/h (default 30 km/h)
    
    Returns:
        Estimated delivery datetime
    """
    # Calculate travel time
    travel_time_hours = distance_km / avg_speed_kmh
    travel_time_minutes = int(travel_time_hours * 60)
    
    # Add buffer time (10 minutes for pickup, traffic, etc.)
    buffer_minutes = 10
    
    # Total time = prep time + travel time + buffer
    total_minutes = prep_time_minutes + travel_time_minutes + buffer_minutes
    
    # Calculate estimated delivery time
    estimated_time = datetime.now(timezone.utc) + timedelta(minutes=total_minutes)
    
    return estimated_time


def should_auto_cancel_order(order_status: OrderStatus, created_at: datetime, timeout_minutes: int = 10) -> bool:
    """
    Check if order should be auto-cancelled due to timeout.
    
    Args:
        order_status: Current order status
        created_at: Order creation timestamp
        timeout_minutes: Timeout in minutes (default 10)
    
    Returns:
        True if order should be auto-cancelled
    """
    # Only auto-cancel pending orders
    if order_status != OrderStatus.PENDING:
        return False
    
    # Check if timeout has elapsed
    time_since_creation = datetime.now(timezone.utc) - created_at
    return time_since_creation > timedelta(minutes=timeout_minutes)


# ============================================
# PAYMENT VALIDATIONS
# ============================================

def is_refund_eligible(
    payment_status: PaymentStatus,
    order_status: OrderStatus,
    payment_method: str
) -> Tuple[bool, Optional[str]]:
    """
    Check if order is eligible for refund.
    
    Args:
        payment_status: Current payment status
        order_status: Current order status
        payment_method: Payment method used
    
    Returns:
        Tuple of (is_eligible: bool, reason: Optional[str])
    """
    # Cannot refund if not paid
    if payment_status != PaymentStatus.PAID:
        return False, "Order payment is not completed"
    
    # Cannot refund if already refunded
    if payment_status == PaymentStatus.REFUNDED:
        return False, "Order is already refunded"
    
    # COD orders don't need refund
    if payment_method.lower() in ['cash', 'cod']:
        return False, "Cash on delivery orders do not require refund"
    
    # Can refund cancelled or failed orders
    if order_status in [OrderStatus.CANCELLED, OrderStatus.REFUNDED]:
        return True, None
    
    return False, "Order is not in a refundable state"


# ============================================
# BUSINESS LOGIC HELPERS
# ============================================

def calculate_delivery_partner_earnings(
    delivery_fee: Decimal,
    distance_km: float,
    commission_rate: Decimal = Decimal('0.20')
) -> Decimal:
    """
    Calculate delivery partner earnings.
    
    Args:
        delivery_fee: Total delivery fee
        distance_km: Distance covered
        commission_rate: Platform commission rate (default 20%)
    
    Returns:
        Delivery partner earnings
    """
    # Delivery partner gets delivery fee minus platform commission
    platform_commission = delivery_fee * commission_rate
    partner_earnings = delivery_fee - platform_commission
    
    # Add distance bonus (₹2 per km over 5 km)
    if distance_km > 5:
        distance_bonus = Decimal(str((distance_km - 5) * 2))
        partner_earnings += distance_bonus
    
    return partner_earnings.quantize(Decimal('0.01'))


def get_order_timeout_minutes(order_status: OrderStatus) -> int:
    """
    Get timeout minutes for different order statuses.
    
    Args:
        order_status: Current order status
    
    Returns:
        Timeout in minutes
    """
    timeout_map = {
        OrderStatus.PENDING: 10,  # Restaurant must accept within 10 minutes
        OrderStatus.CONFIRMED: 60,  # Must start preparing within 1 hour
        OrderStatus.PREPARING: 120,  # Must be ready within 2 hours
        OrderStatus.READY_FOR_PICKUP: 30,  # Must be picked up within 30 minutes
        OrderStatus.PICKED_UP: 60,  # Must deliver within 1 hour
    }
    
    return timeout_map.get(order_status, 0)
