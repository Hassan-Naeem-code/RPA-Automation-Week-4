"""
Performance metrics collection and analysis utilities.
"""

import time
import psutil
import functools
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass
from contextlib import contextmanager

from .logger import PerformanceLogger


@dataclass
class PerformanceMetrics:
    """Container for performance metrics."""
    operation: str
    start_time: float
    end_time: float
    duration: float
    initial_memory: float
    peak_memory: float
    memory_delta: float
    records_processed: int = 0
    additional_metrics: Dict[str, Any] = None
    
    @property
    def records_per_second(self) -> float:
        """Calculate records processed per second."""
        return self.records_processed / self.duration if self.duration > 0 else 0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary."""
        data = {
            'operation': self.operation,
            'duration_seconds': self.duration,
            'initial_memory_mb': self.initial_memory,
            'peak_memory_mb': self.peak_memory,
            'memory_delta_mb': self.memory_delta,
            'records_processed': self.records_processed,
            'records_per_second': self.records_per_second,
        }
        
        if self.additional_metrics:
            data.update(self.additional_metrics)
        
        return data


class PerformanceMonitor:
    """Performance monitoring utility."""
    
    def __init__(self):
        self.process = psutil.Process()
        self.logger = PerformanceLogger()
        self._metrics_history = []
    
    def get_memory_usage(self) -> float:
        """Get current memory usage in MB."""
        return self.process.memory_info().rss / 1024 / 1024
    
    def get_cpu_usage(self) -> float:
        """Get current CPU usage percentage."""
        return self.process.cpu_percent()
    
    @contextmanager
    def measure_operation(self, operation_name: str, records_count: int = 0):
        """
        Context manager to measure operation performance.
        
        Args:
            operation_name: Name of the operation being measured
            records_count: Number of records being processed
            
        Yields:
            PerformanceMetrics object that gets populated during execution
        """
        start_time = time.time()
        initial_memory = self.get_memory_usage()
        peak_memory = initial_memory
        
        # Create metrics object
        metrics = PerformanceMetrics(
            operation=operation_name,
            start_time=start_time,
            end_time=0,
            duration=0,
            initial_memory=initial_memory,
            peak_memory=peak_memory,
            memory_delta=0,
            records_processed=records_count
        )
        
        try:
            yield metrics
            
        finally:
            end_time = time.time()
            final_memory = self.get_memory_usage()
            
            # Update metrics
            metrics.end_time = end_time
            metrics.duration = end_time - start_time
            metrics.peak_memory = max(peak_memory, final_memory)
            metrics.memory_delta = final_memory - initial_memory
            
            # Log metrics
            self.logger.log_processing_metrics(
                operation=operation_name,
                duration=metrics.duration,
                records_processed=records_count,
                memory_usage=final_memory,
                memory_delta=metrics.memory_delta,
                records_per_second=metrics.records_per_second
            )
            
            # Store in history
            self._metrics_history.append(metrics)
    
    def get_metrics_history(self) -> list[PerformanceMetrics]:
        """Get all recorded metrics."""
        return self._metrics_history.copy()
    
    def get_operation_summary(self, operation_name: str) -> Dict[str, Any]:
        """
        Get summary statistics for a specific operation.
        
        Args:
            operation_name: Name of the operation to summarize
            
        Returns:
            Summary statistics dictionary
        """
        operation_metrics = [
            m for m in self._metrics_history 
            if m.operation == operation_name
        ]
        
        if not operation_metrics:
            return {}
        
        durations = [m.duration for m in operation_metrics]
        memory_deltas = [m.memory_delta for m in operation_metrics]
        records_per_sec = [m.records_per_second for m in operation_metrics]
        
        return {
            'operation': operation_name,
            'total_executions': len(operation_metrics),
            'avg_duration': sum(durations) / len(durations),
            'min_duration': min(durations),
            'max_duration': max(durations),
            'avg_memory_delta': sum(memory_deltas) / len(memory_deltas),
            'avg_records_per_second': sum(records_per_sec) / len(records_per_sec),
            'max_records_per_second': max(records_per_sec),
        }


def performance_monitor(operation_name: str = None, log_results: bool = True):
    """
    Decorator to monitor function performance.
    
    Args:
        operation_name: Name for the operation (defaults to function name)
        log_results: Whether to log the results
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            op_name = operation_name or func.__name__
            monitor = PerformanceMonitor()
            
            with monitor.measure_operation(op_name) as metrics:
                result = func(*args, **kwargs)
                
                # Try to extract record count from result if it's a DataFrame or list
                if hasattr(result, '__len__'):
                    metrics.records_processed = len(result)
                elif hasattr(result, 'shape'):  # pandas DataFrame
                    metrics.records_processed = result.shape[0]
            
            return result
        
        return wrapper
    return decorator


class MemoryProfiler:
    """Memory usage profiler for identifying memory leaks."""
    
    def __init__(self):
        self.process = psutil.Process()
        self._snapshots = []
    
    def take_snapshot(self, label: str = None):
        """
        Take a memory snapshot.
        
        Args:
            label: Optional label for the snapshot
        """
        memory_info = self.process.memory_info()
        snapshot = {
            'timestamp': time.time(),
            'label': label or f"snapshot_{len(self._snapshots)}",
            'rss_mb': memory_info.rss / 1024 / 1024,
            'vms_mb': memory_info.vms / 1024 / 1024,
            'percent': self.process.memory_percent(),
        }
        
        self._snapshots.append(snapshot)
        return snapshot
    
    def get_memory_growth(self) -> Dict[str, Any]:
        """
        Calculate memory growth between first and last snapshot.
        
        Returns:
            Memory growth statistics
        """
        if len(self._snapshots) < 2:
            return {}
        
        first = self._snapshots[0]
        last = self._snapshots[-1]
        
        return {
            'initial_memory_mb': first['rss_mb'],
            'final_memory_mb': last['rss_mb'],
            'memory_growth_mb': last['rss_mb'] - first['rss_mb'],
            'memory_growth_percent': (
                (last['rss_mb'] - first['rss_mb']) / first['rss_mb'] * 100
                if first['rss_mb'] > 0 else 0
            ),
            'duration_seconds': last['timestamp'] - first['timestamp'],
            'total_snapshots': len(self._snapshots)
        }
    
    def detect_memory_leaks(self, threshold_mb: float = 50) -> bool:
        """
        Detect potential memory leaks.
        
        Args:
            threshold_mb: Memory growth threshold in MB
            
        Returns:
            True if potential leak detected
        """
        growth = self.get_memory_growth()
        return growth.get('memory_growth_mb', 0) > threshold_mb


# Global performance monitor instance
performance_monitor_instance = PerformanceMonitor()
