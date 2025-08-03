#!/usr/bin/env python3
"""
Flight Booking Confirmation Automation - Main Entry Point
This script contains intentional bugs and performance issues for debugging practice.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data_processor import FlightDataProcessor
from src.email_service import EmailConfirmationService
from src.validation import DataValidator
from src.reporting import ReportGenerator
import logging
import time
import cProfile
import psutil
import gc

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    """Main automation workflow with intentional performance and logic issues."""
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    logger.info("Starting Flight Booking Confirmation Automation")
    logger.info(f"Initial memory usage: {initial_memory:.2f} MB")
    
    try:
        # Load and process data
        data_file = "data/reservations.csv"
        processor = FlightDataProcessor()
        
        # Bug 1: Not checking if file exists
        raw_data = processor.load_data(data_file)
        logger.info(f"Loaded {len(raw_data)} reservation records")
        
        # Bug 2: Not handling data validation properly
        validator = DataValidator()
        valid_data = validator.validate_reservations(raw_data)
        
        # Bug 3: Processing data inefficiently (row by row instead of vectorized)
        processed_data = processor.process_reservations(valid_data)
        logger.info(f"Processed {len(processed_data)} valid reservations")
        
        # Bug 4: Email service has synchronous processing (should be async/batched)
        email_service = EmailConfirmationService()
        confirmation_results = email_service.send_confirmations(processed_data)
        
        # Bug 5: Not releasing memory of large objects
        # processed_data is kept in memory unnecessarily
        
        # Generate reports
        report_generator = ReportGenerator()
        report_data = report_generator.generate_summary_report(processed_data, confirmation_results)
        
        # Bug 6: No error handling for report generation
        report_generator.save_report(report_data, "reports/flight_automation_report.csv")
        
        # Performance metrics
        end_time = time.time()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        logger.info("=== AUTOMATION COMPLETED ===")
        logger.info(f"Total runtime: {end_time - start_time:.2f} seconds")
        logger.info(f"Peak memory usage: {final_memory:.2f} MB")
        logger.info(f"Memory increase: {final_memory - initial_memory:.2f} MB")
        logger.info(f"Records processed: {len(processed_data)}")
        logger.info(f"Confirmations sent: {sum(1 for r in confirmation_results if r['status'] == 'sent')}")
        
    except Exception as e:
        logger.error(f"Automation failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Profile the execution
    profiler = cProfile.Profile()
    profiler.enable()
    
    main()
    
    profiler.disable()
    profiler.dump_stats('automation_profile.prof')
    logger.info("Profiling data saved to automation_profile.prof")
