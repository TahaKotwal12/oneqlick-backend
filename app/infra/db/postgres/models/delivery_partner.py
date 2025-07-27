from sqlalchemy import Column, String, Boolean, DECIMAL, Integer, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..base import Base
import enum

class VehicleType(str, enum.Enum):
    bicycle = 'bicycle'
    motorcycle = 'motorcycle'
    car = 'car'

class AvailabilityStatus(str, enum.Enum):
    available = 'available'
    busy = 'busy'
    offline = 'offline'

class DeliveryPartner(Base):
    __tablename__ = 'core_mstr_one_qlick_delivery_partners_tbl'

    delivery_partner_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('core_mstr_one_qlick_users_tbl.user_id', ondelete='CASCADE'))
    vehicle_type = Column(Enum(VehicleType), nullable=False)
    vehicle_number = Column(String(50), nullable=False)
    license_number = Column(String(50), nullable=False)
    current_latitude = Column(DECIMAL(10, 8))
    current_longitude = Column(DECIMAL(11, 8))
    availability_status = Column(Enum(AvailabilityStatus), default=AvailabilityStatus.offline)
    rating = Column(DECIMAL(3, 2), default=0)
    total_ratings = Column(Integer, default=0)
    total_deliveries = Column(Integer, default=0)
    documents_json = Column(String)  # JSONB, but use String for now
    is_verified = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False) 