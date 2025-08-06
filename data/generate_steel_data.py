#!/usr/bin/env python3
"""
Steel Industry Data Generator
Generates synthetic steel production and inventory data for automation testing.
"""

import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

# Set seed for reproducible data
fake = Faker()
Faker.seed(42)
np.random.seed(42)
random.seed(42)

# Steel industry specific data
STEEL_GRADES = [
    'A36', 'A572-50', 'A992', 'A514', 'A588', 'A242', 'A709-50',
    'S355', 'S275', 'S235', 'S420', 'S460', 'Q235', 'Q345',
    '304SS', '316SS', '409SS', '430SS', '201SS'
]

STEEL_TYPES = [
    'Hot Rolled', 'Cold Rolled', 'Galvanized', 'Stainless Steel',
    'Carbon Steel', 'Alloy Steel', 'Tool Steel', 'Spring Steel'
]

PRODUCTION_LINES = [
    'Line-A1', 'Line-A2', 'Line-B1', 'Line-B2', 'Line-C1', 'Line-C2',
    'Line-D1', 'Line-D2', 'Line-E1', 'Line-E2'
]

WAREHOUSES = [
    'WH-North', 'WH-South', 'WH-East', 'WH-West', 'WH-Central',
    'WH-Export', 'WH-Domestic', 'WH-Reserve'
]

ORDER_STATUS = [
    'Pending', 'In Production', 'Quality Check', 'Ready', 'Shipped',
    'Delivered', 'Cancelled', 'Hold', 'Rework Required'
]

QUALITY_GRADES = ['A', 'B', 'C', 'Reject', 'Rework']

THICKNESS_RANGES = {
    'Thin': (0.5, 3.0),
    'Medium': (3.0, 12.0),
    'Thick': (12.0, 50.0),
    'Heavy': (50.0, 200.0)
}

def generate_steel_order_id():
    """Generate steel order ID in format SO-YYYY-NNNN"""
    year = random.choice([2024, 2025])
    number = random.randint(1000, 9999)
    return f"SO-{year}-{number}"

def generate_batch_id():
    """Generate batch ID in format B-NNNNNN"""
    return f"B-{random.randint(100000, 999999)}"

def generate_steel_dimensions():
    """Generate realistic steel dimensions"""
    thickness = round(random.uniform(0.5, 100.0), 2)
    width = round(random.uniform(1000, 3000), 0)  # mm
    length = round(random.uniform(6000, 18000), 0)  # mm
    return thickness, width, length

def generate_steel_weight(thickness, width, length):
    """Calculate approximate steel weight (kg) based on dimensions"""
    # Steel density ~7.85 kg/m³
    volume_m3 = (thickness/1000) * (width/1000) * (length/1000)
    weight = volume_m3 * 7850  # kg
    return round(weight, 2)

def generate_steel_records(num_records=200):
    """Generate synthetic steel industry records"""
    records = []
    
    for i in range(num_records):
        # Basic order info
        order_id = generate_steel_order_id()
        batch_id = generate_batch_id()
        
        # Steel specifications
        steel_grade = random.choice(STEEL_GRADES)
        steel_type = random.choice(STEEL_TYPES)
        thickness, width, length = generate_steel_dimensions()
        weight = generate_steel_weight(thickness, width, length)
        
        # Production details
        production_line = random.choice(PRODUCTION_LINES)
        warehouse = random.choice(WAREHOUSES)
        quality_grade = random.choice(QUALITY_GRADES)
        
        # Dates
        order_date = fake.date_between(start_date='-30d', end_date='today')
        production_date = order_date + timedelta(days=random.randint(1, 7))
        delivery_date = production_date + timedelta(days=random.randint(1, 14))
        
        # Status and pricing
        status = random.choice(ORDER_STATUS)
        unit_price = round(random.uniform(500, 2500), 2)  # USD per ton
        total_price = round((weight/1000) * unit_price, 2)
        
        # Customer info
        customer_name = fake.company()
        contact_email = fake.email()
        contact_phone = fake.phone_number()
        
        record = {
            'OrderID': order_id,
            'BatchID': batch_id,
            'CustomerName': customer_name,
            'SteelGrade': steel_grade,
            'SteelType': steel_type,
            'Thickness': thickness,
            'Width': width,
            'Length': length,
            'Weight': weight,
            'UnitPrice': unit_price,
            'TotalPrice': total_price,
            'ProductionLine': production_line,
            'Warehouse': warehouse,
            'QualityGrade': quality_grade,
            'Status': status,
            'OrderDate': order_date.strftime('%Y-%m-%d'),
            'ProductionDate': production_date.strftime('%Y-%m-%d'),
            'DeliveryDate': delivery_date.strftime('%Y-%m-%d'),
            'ContactEmail': contact_email,
            'ContactPhone': contact_phone
        }
        
        records.append(record)
    
    return pd.DataFrame(records)

def introduce_edge_cases(df):
    """Introduce intentional edge cases for testing automation robustness"""
    
    # 1. Missing values (4 missing emails, 6 missing phones, 4 missing prices)
    missing_email_indices = random.sample(range(len(df)), 4)
    missing_phone_indices = random.sample(range(len(df)), 6)
    missing_price_indices = random.sample(range(len(df)), 4)
    
    for idx in missing_email_indices:
        df.at[idx, 'ContactEmail'] = ''
    
    for idx in missing_phone_indices:
        df.at[idx, 'ContactPhone'] = ''
    
    for idx in missing_price_indices:
        df.at[idx, 'TotalPrice'] = ''
    
    # 2. String price values with currency symbols
    currency_indices = random.sample(range(len(df)), 6)
    for idx in currency_indices:
        if pd.notna(df.at[idx, 'TotalPrice']) and df.at[idx, 'TotalPrice'] != '':
            df.at[idx, 'TotalPrice'] = f"${df.at[idx, 'TotalPrice']}"
    
    # 3. Invalid steel grades and types
    invalid_grade_indices = random.sample(range(len(df)), 3)
    invalid_grades = ['XXX', 'ZZZ', 'ABC']
    for i, idx in enumerate(invalid_grade_indices):
        df.at[idx, 'SteelGrade'] = invalid_grades[i]
    
    # 4. Invalid production lines
    invalid_line_indices = random.sample(range(len(df)), 2)
    for idx in invalid_line_indices:
        df.at[idx, 'ProductionLine'] = 'LINE-XXX'
    
    # 5. Zero or negative values
    zero_weight_idx = random.choice(range(len(df)))
    negative_price_idx = random.choice(range(len(df)))
    
    df.at[zero_weight_idx, 'Weight'] = 0.0
    df.at[negative_price_idx, 'UnitPrice'] = -50.0
    
    # 6. Invalid status values
    invalid_status_indices = random.sample(range(len(df)), 3)
    invalid_statuses = ['Unknown', 'Error', 'Processing']
    for i, idx in enumerate(invalid_status_indices):
        df.at[idx, 'Status'] = invalid_statuses[i]
    
    # 7. Future dates (logical errors)
    future_date_idx = random.choice(range(len(df)))
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    df.at[future_date_idx, 'OrderDate'] = future_date
    
    # 8. Same order date and delivery date (logical error)
    same_date_idx = random.choice(range(len(df)))
    df.at[same_date_idx, 'DeliveryDate'] = df.at[same_date_idx, 'OrderDate']
    
    return df

def add_duplicates(df, num_duplicates=5):
    """Add duplicate records for testing deduplication"""
    duplicate_indices = random.sample(range(len(df)), num_duplicates)
    duplicates = df.iloc[duplicate_indices].copy()
    df_with_duplicates = pd.concat([df, duplicates], ignore_index=True)
    return df_with_duplicates

def main():
    """Generate the complete steel industry dataset"""
    print("Generating steel industry automation dataset...")
    
    # Generate base dataset
    df = generate_steel_records(200)
    print(f"Generated {len(df)} base steel production records")
    
    # Introduce edge cases
    df = introduce_edge_cases(df)
    print("Introduced intentional edge cases for testing")
    
    # Add duplicates
    df = add_duplicates(df, 5)
    print(f"Added duplicates. Final dataset: {len(df)} records")
    
    # Save to CSV
    output_file = 'data/steel_orders.csv'
    df.to_csv(output_file, index=False)
    print(f"Dataset saved to {output_file}")
    
    # Print summary statistics
    print("\n=== Dataset Summary ===")
    print(f"Total Records: {len(df)}")
    print(f"Unique Order IDs: {df['OrderID'].nunique()}")
    print(f"Steel Grades: {df['SteelGrade'].nunique()}")
    print(f"Production Lines: {df['ProductionLine'].nunique()}")
    print(f"Average Weight: {df['Weight'].mean():.2f} kg")
    
    # Calculate total value excluding non-numeric entries
    numeric_prices = pd.to_numeric(df['TotalPrice'].astype(str).str.replace('$', ''), errors='coerce')
    total_value = numeric_prices.sum()
    print(f"Total Value: ${total_value:,.2f}")
    
    print("\n=== Edge Cases Summary ===")
    print(f"Missing Emails: {df['ContactEmail'].isna().sum() + (df['ContactEmail'] == '').sum()}")
    print(f"Missing Phones: {df['ContactPhone'].isna().sum() + (df['ContactPhone'] == '').sum()}")
    print(f"Missing Prices: {df['TotalPrice'].isna().sum() + (df['TotalPrice'] == '').sum()}")
    print(f"String Prices: {df['TotalPrice'].astype(str).str.contains('\\$', na=False).sum()}")
    
    return df

if __name__ == "__main__":
    dataset = main()
