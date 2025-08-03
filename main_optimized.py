#!/usr/bin/env python3
"""
Optimized Flight Booking Confirmation Automation
This version implements performance improvements and better error handling.
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
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('automation_optimized.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main_optimized():
    """Optimized automation workflow with performance improvements."""
    start_time = time.time()
    process = psutil.Process()
    initial_memory = process.memory_info().rss / 1024 / 1024  # MB
    
    logger.info("Starting OPTIMIZED Flight Booking Confirmation Automation")
    logger.info(f"Initial memory usage: {initial_memory:.2f} MB")
    
    try:
        # Check file existence first
        data_file = "data/reservations.csv"
        if not os.path.exists(data_file):
            raise FileNotFoundError(f"Data file not found: {data_file}")
        
        # Load and process data with optimized methods
        processor = FlightDataProcessor()
        raw_data = processor.load_data(data_file)
        logger.info(f"Loaded {len(raw_data)} reservation records")
        
        # Optimized data cleaning (vectorized operations)
        cleaned_data = processor.clean_data_optimized(raw_data)
        logger.info(f"Cleaned data: {len(cleaned_data)} valid records")
        
        # Memory cleanup after raw data processing
        del raw_data
        gc.collect()
        
        # Optimized email service with concurrent processing
        email_service = EmailConfirmationService()
        confirmation_results = email_service.send_confirmations_optimized(cleaned_data)
        
        # Memory cleanup after email processing
        gc.collect()
        
        # Generate reports with improved error handling
        report_generator = ReportGenerator()
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Generate detailed report
        report_data, detailed_path = report_generator.generate_detailed_report(
            cleaned_data, confirmation_results
        )
        
        # Save summary report
        summary_path = "reports/optimized_automation_report.csv"
        report_generator.save_report(report_data, summary_path)
        
        # Performance metrics
        end_time = time.time()
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        logger.info("=== OPTIMIZED AUTOMATION COMPLETED ===")
        logger.info(f"Total runtime: {end_time - start_time:.2f} seconds")
        logger.info(f"Peak memory usage: {final_memory:.2f} MB")
        logger.info(f"Memory increase: {final_memory - initial_memory:.2f} MB")
        logger.info(f"Records processed: {len(cleaned_data)}")
        logger.info(f"Confirmations sent: {sum(1 for r in confirmation_results if r['status'] == 'sent')}")
        logger.info(f"Summary report: {summary_path}")
        logger.info(f"Detailed report: {detailed_path}")
        
        # Performance comparison metrics
        records_per_second = len(cleaned_data) / (end_time - start_time)
        logger.info(f"Processing rate: {records_per_second:.2f} records/second")
        
        return {
            'runtime': end_time - start_time,
            'memory_usage': final_memory,
            'memory_increase': final_memory - initial_memory,
            'records_processed': len(cleaned_data),
            'confirmations_sent': sum(1 for r in confirmation_results if r['status'] == 'sent'),
            'processing_rate': records_per_second
        }
        
    except Exception as e:
        logger.error(f"Optimized automation failed: {str(e)}")
        raise

if __name__ == "__main__":
    # Profile the optimized execution
    profiler = cProfile.Profile()
    profiler.enable()
    
    metrics = main_optimized()
    
    profiler.disable()
    profiler.dump_stats('automation_optimized_profile.prof')
    logger.info("Optimized profiling data saved to automation_optimized_profile.prof")
    
    # Print performance summary
    print("\n" + "="*50)
    print("PERFORMANCE SUMMARY")
    print("="*50)
    print(f"Runtime: {metrics['runtime']:.2f} seconds")
    print(f"Memory usage: {metrics['memory_usage']:.2f} MB")
    print(f"Records processed: {metrics['records_processed']}")
    print(f"Processing rate: {metrics['processing_rate']:.2f} records/second")
    print("="*50)
