#!/usr/bin/env python3
"""
Steel Industry Automation System - Main Script

Production-ready steel order processing automation with performance optimization,
comprehensive error handling, and enterprise features.

Usage:
    python main_steel.py [options]

Options:
    --config PATH    Path to configuration file (default: config/settings.yaml)
    --data PATH      Path to steel orders CSV file (default: data/steel_orders.csv)
    --output PATH    Output directory for reports (default: reports/)
    --profile        Enable performance profiling
    --verbose        Enable verbose logging
    --dry-run        Perform validation only, no actual processing
"""

import sys
import argparse
import logging
import time
import cProfile
import pstats
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from steel_automation.core.data_processor import SteelDataProcessor
from steel_automation.core.validation import SteelDataValidator
from steel_automation.services.email_service import EmailService
from steel_automation.services.reporting import ReportGenerator
from steel_automation.utils.logger import LoggerManager
from steel_automation.utils.metrics import PerformanceMonitor

def setup_logging(log_level=logging.INFO, log_file=None):
    """Set up logging configuration"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    if log_file:
        logging.basicConfig(
            level=log_level,
            format=log_format,
            filename=log_file,
            filemode='a'
        )
    else:
        logging.basicConfig(
            level=log_level,
            format=log_format
        )
    
    return logging.getLogger(__name__)

def load_config(config_path: str) -> dict:
    """Load configuration from YAML file"""
    try:
        import yaml
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Warning: Could not load config from {config_path}: {e}")
        return {}

def main():
    """Main steel automation processing function"""
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Steel Industry Automation System')
    parser.add_argument('--config', default='config/settings.yaml', help='Configuration file path')
    parser.add_argument('--data', default='data/steel_orders.csv', help='Steel orders CSV file path')
    parser.add_argument('--output', default='reports/', help='Output directory for reports')
    parser.add_argument('--profile', action='store_true', help='Enable performance profiling')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    parser.add_argument('--dry-run', action='store_true', help='Validation only, no processing')
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_file = f"logs/steel_automation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    logger = setup_logging(log_level, log_file)
    
    logger.info("=" * 60)
    logger.info("STEEL INDUSTRY AUTOMATION SYSTEM STARTED")
    logger.info("=" * 60)
    logger.info(f"Data file: {args.data}")
    logger.info(f"Output directory: {args.output}")
    logger.info(f"Dry run mode: {args.dry_run}")
    
    # Load configuration
    config = load_config(args.config)
    logger.info(f"Configuration loaded from {args.config}")
    
    # Initialize performance monitoring
    performance_monitor = PerformanceMonitor()
    
    try:
        # Initialize components
        logger.info("Initializing steel automation components...")
        
        data_processor = SteelDataProcessor(config)
        validator = SteelDataValidator(config)
        email_service = EmailService(config.get('email', {}))
        report_generator = ReportGenerator(config)
        
        # Performance profiling setup
        profiler = None
        if args.profile:
            profiler = cProfile.Profile()
            profiler.enable()
            logger.info("Performance profiling enabled")
        
        # Phase 1: Data Loading and Validation
        logger.info("Phase 1: Loading and validating steel orders...")
        
        # Load data
        with performance_monitor.measure_operation('data_loading', 0) as metrics:
            raw_data = data_processor.process_steel_orders(args.data)
            metrics.records_processed = len(raw_data)
        
        logger.info(f"Loaded {len(raw_data)} steel order records")
        
        # Validate data
        with performance_monitor.measure_operation('data_validation', len(raw_data)) as metrics:
            validated_data = validator.validate_steel_orders(raw_data)
            metrics.records_processed = len(validated_data)
        
        validation_summary = validator.get_validation_summary()
        logger.info(f"Validation completed: {len(validated_data)} valid orders")
        logger.info(f"Validation success rate: {validation_summary['validation_stats']['valid_records'] / validation_summary['validation_stats']['total_records_validated'] * 100:.1f}%")
        
        if args.dry_run:
            logger.info("DRY RUN MODE: Stopping after validation")
            
            # Generate validation report
            validation_report_path = f"{args.output}/validation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            import json
            with open(validation_report_path, 'w') as f:
                json.dump(validation_summary, f, indent=2)
            logger.info(f"Validation report saved to {validation_report_path}")
            
            return
        
        # Phase 2: Data Processing (if not dry run)
        logger.info("Phase 2: Processing validated steel orders...")
        
        # Additional processing could be added here
        with performance_monitor.measure_operation('data_processing', len(validated_data)) as metrics:
            processed_data = validated_data.copy()
            metrics.records_processed = len(processed_data)
        
        logger.info(f"Processing completed for {len(processed_data)} orders")
        
        # Phase 3: Customer Notifications
        logger.info("Phase 3: Sending customer notifications...")
        
        with performance_monitor.measure_operation('email_processing', len(processed_data)) as metrics:
            email_results = email_service.send_order_confirmations(processed_data)
            metrics.records_processed = len(processed_data)
        
        email_stats = email_service.get_email_stats()
        logger.info(f"Email notifications completed: {email_stats['email_stats']['successful_emails']} sent successfully")
        
        # Phase 4: Report Generation
        logger.info("Phase 4: Generating reports...")
        
        with performance_monitor.measure_operation('report_generation', len(processed_data)) as metrics:
            # Generate comprehensive reports
            reports = report_generator.generate_steel_reports(
                processed_data,
                validation_summary,
                email_stats,
                args.output
            )
            metrics.records_processed = len(reports)
        
        logger.info(f"Reports generated: {len(reports)} files created")
        
        # Final Performance Summary
        logger.info("=" * 60)
        logger.info("STEEL AUTOMATION COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)
        logger.info(f"Orders processed: {len(processed_data)}")
        logger.info(f"Email success rate: {email_stats['performance_metrics']['success_rate']:.1f}%")
        
        # Save performance profile
        if profiler:
            profiler.disable()
            profile_file = f"steel_automation_profile_{datetime.now().strftime('%Y%m%d_%H%M%S')}.prof"
            profiler.dump_stats(profile_file)
            logger.info(f"Performance profile saved to {profile_file}")
            
            # Print top 10 functions by time
            stats = pstats.Stats(profile_file)
            stats.sort_stats('tottime')
            logger.info("Top 10 functions by execution time:")
            stats.print_stats(10)
        
        return 0
        
    except FileNotFoundError as e:
        logger.error(f"File not found: {e}")
        return 1
        
    except Exception as e:
        logger.error(f"Steel automation failed: {e}", exc_info=True)
        return 1
        
    finally:
        logger.info("Steel automation system shutdown")

if __name__ == "__main__":
    sys.exit(main())
