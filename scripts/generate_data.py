#!/usr/bin/env python3
"""
Flight Reservation Data Generator
Creates synthetic flight reservation data with intentional edge cases for testing automation workflows.
"""

import pandas as pd
import random
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import os

# Create 200 fake flight reservations with fields: PNR, Passenger, Origin, Destination, Fare, Status
def generate_flight_reservations(num_records=200):
    """
    Generate synthetic flight reservation data with realistic structures and intentional edge cases.
    
    Returns:
        pandas.DataFrame: Generated flight reservation data
    """
    fake = Faker()
    Faker.seed(42)  # For reproducible results
    random.seed(42)
    
    # Common airport codes for realistic data
    major_airports = [
        'LAX', 'JFK', 'ORD', 'DFW', 'DEN', 'ATL', 'SFO', 'SEA', 'LAS', 'MCO',
        'EWR', 'CLT', 'PHX', 'IAH', 'MIA', 'BOS', 'MSP', 'FLL', 'DTW', 'PHL',
        'LGA', 'BWI', 'MDW', 'TPA', 'IAD', 'SAN', 'HNL', 'PDX', 'STL', 'AUS'
    ]
    
    # Status options
    status_options = ['Confirmed', 'Cancelled', 'Pending', 'Checked-in', 'Completed']
    
    reservations = []
    
    for i in range(num_records):
        # Generate base data
        pnr = fake.bothify(text='??###?', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        passenger = fake.name()
        origin = random.choice(major_airports)
        destination = random.choice([apt for apt in major_airports if apt != origin])
        
        # Generate fare with some variance
        base_fare = random.uniform(150, 2500)
        fare = round(base_fare, 2)
        
        status = random.choice(status_options)
        
        # Create booking date (within last 6 months)
        booking_date = fake.date_between(start_date='-6m', end_date='today')
        
        # Travel date (future dates mostly, some past)
        if random.random() < 0.8:  # 80% future travels
            travel_date = fake.date_between(start_date='today', end_date='+3m')
        else:  # 20% past travels
            travel_date = fake.date_between(start_date='-1m', end_date='today')
        
        reservation = {
            'PNR': pnr,
            'Passenger': passenger,
            'Origin': origin,
            'Destination': destination,
            'Fare': fare,
            'Status': status,
            'BookingDate': booking_date,
            'TravelDate': travel_date,
            'Email': fake.email(),
            'Phone': fake.phone_number()
        }
        
        reservations.append(reservation)
    
    return pd.DataFrame(reservations)

def introduce_edge_cases(df):
    """
    Intentionally introduce edge cases and data quality issues for testing.
    
    Args:
        df (pandas.DataFrame): Clean flight reservation data
        
    Returns:
        pandas.DataFrame: Data with intentional edge cases
    """
    df_copy = df.copy()
    
    # 1. Missing values (5% of records)
    missing_indices = random.sample(range(len(df_copy)), k=int(0.05 * len(df_copy)))
    for idx in missing_indices:
        if random.random() < 0.5:
            df_copy.loc[idx, 'Email'] = np.nan
        else:
            df_copy.loc[idx, 'Phone'] = np.nan
    
    # 2. Missing fare values (2% of records)
    fare_missing_indices = random.sample(range(len(df_copy)), k=int(0.02 * len(df_copy)))
    for idx in fare_missing_indices:
        df_copy.loc[idx, 'Fare'] = np.nan
    
    # 3. Duplicate records (create 5 exact duplicates)
    duplicate_indices = random.sample(range(len(df_copy)), k=5)
    duplicates = df_copy.iloc[duplicate_indices].copy()
    df_copy = pd.concat([df_copy, duplicates], ignore_index=True)
    
    # 4. Invalid airport codes (3% of records)
    invalid_airport_indices = random.sample(range(len(df_copy)), k=int(0.03 * len(df_copy)))
    invalid_codes = ['XXX', 'ZZZ', 'ABC', 'DEF', '123']
    for idx in invalid_airport_indices:
        if random.random() < 0.5:
            df_copy.loc[idx, 'Origin'] = random.choice(invalid_codes)
        else:
            df_copy.loc[idx, 'Destination'] = random.choice(invalid_codes)
    
    # 5. Incorrect data types in Fare column (convert some to strings)
    string_fare_indices = random.sample(range(len(df_copy)), k=int(0.03 * len(df_copy)))
    for idx in string_fare_indices:
        if not pd.isna(df_copy.loc[idx, 'Fare']):
            df_copy.loc[idx, 'Fare'] = f"${df_copy.loc[idx, 'Fare']}"
    
    # 6. Invalid status values
    invalid_status_indices = random.sample(range(len(df_copy)), k=3)
    invalid_statuses = ['Unknown', 'Error', 'Processing']
    for idx in invalid_status_indices:
        df_copy.loc[idx, 'Status'] = random.choice(invalid_statuses)
    
    # 7. Same origin and destination (logical error)
    same_city_indices = random.sample(range(len(df_copy)), k=2)
    for idx in same_city_indices:
        df_copy.loc[idx, 'Destination'] = df_copy.loc[idx, 'Origin']
    
    # 8. Negative or zero fares
    negative_fare_indices = random.sample([i for i in range(len(df_copy)) 
                                         if isinstance(df_copy.loc[i, 'Fare'], (int, float))], k=2)
    for idx in negative_fare_indices:
        df_copy.loc[idx, 'Fare'] = random.choice([-50.0, 0.0, -100.25])
    
    return df_copy

def main():
    """Main function to generate and save flight reservation data."""
    print("Generating synthetic flight reservation data...")
    
    # Generate clean data
    df_clean = generate_flight_reservations(200)
    print(f"Generated {len(df_clean)} clean records")
    
    # Introduce edge cases
    df_with_issues = introduce_edge_cases(df_clean)
    print(f"Final dataset has {len(df_with_issues)} records (including duplicates)")
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'reservations.csv')
    df_with_issues.to_csv(output_path, index=False)
    print(f"Data saved to: {output_path}")
    
    # Print summary statistics
    print("\n=== DATA SUMMARY ===")
    print(f"Total records: {len(df_with_issues)}")
    print(f"Columns: {list(df_with_issues.columns)}")
    print(f"Missing values per column:")
    print(df_with_issues.isnull().sum())
    print(f"\nUnique statuses: {df_with_issues['Status'].unique()}")
    print(f"Fare data types: {df_with_issues['Fare'].apply(type).value_counts()}")
    
    # Check for edge cases
    print("\n=== EDGE CASES INTRODUCED ===")
    print(f"Records with missing emails: {df_with_issues['Email'].isnull().sum()}")
    print(f"Records with missing phones: {df_with_issues['Phone'].isnull().sum()}")
    print(f"Records with missing fares: {df_with_issues['Fare'].isnull().sum()}")
    print(f"Duplicate PNRs: {df_with_issues['PNR'].duplicated().sum()}")
    
    # Check for same origin/destination
    same_origin_dest = (df_with_issues['Origin'] == df_with_issues['Destination']).sum()
    print(f"Records with same origin and destination: {same_origin_dest}")
    
    print("\nData generation complete!")

if __name__ == "__main__":
    main()
