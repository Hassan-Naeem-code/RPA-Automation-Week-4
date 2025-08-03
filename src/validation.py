"""
Data validation module for flight reservations.
Contains validation logic with some intentional gaps.
"""

import pandas as pd
import numpy as np
import logging
import re

logger = logging.getLogger(__name__)

class DataValidator:
    """Validate flight reservation data with some intentional issues."""
    
    def __init__(self):
        self.valid_airports = [
            'LAX', 'JFK', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'LAS', 'MCO',
            'EWR', 'CLT', 'PHX', 'IAH', 'MIA', 'BOS', 'MSP', 'FLL', 'DTW', 'PHL',
            'LGA', 'BWI', 'MDW', 'TPA', 'IAD', 'SAN', 'HNL', 'PDX', 'STL', 'AUS'
        ]
        self.valid_statuses = ['Confirmed', 'Cancelled', 'Pending', 'Checked-in', 'Completed']
        self.validation_errors = []
    
    def validate_reservations(self, data):
        """
        Validate reservation data with incomplete validation logic.
        Bug: Missing comprehensive validation checks.
        """
        logger.info(f"Validating {len(data)} reservations")
        self.validation_errors = []
        
        valid_records = []
        
        for index, row in data.iterrows():
            errors = self._validate_single_record(row, index)
            
            if errors:
                self.validation_errors.extend(errors)
                # Fix: Skip invalid records instead of including them
                logger.debug(f"Skipping invalid record at index {index} due to {len(errors)} errors")
            else:
                valid_records.append(row)
        
        logger.info(f"Found {len(self.validation_errors)} validation errors")
        logger.info(f"Filtered dataset: {len(valid_records)} valid records out of {len(data)} total")
        
        return pd.DataFrame(valid_records)
    
    def _validate_single_record(self, row, index):
        """Validate a single reservation record."""
        errors = []
        
        # Validate PNR format
        if not self._validate_pnr(row.get('PNR')):
            errors.append({
                'row': index,
                'field': 'PNR',
                'value': row.get('PNR'),
                'error': 'Invalid PNR format'
            })
        
        # Validate passenger name
        if not self._validate_passenger_name(row.get('Passenger')):
            errors.append({
                'row': index,
                'field': 'Passenger',
                'value': row.get('Passenger'),
                'error': 'Invalid passenger name'
            })
        
        # Validate airport codes
        if not self._validate_airport_code(row.get('Origin')):
            errors.append({
                'row': index,
                'field': 'Origin',
                'value': row.get('Origin'),
                'error': 'Invalid origin airport code'
            })
        
        if not self._validate_airport_code(row.get('Destination')):
            errors.append({
                'row': index,
                'field': 'Destination',
                'value': row.get('Destination'),
                'error': 'Invalid destination airport code'
            })
        
        # Fix: Check if origin equals destination
        if row.get('Origin') == row.get('Destination'):
            errors.append({
                'row': index,
                'field': 'Origin/Destination',
                'value': f"{row.get('Origin')} -> {row.get('Destination')}",
                'error': 'Origin and destination cannot be the same'
            })
        
        # Validate fare
        if not self._validate_fare(row.get('Fare')):
            errors.append({
                'row': index,
                'field': 'Fare',
                'value': row.get('Fare'),
                'error': 'Invalid fare amount'
            })
        
        # Validate status
        if not self._validate_status(row.get('Status')):
            errors.append({
                'row': index,
                'field': 'Status',
                'value': row.get('Status'),
                'error': 'Invalid status value'
            })
        
        # Fix: Add email validation that was missing
        if not self._validate_email(row.get('Email')):
            errors.append({
                'row': index,
                'field': 'Email',
                'value': row.get('Email'),
                'error': 'Invalid email format'
            })
        
        # Bug 4: Not validating required fields for null values
        required_fields = ['PNR', 'Passenger', 'Origin', 'Destination', 'Status']
        for field in required_fields:
            if pd.isna(row.get(field)) or row.get(field) == '':
                errors.append({
                    'row': index,
                    'field': field,
                    'value': row.get(field),
                    'error': 'Required field is missing'
                })
        
        return errors
    
    def _validate_pnr(self, pnr):
        """Validate PNR format (should be 6 alphanumeric characters)."""
        if pd.isna(pnr):
            return False
        return bool(re.match(r'^[A-Z0-9]{6}$', str(pnr)))
    
    def _validate_passenger_name(self, name):
        """Validate passenger name."""
        if pd.isna(name):
            return False
        return len(str(name).strip()) >= 2
    
    def _validate_airport_code(self, code):
        """Validate airport code."""
        if pd.isna(code):
            return False
        return str(code) in self.valid_airports
    
    def _validate_fare(self, fare):
        """
        Validate fare amount.
        Fix: Handle string fare values properly.
        """
        if pd.isna(fare):
            return False
        
        try:
            # Fix: Handle string values like "$2097.46"
            if isinstance(fare, str):
                fare_value = float(fare.replace('$', '').replace(',', ''))
            else:
                fare_value = float(fare)
            return fare_value > 0
        except (ValueError, TypeError):
            # Fix: Still return False for invalid formats, but after trying to clean
            return False
    
    def _validate_status(self, status):
        """Validate status value."""
        if pd.isna(status):
            return False
        return str(status) in self.valid_statuses
    
    def _validate_email(self, email):
        """
        Validate email format - THIS METHOD IS NOT BEING CALLED!
        Bug: Email validation exists but is never used.
        """
        if pd.isna(email):
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, str(email)))
    
    def get_validation_summary(self):
        """Get summary of validation errors."""
        if not self.validation_errors:
            return "No validation errors found"
        
        error_summary = {}
        for error in self.validation_errors:
            field = error['field']
            error_type = error['error']
            key = f"{field}: {error_type}"
            error_summary[key] = error_summary.get(key, 0) + 1
        
        return error_summary
