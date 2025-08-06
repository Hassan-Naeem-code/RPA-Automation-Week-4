"""
Steel Industry Data Validation Module

This module provides comprehensive validation for steel production orders,
specifications, quality control, and business rules.

Features:
- Steel grade and type validation
- Dimensional validation for steel products
- Production line and warehouse validation
- Customer information validation
- Date and pricing validation
- Quality control standards validation
"""

import pandas as pd
import numpy as np
import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime, timedelta

class SteelDataValidator:
    """
    Comprehensive validator for steel industry data with detailed error reporting
    and quality control standards compliance.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Steel Data Validator
        
        Args:
            config: Configuration dictionary with validation parameters
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Steel industry validation constants
        self.valid_steel_grades = [
            'A36', 'A572-50', 'A992', 'A514', 'A588', 'A242', 'A709-50',
            'S355', 'S275', 'S235', 'S420', 'S460', 'Q235', 'Q345',
            '304SS', '316SS', '409SS', '430SS', '201SS'
        ]
        
        self.valid_steel_types = [
            'Hot Rolled', 'Cold Rolled', 'Galvanized', 'Stainless Steel',
            'Carbon Steel', 'Alloy Steel', 'Tool Steel', 'Spring Steel'
        ]
        
        self.valid_production_lines = [
            'Line-A1', 'Line-A2', 'Line-B1', 'Line-B2', 'Line-C1', 'Line-C2',
            'Line-D1', 'Line-D2', 'Line-E1', 'Line-E2'
        ]
        
        self.valid_statuses = [
            'Pending', 'In Production', 'Quality Check', 'Ready', 'Shipped',
            'Delivered', 'Cancelled', 'Hold', 'Rework Required'
        ]
        
        self.valid_warehouses = [
            'WH-North', 'WH-South', 'WH-East', 'WH-West', 'WH-Central',
            'WH-Export', 'WH-Domestic', 'WH-Reserve'
        ]
        
        self.valid_quality_grades = ['A', 'B', 'C', 'Reject', 'Rework']
        
        # Tracking
        self.validation_errors = []
        self.validation_stats = {
            'total_records_validated': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'error_categories': {}
        }
    
    def validate_order_id(self, order_id: str) -> Tuple[bool, str]:
        """
        Validate steel order ID format (SO-YYYY-NNNN)
        
        Args:
            order_id: Order ID string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if pd.isna(order_id) or not isinstance(order_id, str):
            return False, "Order ID is missing or not a string"
        
        # Check format: SO-YYYY-NNNN
        pattern = r'^SO-\d{4}-\d{4}$'
        if not re.match(pattern, order_id):
            return False, f"Invalid Order ID format: {order_id}. Expected: SO-YYYY-NNNN"
        
        return True, ""
    
    def validate_batch_id(self, batch_id: str) -> Tuple[bool, str]:
        """
        Validate batch ID format (B-NNNNNN)
        
        Args:
            batch_id: Batch ID string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if pd.isna(batch_id) or not isinstance(batch_id, str):
            return False, "Batch ID is missing or not a string"
        
        # Check format: B-NNNNNN
        pattern = r'^B-\d{6}$'
        if not re.match(pattern, batch_id):
            return False, f"Invalid Batch ID format: {batch_id}. Expected: B-NNNNNN"
        
        return True, ""
    
    def validate_steel_specifications(self, grade: str, steel_type: str) -> Tuple[bool, str]:
        """
        Validate steel grade and type combinations
        
        Args:
            grade: Steel grade
            steel_type: Steel type
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        if pd.isna(grade) or grade not in self.valid_steel_grades:
            errors.append(f"Invalid steel grade: {grade}")
        
        if pd.isna(steel_type) or steel_type not in self.valid_steel_types:
            errors.append(f"Invalid steel type: {steel_type}")
        
        # Check grade-type compatibility
        if grade and steel_type:
            # Stainless steel grades should match stainless steel type
            if grade.endswith('SS') and steel_type != 'Stainless Steel':
                errors.append(f"Steel grade {grade} should be Stainless Steel type, not {steel_type}")
            
            # Carbon steel grades should not be stainless
            if grade in ['A36', 'A572-50', 'A992'] and steel_type == 'Stainless Steel':
                errors.append(f"Carbon steel grade {grade} cannot be Stainless Steel type")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_dimensions(self, thickness: float, width: float, length: float, weight: float) -> Tuple[bool, str]:
        """
        Validate steel dimensions and weight for physical feasibility
        
        Args:
            thickness: Steel thickness in mm
            width: Steel width in mm
            length: Steel length in mm
            weight: Steel weight in kg
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        try:
            # Validate thickness
            if pd.isna(thickness) or thickness <= 0:
                errors.append("Thickness must be positive")
            elif not (0.1 <= thickness <= 300):
                errors.append(f"Thickness {thickness}mm outside valid range (0.1-300mm)")
            
            # Validate width
            if pd.isna(width) or width <= 0:
                errors.append("Width must be positive")
            elif not (100 <= width <= 5000):
                errors.append(f"Width {width}mm outside valid range (100-5000mm)")
            
            # Validate length
            if pd.isna(length) or length <= 0:
                errors.append("Length must be positive")
            elif not (6000 <= length <= 25000):
                errors.append(f"Length {length}mm outside valid range (6000-25000mm)")
            
            # Validate weight
            if pd.isna(weight) or weight <= 0:
                errors.append("Weight must be positive")
            elif weight > 50000:  # 50 tons maximum
                errors.append(f"Weight {weight}kg exceeds maximum (50,000kg)")
            
            # Cross-validate calculated vs actual weight (within 10% tolerance)
            if all(not pd.isna(x) and x > 0 for x in [thickness, width, length, weight]):
                calculated_weight = (thickness/1000) * (width/1000) * (length/1000) * 7850
                weight_diff = abs(weight - calculated_weight) / calculated_weight
                if weight_diff > 0.10:  # More than 10% difference
                    errors.append(f"Weight {weight}kg differs significantly from calculated {calculated_weight:.1f}kg")
            
        except (TypeError, ValueError):
            errors.append("Invalid dimension data types")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_pricing(self, unit_price: float, total_price: float, weight: float) -> Tuple[bool, str]:
        """
        Validate pricing information
        
        Args:
            unit_price: Unit price per ton
            total_price: Total order price
            weight: Steel weight in kg
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        try:
            # Validate unit price
            if pd.isna(unit_price) or unit_price <= 0:
                errors.append("Unit price must be positive")
            elif unit_price > 10000:  # $10,000/ton maximum
                errors.append(f"Unit price ${unit_price}/ton exceeds maximum ($10,000/ton)")
            
            # Validate total price
            if pd.isna(total_price) or total_price <= 0:
                errors.append("Total price must be positive")
            elif total_price > 1000000:  # $1M maximum order
                errors.append(f"Total price ${total_price} exceeds maximum ($1,000,000)")
            
            # Cross-validate pricing calculation (within 5% tolerance)
            if all(not pd.isna(x) and x > 0 for x in [unit_price, total_price, weight]):
                calculated_total = (weight / 1000) * unit_price  # Convert kg to tons
                price_diff = abs(total_price - calculated_total) / calculated_total
                if price_diff > 0.05:  # More than 5% difference
                    errors.append(f"Total price ${total_price} differs from calculated ${calculated_total:.2f}")
            
        except (TypeError, ValueError):
            errors.append("Invalid pricing data types")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_production_info(self, production_line: str, warehouse: str, quality_grade: str, status: str) -> Tuple[bool, str]:
        """
        Validate production and logistics information
        
        Args:
            production_line: Production line identifier
            warehouse: Warehouse location
            quality_grade: Quality control grade
            status: Order status
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        if pd.isna(production_line) or production_line not in self.valid_production_lines:
            errors.append(f"Invalid production line: {production_line}")
        
        if pd.isna(warehouse) or warehouse not in self.valid_warehouses:
            errors.append(f"Invalid warehouse: {warehouse}")
        
        if pd.isna(quality_grade) or quality_grade not in self.valid_quality_grades:
            errors.append(f"Invalid quality grade: {quality_grade}")
        
        if pd.isna(status) or status not in self.valid_statuses:
            errors.append(f"Invalid status: {status}")
        
        # Business rule validations
        if quality_grade == 'Reject' and status not in ['Cancelled', 'Rework Required']:
            errors.append("Rejected quality items must be Cancelled or require Rework")
        
        if status == 'Shipped' and quality_grade in ['Reject', 'Rework']:
            errors.append("Cannot ship rejected or rework items")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_dates(self, order_date: str, production_date: str, delivery_date: str) -> Tuple[bool, str]:
        """
        Validate date sequences and business logic
        
        Args:
            order_date: Order placement date
            production_date: Production start date
            delivery_date: Expected delivery date
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        try:
            # Parse dates
            order_dt = pd.to_datetime(order_date)
            production_dt = pd.to_datetime(production_date)
            delivery_dt = pd.to_datetime(delivery_date)
            
            # Check date sequence
            if production_dt < order_dt:
                errors.append("Production date cannot be before order date")
            
            if delivery_dt < production_dt:
                errors.append("Delivery date cannot be before production date")
            
            # Check for reasonable lead times
            if (production_dt - order_dt).days > 30:
                errors.append("Production lead time exceeds 30 days")
            
            if (delivery_dt - production_dt).days > 60:
                errors.append("Delivery lead time exceeds 60 days")
            
            # Check for future dates beyond reasonable range
            future_limit = datetime.now() + timedelta(days=365)
            if delivery_dt > future_limit:
                errors.append("Delivery date too far in future (>1 year)")
            
        except (ValueError, TypeError):
            errors.append("Invalid date format")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_contact_info(self, email: str, phone: str) -> Tuple[bool, str]:
        """
        Validate customer contact information
        
        Args:
            email: Customer email address
            phone: Customer phone number
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        errors = []
        
        # Validate email with basic regex
        if pd.isna(email) or email == '':
            errors.append("Email address is required")
        else:
            # Basic email validation
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, email):
                errors.append(f"Invalid email format: {email}")
        
        # Validate phone (allow missing phone numbers)
        if not pd.isna(phone) and phone != '':
            # Basic phone validation (numbers, spaces, hyphens, parentheses, plus, x)
            phone_pattern = r'^[\d\s\-\(\)\+x\.]+$'
            if not re.match(phone_pattern, phone):
                errors.append(f"Invalid phone format: {phone}")
        
        if errors:
            return False, "; ".join(errors)
        return True, ""
    
    def validate_single_order(self, order: pd.Series) -> List[str]:
        """
        Validate a single steel order record
        
        Args:
            order: Pandas Series representing one order
            
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Order ID validation
        is_valid, error = self.validate_order_id(order.get('OrderID'))
        if not is_valid:
            errors.append(error)
        
        # Batch ID validation
        is_valid, error = self.validate_batch_id(order.get('BatchID'))
        if not is_valid:
            errors.append(error)
        
        # Steel specifications validation
        is_valid, error = self.validate_steel_specifications(
            order.get('SteelGrade'), order.get('SteelType')
        )
        if not is_valid:
            errors.append(error)
        
        # Dimensions validation
        is_valid, error = self.validate_dimensions(
            order.get('Thickness'), order.get('Width'), 
            order.get('Length'), order.get('Weight')
        )
        if not is_valid:
            errors.append(error)
        
        # Pricing validation
        is_valid, error = self.validate_pricing(
            order.get('UnitPrice'), order.get('TotalPrice'), order.get('Weight')
        )
        if not is_valid:
            errors.append(error)
        
        # Production info validation
        is_valid, error = self.validate_production_info(
            order.get('ProductionLine'), order.get('Warehouse'),
            order.get('QualityGrade'), order.get('Status')
        )
        if not is_valid:
            errors.append(error)
        
        # Dates validation
        is_valid, error = self.validate_dates(
            order.get('OrderDate'), order.get('ProductionDate'), order.get('DeliveryDate')
        )
        if not is_valid:
            errors.append(error)
        
        # Contact info validation
        is_valid, error = self.validate_contact_info(
            order.get('ContactEmail'), order.get('ContactPhone')
        )
        if not is_valid:
            errors.append(error)
        
        return errors
    
    def validate_steel_orders(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Validate all steel orders and return only valid records
        
        Args:
            data: DataFrame containing steel orders
            
        Returns:
            DataFrame containing only valid orders
        """
        self.logger.info(f"Starting validation of {len(data)} steel orders")
        
        valid_orders = []
        self.validation_errors = []
        
        for index, order in data.iterrows():
            errors = self.validate_single_order(order)
            
            if not errors:
                valid_orders.append(order)
                self.validation_stats['valid_records'] += 1
            else:
                # Log errors for this order
                order_id = order.get('OrderID', f'Row-{index}')
                for error in errors:
                    error_msg = f"Order {order_id}: {error}"
                    self.validation_errors.append(error_msg)
                    self.logger.warning(error_msg)
                
                self.validation_stats['invalid_records'] += 1
                
                # Categorize errors
                for error in errors:
                    category = error.split(':')[0] if ':' in error else 'General'
                    self.validation_stats['error_categories'][category] = \
                        self.validation_stats['error_categories'].get(category, 0) + 1
        
        self.validation_stats['total_records_validated'] = len(data)
        
        valid_df = pd.DataFrame(valid_orders)
        self.logger.info(f"Validation completed: {len(valid_df)} valid, "
                        f"{self.validation_stats['invalid_records']} invalid orders")
        
        return valid_df
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get summary of validation results
        
        Returns:
            Dictionary containing validation statistics
        """
        return {
            'validation_stats': self.validation_stats,
            'error_details': self.validation_errors[-20:],  # Last 20 errors
            'error_categories': self.validation_stats['error_categories']
        }
