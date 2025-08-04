"""Unit tests for data processor module."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import tempfile
from pathlib import Path

# Import the module to test
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from flight_automation.core.data_processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sample_data = pd.DataFrame({
            'reservation_id': ['RES001', 'RES002', 'RES003', ''],
            'passenger_name': ['John Doe', 'Jane Smith', '', 'Bob Johnson'],
            'flight_number': ['AA123', 'BA456', 'UA789', 'DL321'],
            'departure_date': ['2024-12-01', '2024-12-02', '2024-12-03', '2024-12-04'],
            'departure_airport': ['JFK', 'LAX', 'ORD', 'ATL'],
            'arrival_airport': ['LAX', 'JFK', 'DFW', 'SEA'],
            'email': ['john@example.com', 'jane@example.com', 'bob@example.com', 'alice@example.com'],
            'status': ['confirmed', 'pending', 'confirmed', 'cancelled']
        })
        
        # Create temporary file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
        self.sample_data.to_csv(self.temp_file.name, index=False)
        self.temp_file.close()
        
        self.processor = DataProcessor()
    
    def tearDown(self):
        """Clean up test fixtures."""
        os.unlink(self.temp_file.name)
    
    def test_load_data_success(self):
        """Test successful data loading."""
        result = self.processor.load_data(self.temp_file.name)
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 4)
    
    def test_load_data_file_not_found(self):
        """Test data loading with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.processor.load_data('non_existent_file.csv')
    
    def test_clean_data(self):
        """Test data cleaning functionality."""
        cleaned_data = self.processor.clean_data(self.sample_data)
        
        # Should remove rows with empty reservation_id
        self.assertEqual(len(cleaned_data), 3)
        
        # Should fill empty passenger names
        self.assertFalse(cleaned_data['passenger_name'].isna().any())
    
    def test_validate_data_structure(self):
        """Test data structure validation."""
        # Valid data should pass
        is_valid, errors = self.processor.validate_data_structure(self.sample_data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Invalid data should fail
        invalid_data = pd.DataFrame({'wrong_column': [1, 2, 3]})
        is_valid, errors = self.processor.validate_data_structure(invalid_data)
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_process_reservations(self):
        """Test reservation processing."""
        processed = self.processor.process_reservations(self.sample_data)
        
        self.assertIsInstance(processed, pd.DataFrame)
        self.assertIn('processed_at', processed.columns)
        self.assertIn('validation_status', processed.columns)
    
    def test_batch_processing(self):
        """Test batch processing functionality."""
        # Create larger dataset
        large_data = pd.concat([self.sample_data] * 100, ignore_index=True)
        
        batches = list(self.processor.process_in_batches(large_data, batch_size=50))
        self.assertEqual(len(batches), 8)  # 400 rows / 50 = 8 batches
    
    @patch('flight_automation.core.data_processor.pd.read_csv')
    def test_load_data_with_encoding_issues(self, mock_read_csv):
        """Test data loading with encoding issues."""
        # Simulate encoding error on first attempt
        mock_read_csv.side_effect = [
            UnicodeDecodeError('utf-8', b'', 0, 1, 'invalid start byte'),
            self.sample_data
        ]
        
        result = self.processor.load_data('test_file.csv')
        self.assertIsInstance(result, pd.DataFrame)
        
        # Should have tried both utf-8 and latin-1 encodings
        self.assertEqual(mock_read_csv.call_count, 2)


if __name__ == '__main__':
    unittest.main()
