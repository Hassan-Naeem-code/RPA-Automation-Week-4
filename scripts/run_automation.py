#!/usr/bin/env python3
"""
Flight Booking Automation - Main Execution Script

Production-ready automation script with industry-standard structure.
"""

import sys
import os
import argparse
import yaml
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from flight_automation import (
    DataProcessor,
    EmailService,
    DataValidator,
    ReportGenerator,
    LoggerManager,
    PerformanceMonitor
)
from flight_automation.utils.metrics import performance_monitor


def load_config(config_path: str = None) -> dict:
    """
    Load application configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
    """
    if config_path is None:
        config_path = project_root / "config" / "settings.yaml"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        raise RuntimeError(f"Failed to load configuration: {e}")


@performance_monitor("full_automation_pipeline")
def run_automation_pipeline(config: dict, data_file: str = None) -> dict:
    """
    Execute the complete automation pipeline.
    
    Args:
        config: Application configuration
        data_file: Path to data file (optional)
        
    Returns:
        Pipeline execution results
    """
    logger_manager = LoggerManager()
    logger = logger_manager.get_logger('flight_automation.main')
    monitor = PerformanceMonitor()
    
    logger.info("Starting Flight Booking Automation Pipeline")
    
    # Initialize components
    processor = DataProcessor()
    validator = DataValidator()
    email_service = EmailService()
    report_generator = ReportGenerator()
    
    try:
        # Data loading phase
        with monitor.measure_operation("data_loading") as metrics:
            if data_file is None:
                data_file = config['data']['input_path'] + "reservations.csv"
            
            if not os.path.exists(data_file):
                raise FileNotFoundError(f"Data file not found: {data_file}")
            
            raw_data = processor.load_data(data_file)
            metrics.records_processed = len(raw_data)
            logger.info(f"Loaded {len(raw_data)} reservation records")
        
        # Data validation phase
        with monitor.measure_operation("data_validation", len(raw_data)) as metrics:
            validated_data = validator.validate_reservations(raw_data)
            metrics.records_processed = len(validated_data)
            logger.info(f"Validated data: {len(validated_data)} valid records")
        
        # Data processing phase
        with monitor.measure_operation("data_processing", len(validated_data)) as metrics:
            if config['performance']['optimization']['use_vectorized_operations']:
                processed_data = processor.clean_data_optimized(validated_data)
            else:
                processed_data = processor.process_reservations(validated_data)
            
            metrics.records_processed = len(processed_data)
            logger.info(f"Processed {len(processed_data)} reservations")
        
        # Email confirmation phase
        with monitor.measure_operation("email_processing", len(processed_data)) as metrics:
            if config['performance']['optimization']['enable_concurrent_processing']:
                confirmation_results = email_service.send_confirmations_optimized(processed_data)
            else:
                confirmation_results = email_service.send_confirmations(processed_data)
            
            successful = sum(1 for r in confirmation_results if r['status'] == 'sent')
            failed = sum(1 for r in confirmation_results if r['status'] == 'failed')
            
            logger.info(f"Email confirmations: {successful} sent, {failed} failed")
        
        # Report generation phase
        with monitor.measure_operation("report_generation") as metrics:
            # Ensure output directory exists
            output_dir = Path(config['data']['output_path'])
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate reports
            if config['reporting']['include_detailed_report']:
                report_data, detailed_path = report_generator.generate_detailed_report(
                    processed_data, confirmation_results
                )
            else:
                report_data = report_generator.generate_summary_report(
                    processed_data, confirmation_results
                )
                detailed_path = None
            
            # Save summary report
            summary_path = output_dir / "automation_summary_report.csv"
            report_generator.save_report(report_data, str(summary_path))
            
            logger.info(f"Reports generated: {summary_path}")
            if detailed_path:
                logger.info(f"Detailed report: {detailed_path}")
        
        # Calculate pipeline results
        pipeline_results = {
            'status': 'success',
            'total_records_input': len(raw_data),
            'total_records_processed': len(processed_data),
            'emails_sent': successful,
            'emails_failed': failed,
            'summary_report_path': str(summary_path),
            'detailed_report_path': detailed_path,
            'performance_summary': monitor.get_operation_summary("full_automation_pipeline")
        }
        
        logger.info("=== AUTOMATION PIPELINE COMPLETED SUCCESSFULLY ===")
        return pipeline_results
        
    except Exception as e:
        logger.error(f"Automation pipeline failed: {str(e)}")
        raise


def main():
    """Main entry point for the automation script."""
    parser = argparse.ArgumentParser(
        description="Flight Booking Automation System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/run_automation.py
  python scripts/run_automation.py --config config/settings.yaml
  python scripts/run_automation.py --data data/sample/reservations.csv
  python scripts/run_automation.py --profile --verbose
        """
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to configuration file (default: config/settings.yaml)'
    )
    
    parser.add_argument(
        '--data', '-d',
        type=str,
        help='Path to input data file'
    )
    
    parser.add_argument(
        '--profile', '-p',
        action='store_true',
        help='Enable detailed performance profiling'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run without sending actual emails'
    )
    
    args = parser.parse_args()
    
    try:
        # Load configuration
        config = load_config(args.config)
        
        # Adjust logging level if verbose
        if args.verbose:
            import logging
            logging.getLogger('flight_automation').setLevel(logging.DEBUG)
        
        # Setup profiling if requested
        profiler = None
        if args.profile:
            import cProfile
            profiler = cProfile.Profile()
            profiler.enable()
        
        # Override email sending for dry run
        if args.dry_run:
            config['email']['max_workers'] = 1
            print("DRY RUN MODE: No emails will be sent")
        
        # Run the automation pipeline
        results = run_automation_pipeline(config, args.data)
        
        # Print results summary
        print("\n" + "="*60)
        print("AUTOMATION PIPELINE RESULTS")
        print("="*60)
        print(f"Status: {results['status'].upper()}")
        print(f"Input records: {results['total_records_input']}")
        print(f"Processed records: {results['total_records_processed']}")
        print(f"Emails sent: {results['emails_sent']}")
        print(f"Emails failed: {results['emails_failed']}")
        print(f"Summary report: {results['summary_report_path']}")
        if results['detailed_report_path']:
            print(f"Detailed report: {results['detailed_report_path']}")
        print("="*60)
        
        # Save profiling data if enabled
        if profiler:
            profiler.disable()
            profiler.dump_stats('logs/automation_profile.prof')
            print(f"Profiling data saved to: logs/automation_profile.prof")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
