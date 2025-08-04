"""
Data processing module for flight reservations.
Contains intentional bugs and performance issues.
"""

import pandas as pd
import numpy as np
import logging
import time

logger = logging.getLogger(__name__)

class DataProcessor:
    """Process flight reservation data with intentional bugs."""
    
    def __init__(self):
        self.valid_airports = [
            'LAX', 'JFK', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'LAS', 'MCO',
            'EWR', 'CLT', 'PHX', 'IAH', 'MIA', 'BOS', 'MSP', 'FLL', 'DTW', 'PHL',
            'LGA', 'BWI', 'MDW', 'TPA', 'IAD', 'SAN', 'HNL', 'PDX', 'STL', 'AUS'
        ]
        self.valid_statuses = ['Confirmed', 'Cancelled', 'Pending', 'Checked-in', 'Completed']
    
    def load_data(self, file_path):
        """
        Load flight reservation data from CSV.
        Bug: No file existence check or proper error handling.
        """
        logger.info(f"Loading data from {file_path}")
        
        # Bug 1: No file existence check
        data = pd.read_csv(file_path)
        
        # Bug 2: No data validation on load
        return data
    
    def process_reservations(self, data):
        """
        Process reservation data with multiple performance issues.
        Bug: Inefficient row-by-row processing instead of vectorized operations.
        """
        logger.info("Processing reservations (inefficient method)")
        processed_records = []
        
        # Bug 3: Inefficient row-by-row iteration
        for index, row in data.iterrows():
            try:
                processed_record = self._process_single_reservation(row)
                if processed_record:
                    processed_records.append(processed_record)
                    
                # Bug 4: Unnecessary sleep in loop (simulating slow processing)
                time.sleep(0.01)  # 10ms delay per record = 2+ seconds for 200 records
                
            except Exception as e:
                logger.error(f"Error processing record {index}: {str(e)}")
                # Bug 5: Continue processing without proper error tracking
                continue
        
        return pd.DataFrame(processed_records)
    
    def _process_single_reservation(self, row):
        """
        Process a single reservation record with data type issues.
        """
        # Fix: Handle string fare values properly
        fare = row['Fare']
        if isinstance(fare, str):
            try:
                # Remove currency symbols and convert to float
                fare = float(fare.replace('$', '').replace(',', ''))
            except ValueError:
                logger.warning(f"Invalid fare format for PNR {row['PNR']}: {fare}")
                fare = 0.0
        
        # Fix: Check for missing values and handle appropriately
        if pd.isna(fare):
            logger.warning(f"Missing fare value for PNR {row['PNR']}")
            fare = 0.0
        
        # Fix: Validate airport codes
        origin = row['Origin']
        destination = row['Destination']
        
        # Fix: Handle same origin/destination and invalid codes
        if origin == destination:
            logger.warning(f"Same origin and destination for PNR {row['PNR']} - skipping record")
            return None  # Skip this record
        
        if origin not in self.valid_airports or destination not in self.valid_airports:
            logger.warning(f"Invalid airport codes for PNR {row['PNR']}: {origin} -> {destination}")
            return None  # Skip this record
        
        # Fix: Validate status and skip invalid records
        status = row['Status']
        if status not in self.valid_statuses:
            logger.warning(f"Invalid status for PNR {row['PNR']}: {status}")
            return None  # Skip this record
        
        # Fix: Skip records with zero or negative fares
        if fare <= 0:
            logger.warning(f"Invalid fare amount for PNR {row['PNR']}: {fare}")
            return None  # Skip this record
        
        processed_record = {
            'PNR': row['PNR'],
            'Passenger': row['Passenger'],
            'Origin': origin,
            'Destination': destination,
            'Fare': fare,
            'Status': status,
            'BookingDate': row['BookingDate'],
            'TravelDate': row['TravelDate'],
            'Email': row['Email'],
            'Phone': row['Phone'],
            'ProcessedAt': pd.Timestamp.now(),
            'IsValid': True  # Fixed: Now only valid records reach this point
        }
        
        return processed_record
    
    def clean_data_optimized(self, data):
        """
        Optimized version of data cleaning using vectorized operations.
        This method will be implemented during optimization phase.
        """
        logger.info("Cleaning data using optimized vectorized operations")
        
        # Remove duplicates
        data_clean = data.drop_duplicates(subset=['PNR'], keep='first')
        
        # Handle fare data type issues vectorized
        def clean_fare(fare_value):
            if pd.isna(fare_value):
                return 0.0
            if isinstance(fare_value, str):
                # Remove $ symbol and convert to float
                try:
                    return float(fare_value.replace('$', ''))
                except:
                    return 0.0
            return float(fare_value)
        
        data_clean['Fare'] = data_clean['Fare'].apply(clean_fare)
        
        # Filter out invalid airport codes
        valid_airports = set(self.valid_airports)
        data_clean = data_clean[
            (data_clean['Origin'].isin(valid_airports)) & 
            (data_clean['Destination'].isin(valid_airports))
        ]
        
        # Remove records where origin equals destination
        data_clean = data_clean[data_clean['Origin'] != data_clean['Destination']]
        
        # Filter valid statuses
        data_clean = data_clean[data_clean['Status'].isin(self.valid_statuses)]
        
        # Remove records with negative or zero fares
        data_clean = data_clean[data_clean['Fare'] > 0]
        
        return data_clean
