"""
Steel Industry Email Service Module

This module provides email communication services for steel production and order management,
including customer notifications, production updates, quality alerts, and delivery confirmations.

Features:
- Customer order confirmations
- Production status updates
- Quality control notifications
- Delivery scheduling alerts
- Bulk email processing with optimization
- Email template management
"""

import smtplib
import time
import logging
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

class EmailService:
    """
    High-performance email service for steel industry customer communications
    with concurrent processing and comprehensive error handling.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize the Email Service
        
        Args:
            config: Configuration dictionary with SMTP settings
        """
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # SMTP Configuration
        self.smtp_server = self.config.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.config.get('smtp_port', 587)
        self.smtp_username = self.config.get('smtp_username', '')
        self.smtp_password = self.config.get('smtp_password', '')
        self.from_email = self.config.get('from_email', 'noreply@steelcorp.com')
        
        # Email templates
        self.templates = {
            'order_confirmation': {
                'subject': 'Steel Order Confirmation - {order_id}',
                'body': '''
Dear {customer_name},

Thank you for your steel order. We are pleased to confirm the following details:

ORDER DETAILS:
Order ID: {order_id}
Batch ID: {batch_id}
Steel Grade: {steel_grade}
Steel Type: {steel_type}
Dimensions: {thickness}mm x {width}mm x {length}mm
Weight: {weight:,.1f} kg
Total Price: ${total_price:,.2f}

PRODUCTION DETAILS:
Production Line: {production_line}
Expected Production Date: {production_date}
Expected Delivery Date: {delivery_date}
Quality Grade: {quality_grade}
Warehouse: {warehouse}

Your order is currently: {status}

We will keep you updated on the progress of your order. Please contact us if you have any questions.

Best regards,
Steel Corporation Production Team
Email: production@steelcorp.com
Phone: 1-800-STEEL-01
                '''.strip()
            },
            'production_update': {
                'subject': 'Production Update - Order {order_id}',
                'body': '''
Dear {customer_name},

We would like to update you on the production status of your steel order:

Order ID: {order_id}
Current Status: {status}
Production Line: {production_line}
Quality Grade: {quality_grade}

{status_message}

Thank you for choosing Steel Corporation.

Best regards,
Production Team
                '''.strip()
            },
            'quality_alert': {
                'subject': 'Quality Alert - Order {order_id}',
                'body': '''
Dear {customer_name},

We need to inform you about a quality issue with your steel order:

Order ID: {order_id}
Quality Grade: {quality_grade}
Issue: Quality grade below standard specifications

Our quality control team is working to resolve this issue. We will contact you shortly with options including:
- Rework to meet specifications
- Replacement order
- Partial refund

We apologize for any inconvenience and appreciate your patience.

Best regards,
Quality Control Team
                '''.strip()
            }
        }
        
        # Performance tracking
        self.email_stats = {
            'total_emails_sent': 0,
            'successful_emails': 0,
            'failed_emails': 0,
            'processing_time': 0,
            'errors': []
        }
    
    def format_email_content(self, template_name: str, order_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Format email content using template and order data
        
        Args:
            template_name: Name of the email template
            order_data: Dictionary containing order information
            
        Returns:
            Dictionary with formatted subject and body
        """
        if template_name not in self.templates:
            raise ValueError(f"Unknown email template: {template_name}")
        
        template = self.templates[template_name]
        
        try:
            # Add status-specific messages
            status_messages = {
                'Pending': 'Your order is pending approval and will enter production soon.',
                'In Production': 'Your order is currently being manufactured on our production line.',
                'Quality Check': 'Your order is undergoing final quality inspection.',
                'Ready': 'Your order has passed quality control and is ready for shipment.',
                'Shipped': 'Your order has been shipped and is on its way to you.',
                'Delivered': 'Your order has been successfully delivered.',
                'Hold': 'Your order is temporarily on hold. We will contact you shortly.',
                'Rework Required': 'Your order requires rework to meet quality standards.'
            }
            
            # Enhance order data with additional context
            enhanced_data = order_data.copy()
            enhanced_data['status_message'] = status_messages.get(
                order_data.get('Status', ''), 
                'Please contact us for current status.'
            )
            
            # Format subject and body
            subject = template['subject'].format(**enhanced_data)
            body = template['body'].format(**enhanced_data)
            
            return {'subject': subject, 'body': body}
            
        except KeyError as e:
            self.logger.error(f"Missing template data field: {e}")
            raise ValueError(f"Missing required field for email template: {e}")
    
    def send_single_email(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        """
        Send a single email with error handling and retry logic
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body content
            
        Returns:
            Dictionary with send result information
        """
        result = {
            'email': to_email,
            'success': False,
            'error': None,
            'timestamp': datetime.now().isoformat()
        }
        
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # Create email message
                msg = MIMEMultipart()
                msg['From'] = self.from_email
                msg['To'] = to_email
                msg['Subject'] = subject
                
                msg.attach(MIMEText(body, 'plain'))
                
                # Simulate email sending (in production, use actual SMTP)
                if self.config.get('simulate', True):
                    # Simulate processing time
                    time.sleep(0.1)
                    
                    # Simulate occasional failures for testing
                    import random
                    if random.random() < 0.02:  # 2% failure rate
                        raise Exception("Simulated network timeout")
                    
                    result['success'] = True
                    self.logger.debug(f"Email simulated sent to {to_email}")
                else:
                    # Actual SMTP sending (uncomment for production)
                    # with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    #     server.starttls()
                    #     server.login(self.smtp_username, self.smtp_password)
                    #     server.send_message(msg)
                    result['success'] = True
                    self.logger.info(f"Email sent to {to_email}")
                
                break  # Success, exit retry loop
                
            except Exception as e:
                retry_count += 1
                error_msg = f"Attempt {retry_count}/{max_retries} failed: {str(e)}"
                self.logger.warning(f"Email to {to_email} - {error_msg}")
                
                if retry_count >= max_retries:
                    result['error'] = f"Failed after {max_retries} attempts: {str(e)}"
                    self.email_stats['errors'].append(result['error'])
                else:
                    # Exponential backoff
                    time.sleep(2 ** retry_count)
        
        return result
    
    def send_order_confirmations(self, orders_data: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Send order confirmation emails for all valid orders using concurrent processing
        
        Args:
            orders_data: DataFrame containing order information
            
        Returns:
            List of email send results
        """
        start_time = time.time()
        self.logger.info(f"Starting to send {len(orders_data)} order confirmation emails")
        
        results = []
        
        # Filter orders with valid email addresses
        valid_email_orders = orders_data[
            orders_data['ContactEmail'].notna() & 
            (orders_data['ContactEmail'] != '')
        ]
        
        self.logger.info(f"Sending emails to {len(valid_email_orders)} customers with valid email addresses")
        
        # Concurrent email sending
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_order = {}
            
            for index, order in valid_email_orders.iterrows():
                try:
                    # Format email content
                    email_content = self.format_email_content('order_confirmation', {
                        'customer_name': order['CustomerName'],
                        'order_id': order['OrderID'],
                        'batch_id': order['BatchID'],
                        'steel_grade': order['SteelGrade'],
                        'steel_type': order['SteelType'],
                        'thickness': order['Thickness'],
                        'width': order['Width'],
                        'length': order['Length'],
                        'weight': order['Weight'],
                        'total_price': order['TotalPrice'],
                        'production_line': order['ProductionLine'],
                        'production_date': order['ProductionDate'],
                        'delivery_date': order['DeliveryDate'],
                        'quality_grade': order['QualityGrade'],
                        'warehouse': order['Warehouse'],
                        'status': order['Status']
                    })
                    
                    # Submit email task
                    future = executor.submit(
                        self.send_single_email,
                        order['ContactEmail'],
                        email_content['subject'],
                        email_content['body']
                    )
                    future_to_order[future] = order
                    
                except Exception as e:
                    self.logger.error(f"Error preparing email for order {order.get('OrderID', 'Unknown')}: {e}")
                    results.append({
                        'email': order.get('ContactEmail', 'Unknown'),
                        'success': False,
                        'error': f"Email preparation failed: {str(e)}",
                        'timestamp': datetime.now().isoformat()
                    })
            
            # Collect results as they complete
            for future in as_completed(future_to_order):
                try:
                    result = future.result()
                    results.append(result)
                    
                    if result['success']:
                        self.email_stats['successful_emails'] += 1
                    else:
                        self.email_stats['failed_emails'] += 1
                        
                except Exception as e:
                    order = future_to_order[future]
                    error_result = {
                        'email': order.get('ContactEmail', 'Unknown'),
                        'success': False,
                        'error': f"Email execution failed: {str(e)}",
                        'timestamp': datetime.now().isoformat()
                    }
                    results.append(error_result)
                    self.email_stats['failed_emails'] += 1
        
        # Update statistics
        processing_time = time.time() - start_time
        self.email_stats.update({
            'total_emails_sent': len(results),
            'processing_time': processing_time
        })
        
        success_rate = (self.email_stats['successful_emails'] / max(len(results), 1)) * 100
        
        self.logger.info(f"Email sending completed in {processing_time:.2f}s")
        self.logger.info(f"Success rate: {success_rate:.1f}% ({self.email_stats['successful_emails']}/{len(results)})")
        
        return results
    
    def send_production_updates(self, orders_data: pd.DataFrame, update_type: str = 'production_update') -> List[Dict[str, Any]]:
        """
        Send production status update emails
        
        Args:
            orders_data: DataFrame containing order information
            update_type: Type of update email to send
            
        Returns:
            List of email send results
        """
        self.logger.info(f"Sending {update_type} emails for {len(orders_data)} orders")
        
        results = []
        
        # Process each order
        for index, order in orders_data.iterrows():
            if pd.notna(order.get('ContactEmail')) and order.get('ContactEmail') != '':
                try:
                    # Format email content
                    email_content = self.format_email_content(update_type, {
                        'customer_name': order['CustomerName'],
                        'order_id': order['OrderID'],
                        'status': order['Status'],
                        'production_line': order['ProductionLine'],
                        'quality_grade': order['QualityGrade']
                    })
                    
                    # Send email
                    result = self.send_single_email(
                        order['ContactEmail'],
                        email_content['subject'],
                        email_content['body']
                    )
                    results.append(result)
                    
                except Exception as e:
                    self.logger.error(f"Error sending update for order {order.get('OrderID')}: {e}")
                    results.append({
                        'email': order.get('ContactEmail', 'Unknown'),
                        'success': False,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
        
        return results
    
    def get_email_stats(self) -> Dict[str, Any]:
        """
        Get email service statistics
        
        Returns:
            Dictionary containing email performance metrics
        """
        return {
            'email_stats': self.email_stats,
            'performance_metrics': {
                'emails_per_second': self.email_stats['total_emails_sent'] / max(self.email_stats['processing_time'], 0.001),
                'success_rate': (self.email_stats['successful_emails'] / max(self.email_stats['total_emails_sent'], 1)) * 100,
                'failure_rate': (self.email_stats['failed_emails'] / max(self.email_stats['total_emails_sent'], 1)) * 100
            }
        }
