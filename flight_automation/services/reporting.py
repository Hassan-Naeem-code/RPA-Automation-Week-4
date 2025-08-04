"""
Reporting module for flight booking automation.
Generates summary reports and metrics.
"""

import pandas as pd
import logging
import os
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports for flight booking automation."""
    
    def __init__(self):
        self.report_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_summary_report(self, processed_data, confirmation_results):
        """
        Generate summary report from processed data and email results.
        Bug: Not handling cases where data might be empty or malformed.
        """
        logger.info("Generating summary report")
        
        # Bug 1: Not checking if inputs are valid
        if processed_data is None or confirmation_results is None:
            raise ValueError("Cannot generate report with empty data")
        
        # Process confirmation results
        confirmation_df = pd.DataFrame(confirmation_results)
        
        # Bug 2: Assuming specific column structure without validation
        total_reservations = len(processed_data)
        confirmed_emails = len(confirmation_df[confirmation_df['status'] == 'sent'])
        failed_emails = len(confirmation_df[confirmation_df['status'] == 'failed'])
        
        # Revenue calculations
        # Bug 3: Not handling non-numeric fare values
        total_revenue = processed_data['Fare'].sum()
        avg_fare = processed_data['Fare'].mean()
        
        # Status breakdown
        status_counts = processed_data['Status'].value_counts().to_dict()
        
        # Airport statistics
        origin_counts = processed_data['Origin'].value_counts().head(10).to_dict()
        destination_counts = processed_data['Destination'].value_counts().head(10).to_dict()
        
        # Bug 4: Not handling timezone issues in date calculations
        processing_summary = {
            'timestamp': self.report_timestamp,
            'total_reservations': total_reservations,
            'email_confirmations': {
                'sent': confirmed_emails,
                'failed': failed_emails,
                'success_rate': confirmed_emails / total_reservations if total_reservations > 0 else 0
            },
            'revenue_summary': {
                'total_revenue': float(total_revenue),
                'average_fare': float(avg_fare),
                'min_fare': float(processed_data['Fare'].min()),
                'max_fare': float(processed_data['Fare'].max())
            },
            'status_breakdown': status_counts,
            'top_origins': origin_counts,
            'top_destinations': destination_counts
        }
        
        return processing_summary
    
    def save_report(self, report_data, output_path):
        """
        Save report to file.
        Bug: Not creating directories if they don't exist.
        """
        logger.info(f"Saving report to {output_path}")
        
        # Bug 5: Not creating directory structure
        # This will fail if the 'reports' directory doesn't exist
        
        # Save as JSON
        json_path = output_path.replace('.csv', '.json')
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Create CSV version for easier analysis
        # Bug 6: Flattening nested data incorrectly
        flattened_data = []
        
        # Basic metrics
        flattened_data.append({
            'metric': 'Total Reservations',
            'value': report_data['total_reservations']
        })
        
        flattened_data.append({
            'metric': 'Emails Sent',
            'value': report_data['email_confirmations']['sent']
        })
        
        flattened_data.append({
            'metric': 'Emails Failed',
            'value': report_data['email_confirmations']['failed']
        })
        
        flattened_data.append({
            'metric': 'Email Success Rate',
            'value': report_data['email_confirmations']['success_rate']
        })
        
        flattened_data.append({
            'metric': 'Total Revenue',
            'value': report_data['revenue_summary']['total_revenue']
        })
        
        flattened_data.append({
            'metric': 'Average Fare',
            'value': report_data['revenue_summary']['average_fare']
        })
        
        # Status breakdown
        for status, count in report_data['status_breakdown'].items():
            flattened_data.append({
                'metric': f'Status: {status}',
                'value': count
            })
        
        # Top origins
        for airport, count in report_data['top_origins'].items():
            flattened_data.append({
                'metric': f'Top Origin: {airport}',
                'value': count
            })
        
        # Top destinations
        for airport, count in report_data['top_destinations'].items():
            flattened_data.append({
                'metric': f'Top Destination: {airport}',
                'value': count
            })
        
        # Save CSV
        df_report = pd.DataFrame(flattened_data)
        df_report.to_csv(output_path, index=False)
        
        logger.info(f"Report saved to {output_path} and {json_path}")
    
    def generate_detailed_report(self, processed_data, confirmation_results, validation_errors=None):
        """
        Generate a more detailed report including individual record analysis.
        This is the optimized version that will be implemented later.
        """
        logger.info("Generating detailed report")
        
        # Create reports directory if it doesn't exist
        os.makedirs('reports', exist_ok=True)
        
        # Individual reservation details
        confirmation_df = pd.DataFrame(confirmation_results)
        
        # Merge processed data with confirmation results
        detailed_data = processed_data.merge(
            confirmation_df[['PNR', 'status', 'processing_time']], 
            on='PNR', 
            how='left',
            suffixes=('', '_email')
        )
        
        # Add validation error information if available
        if validation_errors:
            error_df = pd.DataFrame(validation_errors)
            error_summary = error_df.groupby('row')['error'].apply(list).reset_index()
            error_summary.columns = ['row_index', 'validation_errors']
            detailed_data = detailed_data.merge(error_summary, left_index=True, right_on='row_index', how='left')
        
        # Save detailed CSV
        detailed_path = f"reports/detailed_report_{self.report_timestamp}.csv"
        detailed_data.to_csv(detailed_path, index=False)
        
        # Generate summary statistics
        summary = self.generate_summary_report(processed_data, confirmation_results)
        
        return summary, detailed_path
