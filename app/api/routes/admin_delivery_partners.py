from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func, cast, String
from typing import Optional
from uuid import UUID

from app.infra.db.postgres.postgres_config import get_db
from app.api.dependencies import get_current_user
from app.infra.db.postgres.models.user import User
from app.infra.db.postgres.models.delivery_partner import DeliveryPartner
from app.infra.db.postgres.models.address import Address
from app.api.schemas.admin_delivery_partner_schemas import (
    DeliveryPartnerAdminResponse,
    DeliveryPartnerAdminListResponse,
    DeliveryPartnerAdminUpdateRequest
)
from app.api.schemas.common_schemas import CommonResponse
from app.utils.enums import UserRole

router = APIRouter()

def check_admin_access(current_user: User):
    """Helper to ensure only admins can access these endpoints"""
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this endpoint"
        )

def format_partner_response(partner: DeliveryPartner, user: User, address: Optional[Address]) -> dict:
    address_str = None
    if address:
        parts = [address.address_line1, address.address_line2, address.city, address.state, address.postal_code]
        address_str = ", ".join([p for p in parts if p])

    return {
        "delivery_partner_id": partner.delivery_partner_id,
        "user_id": user.user_id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "phone": user.phone,
        "profile_image": user.profile_image,
        "vehicle_type": partner.vehicle_type,
        "vehicle_number": partner.vehicle_number,
        "license_number": partner.license_number,
        "availability_status": partner.availability_status,
        "status": user.status,
        "total_deliveries": partner.total_deliveries,
        "rating": float(partner.rating) if partner.rating is not None else None,
        "address": address_str,
        "created_at": partner.created_at
    }


@router.get("/", response_model=CommonResponse[DeliveryPartnerAdminListResponse])
def get_all_delivery_partners(
    search: Optional[str] = Query(None, description="Search by name, bike number plate, or location"),
    availability: Optional[str] = Query(None, description="Filter by availability: 'available', 'busy', or 'offline'"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all delivery partners with search and filtering"""
    check_admin_access(current_user)

    query = db.query(DeliveryPartner, User, Address).join(
        User, DeliveryPartner.user_id == User.user_id
    ).outerjoin(
        Address, Address.user_id == User.user_id
    )

    if availability:
        query = query.filter(DeliveryPartner.availability_status == availability)

    if search:
        search_term = f"%{search.lower()}%"
        query = query.filter(
            or_(
                func.lower(User.first_name).ilike(search_term),
                func.lower(User.last_name).ilike(search_term),
                func.lower(DeliveryPartner.vehicle_number).ilike(search_term),
                cast(DeliveryPartner.vehicle_type, String).ilike(search_term),
                func.lower(Address.city).ilike(search_term),
                func.lower(Address.address_line1).ilike(search_term),
                func.lower(Address.address_line2).ilike(search_term),
                func.lower(Address.state).ilike(search_term),
            )
        )

    total_count = query.group_by(DeliveryPartner.delivery_partner_id, User.user_id, Address.address_id).count()

    results = query.offset(skip).limit(limit).all()

    formatted_partners = [
        format_partner_response(partner, user, address)
        for partner, user, address in results
    ]

    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Delivery partners fetched successfully",
        message_id="DELIVERY_PARTNERS_GET_SUCCESS",
        data=DeliveryPartnerAdminListResponse(
            delivery_partners=formatted_partners,
            total_count=total_count
        )
    )


@router.get("/{delivery_partner_id}", response_model=CommonResponse[DeliveryPartnerAdminResponse])
def get_delivery_partner_by_id(
    delivery_partner_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get details of a specific delivery partner by ID"""
    check_admin_access(current_user)

    result = db.query(DeliveryPartner, User, Address).join(
        User, DeliveryPartner.user_id == User.user_id
    ).outerjoin(
        Address, Address.user_id == User.user_id
    ).filter(
        DeliveryPartner.delivery_partner_id == delivery_partner_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Delivery partner not found")

    partner, user, address = result
    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Delivery partner details fetched successfully",
        message_id="DELIVERY_PARTNER_GET_SUCCESS",
        data=DeliveryPartnerAdminResponse(**format_partner_response(partner, user, address))
    )


@router.put("/{delivery_partner_id}", response_model=CommonResponse[DeliveryPartnerAdminResponse])
def update_delivery_partner(
    delivery_partner_id: UUID,
    update_data: DeliveryPartnerAdminUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a delivery partner's profile information"""
    check_admin_access(current_user)

    # Fetch the partner and user
    result = db.query(DeliveryPartner, User, Address).join(
        User, DeliveryPartner.user_id == User.user_id
    ).outerjoin(
        Address, Address.user_id == User.user_id
    ).filter(
        DeliveryPartner.delivery_partner_id == delivery_partner_id
    ).first()

    if not result:
        raise HTTPException(status_code=404, detail="Delivery partner not found")

    partner, user, address = result

    # Update User fields if provided
    if update_data.first_name is not None:
        user.first_name = update_data.first_name
    if update_data.last_name is not None:
        user.last_name = update_data.last_name
    if update_data.phone is not None:
        user.phone = update_data.phone

    # Update Delivery Partner fields if provided
    if update_data.vehicle_type is not None:
        partner.vehicle_type = update_data.vehicle_type
    if update_data.vehicle_number is not None:
        partner.vehicle_number = update_data.vehicle_number
    if update_data.license_number is not None:
        partner.license_number = update_data.license_number
    if update_data.availability_status is not None:
        partner.availability_status = update_data.availability_status

    db.commit()
    db.refresh(partner)
    db.refresh(user)

    return CommonResponse(
        code=status.HTTP_200_OK,
        message="Delivery partner updated successfully",
        message_id="DELIVERY_PARTNER_UPDATE_SUCCESS",
        data=DeliveryPartnerAdminResponse(**format_partner_response(partner, user, address))
    )
