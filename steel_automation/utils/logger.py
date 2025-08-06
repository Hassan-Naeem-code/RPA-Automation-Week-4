"""
Logging configuration and utilities.
"""

import logging
import logging.config
import yaml
import os
from pathlib import Path
from typing import Dict, Any


class LoggerManager:
    """Centralized logging configuration manager."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize logger manager with configuration.
        
        Args:
            config_path: Path to logging configuration file
        """
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), '../../config/logging.yaml')
        
        self.config_path = config_path
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration from YAML file."""
        try:
            # Ensure logs directory exists
            logs_dir = Path("logs")
            logs_dir.mkdir(exist_ok=True)
            
            # Load logging configuration
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Apply configuration
            logging.config.dictConfig(config)
            
        except Exception as e:
            # Fallback to basic logging if config fails
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.StreamHandler(),
                    logging.FileHandler('logs/automation.log')
                ]
            )
            logging.error(f"Failed to load logging config: {e}")
    
    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        """
        Get a logger with the specified name.
        
        Args:
            name: Logger name
            
        Returns:
            Configured logger instance
        """
        return logging.getLogger(name)
    
    @staticmethod
    def get_performance_logger() -> logging.Logger:
        """Get the performance metrics logger."""
        return logging.getLogger('steel_automation.performance')
    
    @staticmethod
    def get_audit_logger() -> logging.Logger:
        """Get the audit trail logger."""
        return logging.getLogger('steel_automation.audit')


# Global logger manager instance
_logger_manager = LoggerManager()

# Convenience functions
def get_logger(name: str = 'steel_automation') -> logging.Logger:
    """Get a logger with the specified name."""
    return _logger_manager.get_logger(name)

def get_performance_logger() -> logging.Logger:
    """Get the performance metrics logger."""
    return _logger_manager.get_performance_logger()

def get_audit_logger() -> logging.Logger:
    """Get the audit trail logger."""
    return _logger_manager.get_audit_logger()


class PerformanceLogger:
    """Specialized logger for performance metrics."""
    
    def __init__(self):
        self.logger = get_performance_logger()
    
    def log_processing_metrics(self, 
                             operation: str,
                             duration: float,
                             records_processed: int,
                             memory_usage: float = None,
                             **kwargs):
        """
        Log performance metrics for processing operations.
        
        Args:
            operation: Name of the operation
            duration: Duration in seconds
            records_processed: Number of records processed
            memory_usage: Memory usage in MB
            **kwargs: Additional metrics
        """
        metrics = {
            'operation': operation,
            'duration_seconds': duration,
            'records_processed': records_processed,
            'records_per_second': records_processed / duration if duration > 0 else 0,
        }
        
        if memory_usage is not None:
            metrics['memory_usage_mb'] = memory_usage
        
        metrics.update(kwargs)
        
        self.logger.info(f"Performance metrics: {metrics}")
    
    def log_email_metrics(self,
                         total_emails: int,
                         successful: int,
                         failed: int,
                         duration: float):
        """
        Log email processing metrics.
        
        Args:
            total_emails: Total number of emails processed
            successful: Number of successful sends
            failed: Number of failed sends
            duration: Duration in seconds
        """
        metrics = {
            'operation': 'email_processing',
            'total_emails': total_emails,
            'successful': successful,
            'failed': failed,
            'success_rate': successful / total_emails if total_emails > 0 else 0,
            'duration_seconds': duration,
            'emails_per_second': total_emails / duration if duration > 0 else 0
        }
        
        self.logger.info(f"Email metrics: {metrics}")


class AuditLogger:
    """Specialized logger for audit trail."""
    
    def __init__(self):
        self.logger = get_audit_logger()
    
    def log_data_processing(self,
                          operation: str,
                          input_records: int,
                          output_records: int,
                          data_source: str = None,
                          **kwargs):
        """
        Log data processing audit trail.
        
        Args:
            operation: Type of operation performed
            input_records: Number of input records
            output_records: Number of output records
            data_source: Source of the data
            **kwargs: Additional audit information
        """
        audit_data = {
            'type': 'data_processing',
            'operation': operation,
            'input_records': input_records,
            'output_records': output_records,
            'records_filtered': input_records - output_records,
        }
        
        if data_source:
            audit_data['data_source'] = data_source
        
        audit_data.update(kwargs)
        
        self.logger.info(f"Audit: {audit_data}")
    
    def log_email_activity(self,
                          pnr: str,
                          email: str,
                          status: str,
                          template: str = None):
        """
        Log email sending activity for audit.
        
        Args:
            pnr: Booking PNR
            email: Email address
            status: Send status (sent/failed)
            template: Email template used
        """
        audit_data = {
            'type': 'email_activity',
            'pnr': pnr,
            'email': self._mask_email(email),
            'status': status,
        }
        
        if template:
            audit_data['template'] = template
        
        self.logger.info(f"Audit: {audit_data}")
    
    @staticmethod
    def _mask_email(email: str) -> str:
        """
        Mask email address for privacy.
        
        Args:
            email: Email address to mask
            
        Returns:
            Masked email address
        """
        if not email or '@' not in email:
            return 'invalid_email'
        
        local, domain = email.split('@', 1)
        if len(local) <= 2:
            return f"{local}@{domain}"
        
        return f"{local[0]}{'*' * (len(local) - 2)}{local[-1]}@{domain}"
