"""
Pricing service layer for OneQlick food delivery platform.
Handles dynamic pricing configuration from database.
"""

from sqlalchemy.orm import Session
from decimal import Decimal
from typing import Dict, Optional
from app.infra.db.postgres.models.pricing_config import PricingConfig
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class PricingService:
    """Service for managing pricing configuration"""
    
    @staticmethod
    def get_config(db: Session) -> Dict[str, Decimal]:
        """Get all active pricing configuration"""
        configs = db.query(PricingConfig).filter(
            PricingConfig.is_active == True
        ).all()
        
        return {
            config.config_key: Decimal(str(config.config_value))
            for config in configs
        }
    
    @staticmethod
    def get_config_value(db: Session, key: str, default: Optional[Decimal] = None) -> Decimal:
        """Get specific pricing configuration value"""
        config = db.query(PricingConfig).filter(
            PricingConfig.config_key == key,
            PricingConfig.is_active == True
        ).first()
        
        if not config:
            if default is not None:
                return default
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pricing config '{key}' not found"
            )
        
        return Decimal(str(config.config_value))
    
    @staticmethod
    def update_config(db: Session, key: str, value: Decimal) -> PricingConfig:
        """Update pricing configuration"""
        config = db.query(PricingConfig).filter(
            PricingConfig.config_key == key
        ).first()
        
        if not config:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pricing config '{key}' not found"
            )
        
        config.config_value = value
        db.commit()
        db.refresh(config)
        
        logger.info(f"Updated pricing config: {key} = {value}")
        return config
    
    @staticmethod
    def calculate_platform_fee(db: Session, subtotal: Decimal) -> Decimal:
        """Calculate platform fee based on configuration"""
        fee_type = PricingService.get_config_value(db, 'platform_fee_type', Decimal('1'))  # 1 = fixed
        fee_value = PricingService.get_config_value(db, 'platform_fee_value', Decimal('5.00'))
        
        if fee_type == Decimal('0'):  # Percentage
            return (subtotal * fee_value / Decimal('100')).quantize(Decimal('0.01'))
        else:  # Fixed
            return fee_value
    
    @staticmethod
    def calculate_delivery_fee(db: Session, distance_km: float, subtotal: Decimal) -> Decimal:
        """Calculate delivery fee based on configuration"""
        # Check free delivery threshold
        free_delivery_threshold = PricingService.get_config_value(
            db, 'free_delivery_threshold', Decimal('199.00')
        )
        
        if subtotal >= free_delivery_threshold:
            return Decimal('0.00')
        
        # Calculate distance-based fee
        base_fee = PricingService.get_config_value(db, 'delivery_base_fee', Decimal('20.00'))
        
        if distance_km <= 2:
            return base_fee
        elif distance_km <= 5:
            rate = PricingService.get_config_value(db, 'delivery_fee_2_5km', Decimal('5.00'))
            additional = Decimal(str((distance_km - 2) * float(rate)))
            return base_fee + additional
        elif distance_km <= 10:
            rate = PricingService.get_config_value(db, 'delivery_fee_5_10km', Decimal('8.00'))
            rate_2_5 = PricingService.get_config_value(db, 'delivery_fee_2_5km', Decimal('5.00'))
            base_2_5 = Decimal(str(3 * float(rate_2_5)))
            additional = Decimal(str((distance_km - 5) * float(rate)))
            return base_fee + base_2_5 + additional
        else:
            rate = PricingService.get_config_value(db, 'delivery_fee_10plus_km', Decimal('10.00'))
            rate_2_5 = PricingService.get_config_value(db, 'delivery_fee_2_5km', Decimal('5.00'))
            rate_5_10 = PricingService.get_config_value(db, 'delivery_fee_5_10km', Decimal('8.00'))
            base_2_5 = Decimal(str(3 * float(rate_2_5)))
            base_5_10 = Decimal(str(5 * float(rate_5_10)))
            additional = Decimal(str((distance_km - 10) * float(rate)))
            return base_fee + base_2_5 + base_5_10 + additional
    
    @staticmethod
    def calculate_tax(db: Session, subtotal: Decimal) -> Decimal:
        """Calculate tax based on configuration"""
        tax_rate = PricingService.get_config_value(db, 'tax_rate', Decimal('5.00'))
        return (subtotal * tax_rate / Decimal('100')).quantize(Decimal('0.01'))
