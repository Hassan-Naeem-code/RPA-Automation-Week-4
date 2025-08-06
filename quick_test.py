#!/usr/bin/env python3
"""
Quick Steel Automation Test - Minimal Version
"""

import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def quick_test():
    print("=== QUICK STEEL AUTOMATION TEST ===")
    
    try:
        # Test basic imports
        print("1. Testing imports...")
        from steel_automation.core.data_processor import SteelDataProcessor
        from steel_automation.core.validation import SteelDataValidator
        print("   ✓ Core modules imported successfully")
        
        # Test basic data processing
        print("2. Testing data processing...")
        processor = SteelDataProcessor()
        data = processor.process_steel_orders('data/steel_orders.csv')
        print(f"   ✓ Processed {len(data)} steel orders")
        
        # Test validation (limit output)
        print("3. Testing validation...")
        validator = SteelDataValidator()
        # Just validate first 10 records to limit warnings
        sample_data = data.head(10)
        validated = validator.validate_steel_orders(sample_data)
        print(f"   ✓ Validated {len(validated)} orders (sample)")
        
        print("\n=== TEST COMPLETED SUCCESSFULLY ===")
        print(f"Total orders in dataset: {len(data)}")
        print(f"Sample validation rate: {len(validated)/len(sample_data)*100:.1f}%")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
