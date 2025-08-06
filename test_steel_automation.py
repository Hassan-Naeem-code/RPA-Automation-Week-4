#!/usr/bin/env python3
"""
Simple Steel Automation Test Script
"""

import sys
import logging
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_steel_automation():
    """Test steel automation components individually"""
    
    # Setup basic logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("Testing Steel Automation System Components")
    
    try:
        # Test 1: Data Processor
        logger.info("Testing SteelDataProcessor...")
        from steel_automation.core.data_processor import SteelDataProcessor
        processor = SteelDataProcessor()
        logger.info("✓ SteelDataProcessor imported successfully")
        
        # Test 2: Validator
        logger.info("Testing SteelDataValidator...")
        from steel_automation.core.validation import SteelDataValidator
        validator = SteelDataValidator()
        logger.info("✓ SteelDataValidator imported successfully")
        
        # Test 3: Email Service
        logger.info("Testing EmailService...")
        from steel_automation.services.email_service import EmailService
        email_service = EmailService()
        logger.info("✓ EmailService imported successfully")
        
        # Test 4: Report Generator
        logger.info("Testing ReportGenerator...")
        from steel_automation.services.reporting import ReportGenerator
        report_gen = ReportGenerator()
        logger.info("✓ ReportGenerator imported successfully")
        
        # Test 5: Process sample data
        logger.info("Testing data processing with steel orders...")
        steel_data = processor.process_steel_orders('data/steel_orders.csv')
        logger.info(f"✓ Processed {len(steel_data)} steel orders")
        
        # Test 6: Validation
        logger.info("Testing validation...")
        validated_data = validator.validate_steel_orders(steel_data)
        logger.info(f"✓ Validated {len(validated_data)} orders")
        
        logger.info("=" * 50)
        logger.info("STEEL AUTOMATION SYSTEM TEST COMPLETED SUCCESSFULLY")
        logger.info(f"Total orders processed: {len(steel_data)}")
        logger.info(f"Valid orders: {len(validated_data)}")
        logger.info(f"Success rate: {len(validated_data)/len(steel_data)*100:.1f}%")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}", exc_info=True)
        return False

if __name__ == "__main__":
    success = test_steel_automation()
    sys.exit(0 if success else 1)
