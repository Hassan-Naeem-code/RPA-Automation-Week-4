"""
Email confirmation service for flight reservations.
Contains synchronous processing that should be optimized.
"""

import logging
import time
import random
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)

class EmailConfirmationService:
    """Send email confirmations with intentional performance issues."""
    
    def __init__(self):
        self.smtp_config = {
            'server': 'smtp.example.com',
            'port': 587,
            'username': 'automation@company.com',
            'password': 'secure_password'
        }
        self.success_rate = 0.85  # Simulate 85% success rate
        self.max_workers = 5
    
    def send_confirmations(self, reservations_data):
        """
        Send confirmation emails.
        Bug: Synchronous processing - should be async/batched.
        """
        logger.info(f"Sending confirmations for {len(reservations_data)} reservations")
        results = []
        
        # Bug 1: Processing emails one by one instead of in batches
        for index, reservation in reservations_data.iterrows():
            try:
                result = self._send_single_confirmation(reservation)
                results.append(result)
                
                # Bug 2: Fixed delay between emails (inefficient)
                time.sleep(0.1)  # 100ms delay per email
                
            except Exception as e:
                logger.error(f"Failed to send confirmation for PNR {reservation.get('PNR')}: {str(e)}")
                results.append({
                    'PNR': reservation.get('PNR'),
                    'status': 'failed',
                    'error': str(e),
                    'timestamp': time.time()
                })
        
        logger.info(f"Completed email sending: {sum(1 for r in results if r['status'] == 'sent')} sent, "
                   f"{sum(1 for r in results if r['status'] == 'failed')} failed")
        
        return results
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _send_single_confirmation(self, reservation):
        """
        Send a single confirmation email with retry logic.
        """
        # Simulate email sending with random failures
        processing_time = random.uniform(0.05, 0.3)  # 50-300ms
        time.sleep(processing_time)
        
        # Simulate random failures
        if random.random() > self.success_rate:
            raise Exception("SMTP connection failed")
        
        # Bug 3: Not checking if email address is valid before sending
        email = reservation.get('Email')
        if not email or pd.isna(email):
            raise Exception("No email address provided")
        
        # Simulate successful email sending
        confirmation_data = {
            'PNR': reservation.get('PNR'),
            'passenger': reservation.get('Passenger'),
            'email': email,
            'origin': reservation.get('Origin'),
            'destination': reservation.get('Destination'),
            'fare': reservation.get('Fare'),
            'status': reservation.get('Status')
        }
        
        # Log the email (in real implementation, this would send actual email)
        logger.debug(f"Email sent to {email} for PNR {reservation.get('PNR')}")
        
        return {
            'PNR': reservation.get('PNR'),
            'email': email,
            'status': 'sent',
            'timestamp': time.time(),
            'processing_time': processing_time
        }
    
    def send_confirmations_optimized(self, reservations_data, batch_size=10):
        """
        Optimized version with concurrent processing.
        This method will be implemented during optimization phase.
        """
        logger.info(f"Sending confirmations in optimized mode for {len(reservations_data)} reservations")
        results = []
        
        # Process in batches with concurrent execution
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_reservation = {}
            
            for index, reservation in reservations_data.iterrows():
                # Skip records without valid email
                if pd.isna(reservation.get('Email')):
                    results.append({
                        'PNR': reservation.get('PNR'),
                        'status': 'skipped',
                        'error': 'No email address',
                        'timestamp': time.time()
                    })
                    continue
                
                future = executor.submit(self._send_single_confirmation_optimized, reservation)
                future_to_reservation[future] = reservation
            
            # Collect results as they complete
            for future in as_completed(future_to_reservation):
                reservation = future_to_reservation[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Failed to send confirmation for PNR {reservation.get('PNR')}: {str(e)}")
                    results.append({
                        'PNR': reservation.get('PNR'),
                        'status': 'failed',
                        'error': str(e),
                        'timestamp': time.time()
                    })
        
        success_count = sum(1 for r in results if r['status'] == 'sent')
        failed_count = sum(1 for r in results if r['status'] == 'failed')
        skipped_count = sum(1 for r in results if r['status'] == 'skipped')
        
        logger.info(f"Optimized email sending completed: {success_count} sent, "
                   f"{failed_count} failed, {skipped_count} skipped")
        
        return results
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def _send_single_confirmation_optimized(self, reservation):
        """Optimized version of single email sending."""
        # Simulate faster email sending
        processing_time = random.uniform(0.02, 0.1)  # 20-100ms (faster)
        time.sleep(processing_time)
        
        # Simulate random failures (slightly better success rate for optimized version)
        if random.random() > 0.9:  # 90% success rate
            raise Exception("SMTP connection failed")
        
        email = reservation.get('Email')
        
        logger.debug(f"Optimized email sent to {email} for PNR {reservation.get('PNR')}")
        
        return {
            'PNR': reservation.get('PNR'),
            'email': email,
            'status': 'sent',
            'timestamp': time.time(),
            'processing_time': processing_time
        }
