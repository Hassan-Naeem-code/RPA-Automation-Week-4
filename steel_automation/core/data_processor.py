"""
Steel Industry Data Processing Module

This module handles the processing, cleaning, and optimization of steel production
and order data with advanced vectorization and performance optimizations.

Features:
- Steel order data validation and cleaning
- Production metrics calculation
- Inventory management processing
- Quality control data processing
- Performance-optimized operations
"""

import pandas as pd
import numpy as np
import time
import gc
import logging
from typing import Dict, List, Tuple, Optional, Any
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class SteelDataProcessor:
    """
    High-performance steel industry data processor with vectorized operations
    and comprehensive error handling.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Steel Data Processor
        
        Args:
            config: Configuration dictionary with processing parameters
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Steel industry specific constants
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
        
        # Performance tracking
        self.processing_stats = {
            'total_records_processed': 0,
            'valid_records': 0,
            'invalid_records': 0,
            'processing_time': 0,
            'errors_encountered': []
        }
    
    def clean_price_value(self, price_str: str) -> float:
        """
        Clean and convert price strings to float values
        
        Args:
            price_str: Price string (may contain $ symbol or be empty)
            
        Returns:
            Float value of the price, 0.0 if invalid
        """
        if pd.isna(price_str) or price_str == '' or price_str is None:
            return 0.0
            
        try:
            # Remove currency symbols and convert to float
            if isinstance(price_str, str):
                cleaned = price_str.replace('$', '').replace(',', '').strip()
                return float(cleaned)
            return float(price_str)
        except (ValueError, TypeError):
            self.logger.warning(f"Could not convert price '{price_str}' to float")
            return 0.0
    
    def validate_steel_dimensions(self, thickness: float, width: float, length: float) -> bool:
        """
        Validate steel dimensions for physical feasibility
        
        Args:
            thickness: Steel thickness in mm
            width: Steel width in mm  
            length: Steel length in mm
            
        Returns:
            True if dimensions are valid, False otherwise
        """
        try:
            # Check for reasonable ranges
            if not (0.1 <= thickness <= 300):  # 0.1mm to 300mm thickness
                return False
            if not (100 <= width <= 5000):     # 100mm to 5m width
                return False
            if not (6000 <= length <= 25000):  # 6m to 25m length
                return False
            return True
        except (TypeError, ValueError):
            return False
    
    def calculate_weight_from_dimensions(self, thickness: float, width: float, length: float) -> float:
        """
        Calculate steel weight from dimensions using standard steel density
        
        Args:
            thickness: Steel thickness in mm
            width: Steel width in mm
            length: Steel length in mm
            
        Returns:
            Calculated weight in kg
        """
        try:
            # Steel density: ~7.85 kg/m³
            volume_m3 = (thickness/1000) * (width/1000) * (length/1000)
            weight = volume_m3 * 7850  # kg
            return round(weight, 2)
        except (TypeError, ValueError):
            return 0.0
    
    def clean_data_optimized(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Optimized steel order data cleaning using vectorized operations
        
        Args:
            data: Raw steel order data DataFrame
            
        Returns:
            Cleaned and validated DataFrame
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting optimized cleaning of {len(data)} steel orders")
            
            # Create a copy to avoid modifying original data
            data_clean = data.copy()
            
            # 1. Remove exact duplicates based on OrderID
            initial_count = len(data_clean)
            data_clean = data_clean.drop_duplicates(subset=['OrderID'], keep='first')
            duplicates_removed = initial_count - len(data_clean)
            self.logger.info(f"Removed {duplicates_removed} duplicate orders")
            
            # 2. Vectorized price cleaning
            data_clean['TotalPrice'] = data_clean['TotalPrice'].apply(self.clean_price_value)
            data_clean['UnitPrice'] = data_clean['UnitPrice'].apply(self.clean_price_value)
            
            # 3. Vectorized data type corrections
            data_clean['Weight'] = pd.to_numeric(data_clean['Weight'], errors='coerce').fillna(0)
            data_clean['Thickness'] = pd.to_numeric(data_clean['Thickness'], errors='coerce').fillna(0)
            data_clean['Width'] = pd.to_numeric(data_clean['Width'], errors='coerce').fillna(0)
            data_clean['Length'] = pd.to_numeric(data_clean['Length'], errors='coerce').fillna(0)
            
            # 4. Vectorized filtering for valid steel specifications
            valid_mask = (
                data_clean['SteelGrade'].isin(self.valid_steel_grades) &
                data_clean['SteelType'].isin(self.valid_steel_types) &
                data_clean['ProductionLine'].isin(self.valid_production_lines) &
                data_clean['Status'].isin(self.valid_statuses) &
                data_clean['Warehouse'].isin(self.valid_warehouses) &
                (data_clean['TotalPrice'] > 0) &
                (data_clean['Weight'] > 0) &
                (data_clean['Thickness'] > 0) &
                (data_clean['Width'] > 0) &
                (data_clean['Length'] > 0)
            )
            
            # Apply filtering
            invalid_count = len(data_clean) - valid_mask.sum()
            data_clean = data_clean[valid_mask]
            
            # 5. Calculate derived metrics
            data_clean['ValuePerKg'] = data_clean['TotalPrice'] / data_clean['Weight']
            data_clean['Volume'] = (data_clean['Thickness'] * data_clean['Width'] * data_clean['Length']) / 1e9  # m³
            data_clean['Density'] = data_clean['Weight'] / data_clean['Volume']
            
            # 6. Add processing timestamp
            data_clean['ProcessedAt'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            processing_time = time.time() - start_time
            
            # Update statistics
            self.processing_stats.update({
                'total_records_processed': initial_count,
                'valid_records': len(data_clean),
                'invalid_records': invalid_count + duplicates_removed,
                'processing_time': processing_time
            })
            
            self.logger.info(f"Optimized cleaning completed in {processing_time:.2f}s")
            self.logger.info(f"Valid orders: {len(data_clean)}, Invalid: {invalid_count}")
            
            # Clean up memory
            del data
            gc.collect()
            
            return data_clean
            
        except Exception as e:
            self.logger.error(f"Error in optimized data cleaning: {str(e)}")
            self.processing_stats['errors_encountered'].append(str(e))
            raise
    
    def process_steel_orders(self, data_file: str) -> pd.DataFrame:
        """
        Main processing function for steel orders
        
        Args:
            data_file: Path to the steel orders CSV file
            
        Returns:
            Processed and cleaned DataFrame
        """
        try:
            self.logger.info(f"Loading steel orders from {data_file}")
            
            # Load data with optimized settings
            raw_data = pd.read_csv(data_file, low_memory=False)
            self.logger.info(f"Loaded {len(raw_data)} steel order records")
            
            # Process the data
            processed_data = self.clean_data_optimized(raw_data)
            
            self.logger.info("Steel order processing completed successfully")
            return processed_data
            
        except FileNotFoundError:
            error_msg = f"Steel orders file not found: {data_file}"
            self.logger.error(error_msg)
            raise FileNotFoundError(error_msg)
        except Exception as e:
            error_msg = f"Error processing steel orders: {str(e)}"
            self.logger.error(error_msg)
            raise
    
    def get_processing_summary(self) -> Dict[str, Any]:
        """
        Get summary of processing statistics
        
        Returns:
            Dictionary containing processing metrics
        """
        return {
            'processing_stats': self.processing_stats,
            'efficiency_metrics': {
                'records_per_second': self.processing_stats['valid_records'] / max(self.processing_stats['processing_time'], 0.001),
                'success_rate': self.processing_stats['valid_records'] / max(self.processing_stats['total_records_processed'], 1) * 100,
                'error_rate': len(self.processing_stats['errors_encountered']) / max(self.processing_stats['total_records_processed'], 1) * 100
            }
        }
