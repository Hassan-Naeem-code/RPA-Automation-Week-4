"""Test configuration and fixtures for flight automation system."""

import pytest
import tempfile
import shutil
import os
from pathlib import Path
from unittest.mock import Mock, patch
import pandas as pd

# Test data fixtures
@pytest.fixture
def sample_reservation_data():
    """Sample reservation data for testing."""
    return pd.DataFrame({
        'reservation_id': ['RES001', 'RES002', 'RES003'],
        'passenger_name': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'flight_number': ['AA123', 'BA456', 'UA789'],
        'departure_date': ['2024-12-01', '2024-12-02', '2024-12-03'],
        'departure_airport': ['JFK', 'LAX', 'ORD'],
        'arrival_airport': ['LAX', 'JFK', 'DFW'],
        'email': ['john@example.com', 'jane@example.com', 'bob@example.com'],
        'status': ['confirmed', 'pending', 'confirmed']
    })

@pytest.fixture
def temp_config_dir():
    """Temporary configuration directory for testing."""
    temp_dir = tempfile.mkdtemp()
    config_dir = Path(temp_dir) / 'config'
    config_dir.mkdir()
    
    # Create test config files
    settings_config = {
        'data': {
            'input_file': str(Path(temp_dir) / 'test_data.csv'),
            'output_dir': str(Path(temp_dir) / 'reports')
        },
        'email': {
            'smtp_server': 'test.smtp.com',
            'smtp_port': 587,
            'sender_email': 'test@example.com',
            'sender_password': 'test_password'
        },
        'performance': {
            'enable_optimization': True,
            'batch_size': 100,
            'max_workers': 2
        }
    }
    
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def mock_email_service():
    """Mock email service for testing."""
    with patch('flight_automation.services.email_service.EmailService') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def mock_logger():
    """Mock logger for testing."""
    with patch('flight_automation.utils.logger.LoggerManager') as mock:
        mock_instance = Mock()
        mock.return_value = mock_instance
        yield mock_instance
