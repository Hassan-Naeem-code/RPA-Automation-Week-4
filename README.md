# Flight Booking Automation - Debug & Optimize Assignment

🚀 **Performance Achievement**: 334s → 18.5s (94.5% improvement)

## Project Overview

This project demonstrates the complete lifecycle of debugging and optimizing a Python automation workflow for flight booking confirmations. Starting with a deliberately flawed system, we systematically identified bugs, implemented fixes, and optimized performance using industry best practices.

## 📁 Project Structure

```
RPA-Automation-Week-4/
├── data/
│   ├── generate_sample_data.py    # Synthetic data generator with edge cases
│   └── reservations.csv           # 205 test records with intentional issues
├── src/
│   ├── data_processor.py          # Data processing and validation logic
│   ├── email_service.py           # Email confirmation service  
│   ├── validation.py              # Data validation rules
│   └── reporting.py               # Report generation
├── docs/
│   └── troubleshooting.md         # Complete debugging documentation
├── reports/                       # Generated reports and analysis
├── main.py                        # Original (fixed) automation workflow
├── main_optimized.py              # Performance-optimized version
└── performance_analysis.py        # Performance comparison tool
```

## 🐛 Bugs Identified & Fixed

### Critical Issues Resolved:
1. **String Fare Conversion Errors**: Fixed handling of "$2097.46" format values
2. **Invalid Record Filtering**: Validation wasn't actually filtering out bad records  
3. **Missing Email Validation**: Email format validation existed but wasn't called
4. **Performance Bottlenecks**: Row-by-row processing with artificial delays
5. **Synchronous Email Processing**: Blocking email operations without concurrency

### Edge Cases Handled:
- Missing values (emails, phones, fares)
- Mixed data types (string vs numeric fares)
- Duplicate records
- Invalid airport codes
- Same origin/destination pairs
- Zero/negative fare amounts

## ⚡ Performance Optimizations

### Key Strategies:
1. **Vectorized Operations**: Replaced pandas row iteration with vectorized operations
2. **Concurrent Processing**: Implemented ThreadPoolExecutor for email sending
3. **Memory Management**: Added garbage collection and object cleanup
4. **Batch Processing**: Grouped operations to reduce overhead

### Results:
| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Runtime | 334.22s | 18.51s | **94.5% faster** |
| Throughput | 0.6 rec/s | 9.94 rec/s | **1560% improvement** |
| Memory | Variable | Stable 72MB | Consistent usage |

## 🚀 Quick Start

### Prerequisites
- Python 3.11+ 
- Virtual environment recommended

### Installation
```bash
git clone <repository-url>
cd RPA-Automation-Week-4
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install pandas faker numpy psutil tenacity snakeviz
```

### Generate Test Data
```bash
cd data
python generate_sample_data.py
```

### Run Original vs Optimized
```bash
# Original (fixed) version
python main.py

# Optimized version  
python main_optimized.py

# Performance comparison
python performance_analysis.py
```

## 📊 Key Metrics

### Data Processing Results:
- **Total Records**: 205 (including intentional duplicates)
- **Valid Records**: 184 (after filtering invalid data)
- **Email Success Rate**: 97.8% (180/184 valid emails)
- **Processing Rate**: 9.94 records/second (optimized)

### Optimization Impact:
- **Data Processing**: 2.3s → 0.01s (99.5% faster)
- **Email Sending**: 189s → 18s (90% faster)  
- **Total Workflow**: 334s → 18.5s (94.5% faster)

## 📈 Profiling & Analysis

Performance profiling data available in:
- `automation_profile.prof` - Original version profiling
- `automation_optimized_profile.prof` - Optimized version profiling

View with snakeviz:
```bash
snakeviz automation_optimized_profile.prof
```

## 🛠️ Technical Highlights

### Vectorized Data Cleaning
```python
# Before: Row-by-row processing (slow)
for index, row in data.iterrows():
    processed_record = self._process_single_reservation(row)

# After: Vectorized operations (fast)
data_clean = data.drop_duplicates(subset=['PNR'], keep='first')
data_clean = data_clean[
    (data_clean['Origin'].isin(valid_airports)) & 
    (data_clean['Destination'].isin(valid_airports)) &
    (data_clean['Fare'] > 0)
]
```

### Concurrent Email Processing
```python
# Before: Synchronous sending
for reservation in reservations:
    send_email(reservation)
    time.sleep(0.1)  # Artificial delay

# After: Concurrent processing
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(send_email, reservation) 
               for reservation in reservations]
    results = [future.result() for future in as_completed(futures)]
```

## 📝 Documentation

Complete debugging and optimization documentation available in:
- [`docs/troubleshooting.md`](docs/troubleshooting.md) - Detailed error analysis and fixes
- Log files with performance metrics
- JSON reports with processing statistics

## 🎯 Learning Outcomes

This project demonstrates:
- **Systematic Debugging**: Identifying and fixing complex data processing errors
- **Performance Profiling**: Using cProfile and metrics to identify bottlenecks  
- **Optimization Strategies**: Vectorization, concurrency, and memory management
- **Production Readiness**: Error handling, logging, and monitoring
- **Documentation**: Clear tracking of problems, solutions, and improvements

## 🤝 Contributing

This is an educational project demonstrating debugging and optimization techniques. The intentional bugs and performance issues are designed to simulate real-world automation challenges.

---

**Author**: Muhammad Hassan Naeem  
**Course**: LR-Robotic Process Automation  
**Assignment**: Week 4 - Debug and Optimize Python Automation  
**Date**: August 2025
