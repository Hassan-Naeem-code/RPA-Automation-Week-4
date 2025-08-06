"""
Steel Industry Reporting Module

This module generates comprehensive reports for steel production automation,
including order summaries, production metrics, quality analysis, and performance statistics.

Features:
- Production summary reports
- Order status analytics
- Quality control statistics
- Performance metrics
- Customer analytics
- Export to multiple formats
"""

import pandas as pd
import logging
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

class ReportGenerator:
    """
    Comprehensive reporting system for steel industry automation with
    multiple export formats and detailed analytics.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Report Generator
        
        Args:
            config: Configuration dictionary with reporting settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Report generation settings
        self.output_formats = self.config.get('reporting', {}).get('export_formats', ['json', 'csv'])
        self.include_charts = self.config.get('reporting', {}).get('include_charts', False)
        
        # Report storage
        self.reports = {}
    
    def generate_order_summary(self, orders_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate comprehensive order summary statistics
        
        Args:
            orders_data: DataFrame containing processed steel orders
            
        Returns:
            Dictionary containing order summary metrics
        """
        try:
            summary = {
                'timestamp': datetime.now().isoformat(),
                'total_orders': len(orders_data),
                'total_value': float(orders_data['TotalPrice'].sum()),
                'total_weight': float(orders_data['Weight'].sum()),
                'average_order_value': float(orders_data['TotalPrice'].mean()),
                'average_weight': float(orders_data['Weight'].mean())
            }
            
            # Order status breakdown
            status_counts = orders_data['Status'].value_counts()
            summary['status_breakdown'] = {
                status: int(count) for status, count in status_counts.items()
            }
            
            # Steel grade analysis
            grade_stats = orders_data.groupby('SteelGrade').agg({
                'TotalPrice': ['count', 'sum', 'mean'],
                'Weight': ['sum', 'mean']
            }).round(2)
            
            summary['steel_grade_analysis'] = {}
            for grade in grade_stats.index:
                summary['steel_grade_analysis'][grade] = {
                    'order_count': int(grade_stats.loc[grade, ('TotalPrice', 'count')]),
                    'total_value': float(grade_stats.loc[grade, ('TotalPrice', 'sum')]),
                    'average_value': float(grade_stats.loc[grade, ('TotalPrice', 'mean')]),
                    'total_weight': float(grade_stats.loc[grade, ('Weight', 'sum')]),
                    'average_weight': float(grade_stats.loc[grade, ('Weight', 'mean')])
                }
            
            # Production line utilization
            line_utilization = orders_data['ProductionLine'].value_counts()
            summary['production_line_utilization'] = {
                line: int(count) for line, count in line_utilization.items()
            }
            
            # Quality grade distribution
            quality_distribution = orders_data['QualityGrade'].value_counts()
            summary['quality_distribution'] = {
                grade: int(count) for grade, count in quality_distribution.items()
            }
            
            # Customer analysis
            customer_stats = orders_data.groupby('CustomerName').agg({
                'TotalPrice': ['count', 'sum'],
                'Weight': 'sum'
            })
            
            top_customers = customer_stats.sort_values(('TotalPrice', 'sum'), ascending=False).head(10)
            summary['top_customers'] = {}
            for customer in top_customers.index:
                summary['top_customers'][customer] = {
                    'order_count': int(top_customers.loc[customer, ('TotalPrice', 'count')]),
                    'total_value': float(top_customers.loc[customer, ('TotalPrice', 'sum')]),
                    'total_weight': float(top_customers.loc[customer, ('Weight', 'sum')])
                }
            
            # Warehouse distribution
            warehouse_stats = orders_data['Warehouse'].value_counts()
            summary['warehouse_distribution'] = {
                warehouse: int(count) for warehouse, count in warehouse_stats.items()
            }
            
            self.logger.info(f"Generated order summary for {len(orders_data)} orders")
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating order summary: {e}")
            raise
    
    def generate_production_metrics(self, orders_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate production performance metrics
        
        Args:
            orders_data: DataFrame containing steel orders
            
        Returns:
            Dictionary containing production metrics
        """
        try:
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'production_overview': {}
            }
            
            # Calculate production efficiency by line
            production_lines = orders_data['ProductionLine'].unique()
            
            for line in production_lines:
                line_data = orders_data[orders_data['ProductionLine'] == line]
                
                # Calculate metrics for this production line
                line_metrics = {
                    'total_orders': len(line_data),
                    'total_weight': float(line_data['Weight'].sum()),
                    'total_value': float(line_data['TotalPrice'].sum()),
                    'average_order_size': float(line_data['Weight'].mean()),
                    'quality_distribution': line_data['QualityGrade'].value_counts().to_dict(),
                    'status_distribution': line_data['Status'].value_counts().to_dict()
                }
                
                # Calculate quality rate (A and B grades as good quality)
                good_quality_count = len(line_data[line_data['QualityGrade'].isin(['A', 'B'])])
                line_metrics['quality_rate'] = (good_quality_count / len(line_data)) * 100 if len(line_data) > 0 else 0
                
                # Calculate completion rate
                completed_count = len(line_data[line_data['Status'].isin(['Ready', 'Shipped', 'Delivered'])])
                line_metrics['completion_rate'] = (completed_count / len(line_data)) * 100 if len(line_data) > 0 else 0
                
                metrics['production_overview'][line] = line_metrics
            
            # Overall production metrics
            total_orders = len(orders_data)
            completed_orders = len(orders_data[orders_data['Status'].isin(['Ready', 'Shipped', 'Delivered'])])
            good_quality_orders = len(orders_data[orders_data['QualityGrade'].isin(['A', 'B'])])
            
            metrics['overall_metrics'] = {
                'total_orders': total_orders,
                'completion_rate': (completed_orders / total_orders) * 100 if total_orders > 0 else 0,
                'quality_rate': (good_quality_orders / total_orders) * 100 if total_orders > 0 else 0,
                'average_order_value': float(orders_data['TotalPrice'].mean()),
                'total_production_value': float(orders_data['TotalPrice'].sum()),
                'total_production_weight': float(orders_data['Weight'].sum())
            }
            
            self.logger.info("Generated production metrics")
            return metrics
            
        except Exception as e:
            self.logger.error(f"Error generating production metrics: {e}")
            raise
    
    def generate_quality_analysis(self, orders_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate quality control analysis
        
        Args:
            orders_data: DataFrame containing steel orders
            
        Returns:
            Dictionary containing quality analysis
        """
        try:
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'quality_overview': {}
            }
            
            # Overall quality statistics
            quality_counts = orders_data['QualityGrade'].value_counts()
            total_orders = len(orders_data)
            
            analysis['quality_overview'] = {
                'total_orders': total_orders,
                'quality_distribution': quality_counts.to_dict(),
                'quality_percentages': {
                    grade: (count / total_orders) * 100 
                    for grade, count in quality_counts.items()
                }
            }
            
            # Quality by steel grade
            quality_by_grade = orders_data.groupby(['SteelGrade', 'QualityGrade']).size().unstack(fill_value=0)
            analysis['quality_by_steel_grade'] = quality_by_grade.to_dict()
            
            # Quality by production line
            quality_by_line = orders_data.groupby(['ProductionLine', 'QualityGrade']).size().unstack(fill_value=0)
            analysis['quality_by_production_line'] = quality_by_line.to_dict()
            
            # Quality trends (if date data available)
            if 'ProductionDate' in orders_data.columns:
                orders_data['ProductionDate'] = pd.to_datetime(orders_data['ProductionDate'])
                quality_trends = orders_data.groupby([
                    orders_data['ProductionDate'].dt.date, 
                    'QualityGrade'
                ]).size().unstack(fill_value=0)
                
                analysis['quality_trends'] = {
                    str(date): quality_trends.loc[date].to_dict() 
                    for date in quality_trends.index
                }
            
            # Quality issues analysis
            problematic_orders = orders_data[orders_data['QualityGrade'].isin(['Reject', 'Rework'])]
            
            analysis['quality_issues'] = {
                'total_problematic_orders': len(problematic_orders),
                'reject_rate': (len(orders_data[orders_data['QualityGrade'] == 'Reject']) / total_orders) * 100,
                'rework_rate': (len(orders_data[orders_data['QualityGrade'] == 'Rework']) / total_orders) * 100,
                'issues_by_steel_grade': problematic_orders['SteelGrade'].value_counts().to_dict(),
                'issues_by_production_line': problematic_orders['ProductionLine'].value_counts().to_dict()
            }
            
            self.logger.info("Generated quality analysis")
            return analysis
            
        except Exception as e:
            self.logger.error(f"Error generating quality analysis: {e}")
            raise
    
    def generate_customer_analytics(self, orders_data: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate customer analytics and insights
        
        Args:
            orders_data: DataFrame containing steel orders
            
        Returns:
            Dictionary containing customer analytics
        """
        try:
            analytics = {
                'timestamp': datetime.now().isoformat(),
                'customer_overview': {}
            }
            
            # Customer summary statistics
            customer_stats = orders_data.groupby('CustomerName').agg({
                'OrderID': 'count',
                'TotalPrice': ['sum', 'mean'],
                'Weight': ['sum', 'mean'],
                'QualityGrade': lambda x: (x.isin(['A', 'B'])).mean() * 100  # Quality rate
            }).round(2)
            
            customer_stats.columns = ['order_count', 'total_value', 'avg_order_value', 'total_weight', 'avg_weight', 'quality_rate']
            
            # Top customers by value
            top_customers_by_value = customer_stats.sort_values('total_value', ascending=False).head(10)
            analytics['top_customers_by_value'] = top_customers_by_value.to_dict('index')
            
            # Top customers by volume
            top_customers_by_volume = customer_stats.sort_values('order_count', ascending=False).head(10)
            analytics['top_customers_by_volume'] = top_customers_by_volume.to_dict('index')
            
            # Customer distribution analysis
            analytics['customer_distribution'] = {
                'total_customers': len(customer_stats),
                'avg_orders_per_customer': float(customer_stats['order_count'].mean()),
                'avg_value_per_customer': float(customer_stats['total_value'].mean()),
                'customer_value_distribution': {
                    'high_value': len(customer_stats[customer_stats['total_value'] > customer_stats['total_value'].quantile(0.8)]),
                    'medium_value': len(customer_stats[
                        (customer_stats['total_value'] > customer_stats['total_value'].quantile(0.2)) &
                        (customer_stats['total_value'] <= customer_stats['total_value'].quantile(0.8))
                    ]),
                    'low_value': len(customer_stats[customer_stats['total_value'] <= customer_stats['total_value'].quantile(0.2)])
                }
            }
            
            self.logger.info("Generated customer analytics")
            return analytics
            
        except Exception as e:
            self.logger.error(f"Error generating customer analytics: {e}")
            raise
    
    def save_report(self, report_data: Dict[str, Any], filename: str, output_dir: str) -> List[str]:
        """
        Save report data in multiple formats
        
        Args:
            report_data: Dictionary containing report data
            filename: Base filename for the report
            output_dir: Output directory path
            
        Returns:
            List of created file paths
        """
        created_files = []
        
        try:
            # Ensure output directory exists
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            
            # Save in requested formats
            for format_type in self.output_formats:
                if format_type == 'json':
                    json_path = os.path.join(output_dir, f"{filename}.json")
                    with open(json_path, 'w') as f:
                        json.dump(report_data, f, indent=2, default=str)
                    created_files.append(json_path)
                
                elif format_type == 'csv' and isinstance(report_data, dict):
                    # Convert nested dict to flat structure for CSV
                    csv_path = os.path.join(output_dir, f"{filename}.csv")
                    
                    # Create a simple CSV for summary data
                    if 'total_orders' in report_data:
                        summary_df = pd.DataFrame([{
                            'metric': key,
                            'value': value
                        } for key, value in report_data.items() if not isinstance(value, dict)])
                        
                        summary_df.to_csv(csv_path, index=False)
                        created_files.append(csv_path)
            
            self.logger.info(f"Saved report {filename} in {len(created_files)} formats")
            return created_files
            
        except Exception as e:
            self.logger.error(f"Error saving report {filename}: {e}")
            raise
    
    def generate_steel_reports(self, orders_data: pd.DataFrame, validation_summary: Dict, 
                              email_stats: Dict, output_dir: str) -> List[str]:
        """
        Generate comprehensive steel industry reports
        
        Args:
            orders_data: DataFrame containing processed orders
            validation_summary: Validation results summary
            email_stats: Email service statistics
            output_dir: Output directory for reports
            
        Returns:
            List of generated report file paths
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        all_files = []
        
        try:
            self.logger.info(f"Generating comprehensive steel industry reports to {output_dir}")
            
            # Generate individual reports
            reports = {
                'order_summary': self.generate_order_summary(orders_data),
                'production_metrics': self.generate_production_metrics(orders_data),
                'quality_analysis': self.generate_quality_analysis(orders_data),
                'customer_analytics': self.generate_customer_analytics(orders_data)
            }
            
            # Add system performance data
            reports['system_performance'] = {
                'timestamp': datetime.now().isoformat(),
                'validation_summary': validation_summary,
                'email_statistics': email_stats,
                'data_processing': {
                    'total_orders_processed': len(orders_data),
                    'processing_date': timestamp
                }
            }
            
            # Save individual reports
            for report_name, report_data in reports.items():
                filename = f"steel_{report_name}_{timestamp}"
                files = self.save_report(report_data, filename, output_dir)
                all_files.extend(files)
            
            # Create comprehensive summary report
            comprehensive_summary = {
                'report_metadata': {
                    'generated_at': datetime.now().isoformat(),
                    'system_name': 'Steel Industry Automation System',
                    'version': '1.0.0'
                },
                'executive_summary': {
                    'total_orders': len(orders_data),
                    'total_value': float(orders_data['TotalPrice'].sum()),
                    'average_order_value': float(orders_data['TotalPrice'].mean()),
                    'completion_rate': len(orders_data[orders_data['Status'].isin(['Ready', 'Shipped', 'Delivered'])]) / len(orders_data) * 100,
                    'quality_rate': len(orders_data[orders_data['QualityGrade'].isin(['A', 'B'])]) / len(orders_data) * 100
                },
                'detailed_reports': reports
            }
            
            summary_files = self.save_report(
                comprehensive_summary, 
                f"steel_automation_summary_{timestamp}", 
                output_dir
            )
            all_files.extend(summary_files)
            
            self.logger.info(f"Generated {len(all_files)} report files")
            return all_files
            
        except Exception as e:
            self.logger.error(f"Error generating steel reports: {e}")
            raise
