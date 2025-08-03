# Flight Booking Automation - Troubleshooting Guide

## Data Assumptions

### Test Data Generation
Our synthetic dataset was created using the `generate_sample_data.py` script with the following characteristics:

- **Base Dataset**: 200 clean flight reservations
- **Final Dataset**: 205 records (including 5 intentional duplicates)
- **Fields**: PNR, Passenger, Origin, Destination, Fare, Status, BookingDate, TravelDate, Email, Phone

### Intentional Edge Cases Introduced

1. **Missing Values**: 
   - 4 missing email addresses
   - 6 missing phone numbers  
   - 4 missing fare values

2. **Data Type Issues**:
   - 6 fare values stored as strings with "$" prefix (e.g., "$2097.46")
   - Mixed data types in Fare column

3. **Logical Errors**:
   - 2 records with same origin and destination
   - 2 records with negative or zero fares

4. **Invalid Codes**:
   - ~3% invalid airport codes (XXX, ZZZ, ABC, etc.)
   - 3 invalid status values (Unknown, Error, Processing)

5. **Duplicates**: 5 exact duplicate records

## Error Analysis and Fixes

### Error 1: String Fare Conversion Failure
**Error**: `ValueError: could not convert string to float: '$697.06'`
**Root Cause**: The data processor tried to convert string fare values like "$697.06" directly to float without handling the "$" symbol.
**Location**: `src/data_processor.py:66` in `_process_single_reservation()`

**Fix Applied**: 
```python
# Before (buggy code)
if isinstance(fare, str):
    fare = float(fare)  # Fails for "$697.06"

# After (fixed code)
if isinstance(fare, str):
    try:
        fare = float(fare.replace('$', ''))
    except ValueError:
        fare = 0.0
```

**Git Commit**: `git commit -m "Fix: handle string fare values with currency symbols"`

### Error 2: Validation Not Filtering Invalid Records
**Error**: Invalid records were being included in processing despite validation errors
**Root Cause**: The `DataValidator.validate_reservations()` method identified errors but didn't filter out invalid records
**Location**: `src/validation.py:24`

**Fix Applied**:
```python
# Before (buggy code)
if errors:
    self.validation_errors.extend(errors)
    valid_records.append(row)  # Bug: Adding invalid records!

# After (fixed code)
if not errors:  # Only add records with NO errors
    valid_records.append(row)
else:
    self.validation_errors.extend(errors)
```

**Git Commit**: `git commit -m "Fix: filter out invalid records in validation"`

### Error 3: Missing Email Validation
**Error**: Email format was never validated despite having a validation method
**Root Cause**: `_validate_email()` method existed but was never called
**Location**: `src/validation.py:94`

**Fix Applied**: Added email validation call in `_validate_single_record()`

**Git Commit**: `git commit -m "Fix: add missing email validation"`

### Error 4: Performance Issues
**Error**: 334 seconds runtime for 199 records (1.6 seconds per record)
**Root Cause**: Multiple performance bottlenecks:
- Row-by-row processing with 10ms sleep per record
- Synchronous email sending with 100ms delay between emails
- No vectorized operations

**Initial Status**: 334.22 seconds total runtime
**Target**: < 30 seconds

## Performance Optimization Plan

### Phase 1: Data Processing Optimization
- Replace row-by-row loops with vectorized pandas operations
- Remove artificial delays
- Implement batch processing

### Phase 2: Email Service Optimization  
- Implement concurrent email sending using ThreadPoolExecutor
- Remove fixed delays between emails
- Add proper retry logic with exponential backoff

### Phase 3: Memory Optimization
- Release large objects after use
- Use chunked processing for large datasets
- Implement garbage collection

## Next Steps

1. ✅ Identify all bugs in the codebase
2. 🔄 Fix critical data processing errors
3. ⏳ Implement performance optimizations
4. ⏳ Add comprehensive error handling
5. ⏳ Measure and document performance improvements

---

*Last Updated*: 2025-08-03
*Status*: Initial bug identification complete, fixes in progress
