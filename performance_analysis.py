#!/usr/bin/env python3
"""
Performance analysis tool for comparing original vs optimized automation.
"""

import subprocess
import time
import psutil
import json
import pandas as pd
import os
from datetime import datetime

def run_performance_comparison():
    """Run both versions and compare performance metrics."""
    
    print("🔬 PERFORMANCE ANALYSIS STARTING...")
    print("="*60)
    
    # Test data for comparison
    results = {
        'original_fixed': {},
        'optimized': {},
        'comparison': {}
    }
    
    # Get Python executable path
    python_path = "/Users/muhammadhassannaeem/Desktop/ConcordiaUniversity/LR-Robotic Process Automation/Fourth Assignment/RPA-Automation-Week-4/.venv/bin/python"
    
    print("🐌 Running ORIGINAL (Fixed) version...")
    start_time = time.time()
    start_memory = psutil.virtual_memory().used / 1024 / 1024
    
    try:
        result = subprocess.run([python_path, "main.py"], 
                              capture_output=True, text=True, timeout=600)
        end_time = time.time()
        end_memory = psutil.virtual_memory().used / 1024 / 1024
        
        results['original_fixed'] = {
            'runtime': end_time - start_time,
            'memory_change': end_memory - start_memory,
            'success': result.returncode == 0,
            'output_lines': len(result.stdout.split('\n'))
        }
        
        # Parse log for more details
        if os.path.exists('automation.log'):
            with open('automation.log', 'r') as f:
                log_content = f.read()
                # Extract metrics from log
                for line in log_content.split('\n'):
                    if 'Total runtime:' in line:
                        runtime = float(line.split(':')[1].strip().split()[0])
                        results['original_fixed']['logged_runtime'] = runtime
                    elif 'Records processed:' in line:
                        records = int(line.split(':')[1].strip())
                        results['original_fixed']['records_processed'] = records
                    elif 'Confirmations sent:' in line:
                        confirmations = int(line.split(':')[1].strip())
                        results['original_fixed']['confirmations_sent'] = confirmations
        
        print(f"   ✅ Completed in {results['original_fixed']['runtime']:.2f}s")
        
    except subprocess.TimeoutExpired:
        print("   ❌ Original version timed out (>10 minutes)")
        results['original_fixed']['runtime'] = 600
        results['original_fixed']['success'] = False
    except Exception as e:
        print(f"   ❌ Original version failed: {e}")
        results['original_fixed']['success'] = False
    
    print("\n🚀 Running OPTIMIZED version...")
    start_time = time.time()
    start_memory = psutil.virtual_memory().used / 1024 / 1024
    
    try:
        result = subprocess.run([python_path, "main_optimized.py"], 
                              capture_output=True, text=True, timeout=600)
        end_time = time.time()
        end_memory = psutil.virtual_memory().used / 1024 / 1024
        
        results['optimized'] = {
            'runtime': end_time - start_time,
            'memory_change': end_memory - start_memory,
            'success': result.returncode == 0,
            'output_lines': len(result.stdout.split('\n'))
        }
        
        # Parse log for more details
        if os.path.exists('automation_optimized.log'):
            with open('automation_optimized.log', 'r') as f:
                log_content = f.read()
                for line in log_content.split('\n'):
                    if 'Total runtime:' in line:
                        runtime = float(line.split(':')[1].strip().split()[0])
                        results['optimized']['logged_runtime'] = runtime
                    elif 'Records processed:' in line:
                        records = int(line.split(':')[1].strip())
                        results['optimized']['records_processed'] = records
                    elif 'Confirmations sent:' in line:
                        confirmations = int(line.split(':')[1].strip())
                        results['optimized']['confirmations_sent'] = confirmations
                    elif 'Processing rate:' in line:
                        rate = float(line.split(':')[1].strip().split()[0])
                        results['optimized']['processing_rate'] = rate
        
        print(f"   ✅ Completed in {results['optimized']['runtime']:.2f}s")
        
    except Exception as e:
        print(f"   ❌ Optimized version failed: {e}")
        results['optimized']['success'] = False
    
    # Calculate comparison metrics
    if results['original_fixed'].get('success') and results['optimized'].get('success'):
        orig_runtime = results['original_fixed'].get('logged_runtime', results['original_fixed']['runtime'])
        opt_runtime = results['optimized'].get('logged_runtime', results['optimized']['runtime'])
        
        results['comparison'] = {
            'runtime_improvement': ((orig_runtime - opt_runtime) / orig_runtime) * 100,
            'speed_multiplier': orig_runtime / opt_runtime,
            'orig_records_per_sec': results['original_fixed'].get('records_processed', 0) / orig_runtime,
            'opt_records_per_sec': results['optimized'].get('processing_rate', 0)
        }
    
    # Generate report
    generate_performance_report(results)
    
    return results

def generate_performance_report(results):
    """Generate a comprehensive performance report."""
    
    print("\n📊 PERFORMANCE COMPARISON REPORT")
    print("="*60)
    
    if not results['original_fixed'].get('success') or not results['optimized'].get('success'):
        print("❌ Cannot generate comparison - one or both versions failed")
        return
    
    # Runtime comparison
    orig_runtime = results['original_fixed'].get('logged_runtime', results['original_fixed']['runtime'])
    opt_runtime = results['optimized'].get('logged_runtime', results['optimized']['runtime'])
    improvement = results['comparison']['runtime_improvement']
    speed_mult = results['comparison']['speed_multiplier']
    
    print(f"⏱️  RUNTIME COMPARISON:")
    print(f"   Original (Fixed): {orig_runtime:.2f} seconds")
    print(f"   Optimized:        {opt_runtime:.2f} seconds")
    print(f"   Improvement:      {improvement:.1f}% faster")
    print(f"   Speed multiplier: {speed_mult:.1f}x")
    
    # Throughput comparison
    orig_rate = results['comparison']['orig_records_per_sec']
    opt_rate = results['comparison']['opt_records_per_sec']
    
    print(f"\n📈 THROUGHPUT COMPARISON:")
    print(f"   Original: {orig_rate:.2f} records/second")
    print(f"   Optimized: {opt_rate:.2f} records/second")
    print(f"   Improvement: {(opt_rate/orig_rate):.1f}x faster processing")
    
    # Records processed
    orig_records = results['original_fixed'].get('records_processed', 0)
    opt_records = results['optimized'].get('records_processed', 0)
    
    print(f"\n📋 DATA PROCESSING:")
    print(f"   Original processed: {orig_records} records")
    print(f"   Optimized processed: {opt_records} records")
    print(f"   Data consistency: {'✅ Same' if orig_records == opt_records else '⚠️  Different'}")
    
    # Email confirmations
    orig_emails = results['original_fixed'].get('confirmations_sent', 0)
    opt_emails = results['optimized'].get('confirmations_sent', 0)
    
    print(f"\n📧 EMAIL CONFIRMATIONS:")
    print(f"   Original sent: {orig_emails} emails")
    print(f"   Optimized sent: {opt_emails} emails")
    print(f"   Email consistency: {'✅ Similar' if abs(orig_emails - opt_emails) <= 5 else '⚠️  Different'}")
    
    # Save detailed report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_data = {
        'timestamp': timestamp,
        'performance_metrics': results,
        'summary': {
            'runtime_improvement_percent': improvement,
            'speed_multiplier': speed_mult,
            'throughput_improvement': opt_rate / orig_rate if orig_rate > 0 else 0,
            'data_consistency': orig_records == opt_records,
            'email_consistency': abs(orig_emails - opt_emails) <= 5
        }
    }
    
    # Save as JSON
    with open(f'reports/performance_analysis_{timestamp}.json', 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n💾 Detailed report saved: reports/performance_analysis_{timestamp}.json")
    print("\n🎉 PERFORMANCE ANALYSIS COMPLETE!")

if __name__ == "__main__":
    # Ensure reports directory exists
    os.makedirs('reports', exist_ok=True)
    
    # Run the comparison
    run_performance_comparison()
