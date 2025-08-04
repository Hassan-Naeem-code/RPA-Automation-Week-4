"""
Flight Automation System - Production Ready Package

A comprehensive flight booking automation system with performance optimization,
robust error handling, and enterprise-grade features.

Features:
- High-performance data processing with vectorization
- Concurrent processing capabilities
- Comprehensive logging and monitoring
- Robust error handling and validation
- Email notification system
- Detailed reporting and analytics
"""

__version__ = "1.0.0"
__author__ = "Flight Automation Team"
__email__ = "automation@company.com"
__license__ = "MIT"

from flight_automation.core.data_processor import DataProcessor
from flight_automation.core.validation import DataValidator
from flight_automation.services.email_service import EmailService
from flight_automation.services.reporting import ReportGenerator
from flight_automation.utils.logger import LoggerManager
from flight_automation.utils.metrics import PerformanceMonitor

__all__ = [
    'DataProcessor',
    'DataValidator', 
    'EmailService',
    'ReportGenerator',
    'LoggerManager',
    'PerformanceMonitor',
    '__version__',
    '__author__',
    '__email__',
    '__license__'
]
