"""
Steel Industry Automation System - Production Ready Package

A comprehensive steel production automation system with performance optimization,
robust error handling, and enterprise-grade features.

Features:
- High-performance steel order processing with vectorization
- Concurrent processing capabilities
- Comprehensive logging and monitoring
- Robust error handling and validation
- Customer notification system
- Detailed reporting and analytics
"""

__version__ = "1.0.0"
__author__ = "Steel Automation Team"
__email__ = "automation@steelcorp.com"
__license__ = "MIT"

from steel_automation.core.data_processor import SteelDataProcessor
from steel_automation.core.validation import SteelDataValidator
from steel_automation.services.email_service import EmailService
from steel_automation.services.reporting import ReportGenerator
from steel_automation.utils.logger import LoggerManager
from steel_automation.utils.metrics import PerformanceMonitor

__all__ = [
    'SteelDataProcessor',
    'SteelDataValidator', 
    'EmailService',
    'ReportGenerator',
    'LoggerManager',
    'PerformanceMonitor',
    '__version__',
    '__author__',
    '__email__',
    '__license__'
]

# Steel industry constants
VALID_STEEL_GRADES = [
    'A36', 'A572-50', 'A992', 'A514', 'A588', 'A242', 'A709-50',
    'S355', 'S275', 'S235', 'S420', 'S460', 'Q235', 'Q345',
    '304SS', '316SS', '409SS', '430SS', '201SS'
]

VALID_STEEL_TYPES = [
    'Hot Rolled', 'Cold Rolled', 'Galvanized', 'Stainless Steel',
    'Carbon Steel', 'Alloy Steel', 'Tool Steel', 'Spring Steel'
]

VALID_PRODUCTION_LINES = [
    'Line-A1', 'Line-A2', 'Line-B1', 'Line-B2', 'Line-C1', 'Line-C2',
    'Line-D1', 'Line-D2', 'Line-E1', 'Line-E2'
]

VALID_ORDER_STATUS = [
    'Pending', 'In Production', 'Quality Check', 'Ready', 'Shipped',
    'Delivered', 'Cancelled', 'Hold', 'Rework Required'
]
