# Steel Industry Automation System

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A production-ready automation system for processing steel industry orders with robust error handling, performance optimization, and comprehensive monitoring. Built specifically for steel manufacturing and distribution operations.

## 🚀 Performance Achievement
- **High-performance processing** with vectorized operations
- **Comprehensive validation** with 8-category steel industry rules
- **Real-time monitoring** and performance metrics
- **Production-ready** with robust error handling

## 📊 Key Features

### Steel Industry Specific
- **19 Steel Grades Supported**: A36, S355, 304SS, 316SS, 409SS, 430SS, 201SS, and more
- **8 Steel Types**: Carbon Steel, Stainless Steel, Alloy Steel, Tool Steel, Hot/Cold Rolled, Galvanized, Spring Steel
- **10 Production Lines**: Full production workflow automation
- **Quality Standards**: ASTM, ISO, JIS compliance validation
- **Dimensional Validation**: Thickness, width, length with tolerance checking
- **Weight Calculation**: Automated weight validation and calculations

### Technical Excellence
- **Vectorized Processing**: High-performance pandas operations
- **Concurrent Email Processing**: Parallel customer notifications
- **Comprehensive Validation**: 8-category validation system
- **Performance Monitoring**: Real-time metrics and profiling
- **Industry Standards**: Steel grade compatibility validation
- **Business Rules**: Production workflow and quality control

## 🏗️ Project Structure

```
steel-automation-system/
├── steel_automation/           # Main package
│   ├── core/
│   │   ├── data_processor.py   # Steel order processing
│   │   └── validation.py       # Steel industry validation
│   ├── services/
│   │   ├── email_service.py    # Customer notifications
│   │   └── reporting.py        # Steel production reports
│   └── utils/
│       ├── logger.py           # Logging utilities
│       └── metrics.py          # Performance monitoring
├── data/
│   ├── steel_orders.csv        # Steel order dataset
│   └── generate_steel_data.py  # Data generator
├── config/
│   ├── settings.yaml           # Steel automation settings
│   ├── logging.yaml            # Logging configuration
│   └── email_templates.yaml    # Email templates
├── reports/                    # Generated reports
├── logs/                       # Application logs
├── main_steel.py              # Main entry point
└── test_steel_automation.py   # Testing script
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Required packages: pandas, pyyaml, psutil

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd steel-automation-system

# Install dependencies
pip install -r requirements.txt

# Configure settings (optional)
cp config/settings.yaml.example config/settings.yaml
```

### Basic Usage
```bash
# Run steel automation with default settings
python main_steel.py --data data/steel_orders.csv

# Dry run (validation only)
python main_steel.py --data data/steel_orders.csv --dry-run

# With custom output directory
python main_steel.py --data data/steel_orders.csv --output my_reports/

# Enable performance profiling
python main_steel.py --data data/steel_orders.csv --profile

# Verbose logging
python main_steel.py --data data/steel_orders.csv --verbose
```

### Testing
```bash
# Run component tests
python test_steel_automation.py

# Quick functionality test
python quick_test.py
```

## 📊 Steel Industry Features

### Supported Steel Grades
- **Carbon Steel**: A36, A572-50, A992, S275, S355
- **Stainless Steel**: 304SS, 316SS, 409SS, 430SS, 201SS
- **Alloy Steel**: 4140, 4340, 8620
- **Tool Steel**: H13, D2, O1
- **Special Types**: Hot Rolled, Cold Rolled, Galvanized, Spring Steel

### Validation Categories
1. **Steel Grade Compatibility**: Ensures grade matches steel type
2. **Dimensional Validation**: Thickness, width, length within tolerances
3. **Weight Validation**: Calculated vs. specified weight verification
4. **Quality Control**: Production status and quality grade validation
5. **Business Rules**: Production workflow compliance
6. **Date Validation**: Order, production, and delivery date logic
7. **Financial Validation**: Pricing and cost calculations
8. **Data Format**: Email, phone, and required field validation

### Email Templates
- Order confirmation
- Production start notification
- Quality check update
- Shipping notification
- Delivery confirmation
- Quality alert
- Production delay notice

## 🔧 Configuration

### Steel Industry Settings
```yaml
steel_automation:
  steel_standards:
    grade_validation: true
    dimensional_tolerance: 0.1  # percentage
    weight_tolerance: 0.05     # percentage
    quality_standards: ["ASTM", "ISO", "JIS"]
    
  production:
    default_lead_time_days: 14
    quality_check_required: true
    batch_tracking: true
    production_lines: 10
```

## 📈 Performance Metrics

The system includes comprehensive performance monitoring:
- **Processing Rate**: Orders per second
- **Memory Usage**: Real-time memory tracking
- **Validation Efficiency**: Error detection rates
- **Email Performance**: Delivery success rates
- **Report Generation**: Time and resource usage

## 🏆 Production Ready Features

- ✅ **Robust Error Handling**: Graceful failure recovery
- ✅ **Comprehensive Logging**: Detailed audit trails
- ✅ **Performance Profiling**: Built-in performance analysis
- ✅ **Scalable Architecture**: Modular design for growth
- ✅ **Industry Standards**: Steel manufacturing compliance
- ✅ **Monitoring**: Real-time system health tracking
- ✅ **Documentation**: Complete API and usage docs

## 🔍 Steel Order Processing

### Input Data Format
```csv
OrderID,BatchID,CustomerName,SteelGrade,SteelType,Thickness,Width,Length,Weight,UnitPrice,OrderDate,ProductionDate,DeliveryDate,Status,QualityGrade,ProductionLine,Email
SO-2025-0001,BATCH-001,Steel Corp,A36,Carbon Steel,10.5,1500,3000,345.6,85.50,2025-01-15,2025-01-20,2025-02-15,Confirmed,A,Line-01,customer@steelcorp.com
```

### Processing Pipeline
1. **Data Loading**: CSV parsing with error handling
2. **Validation**: 8-category comprehensive validation
3. **Processing**: Business logic and calculations
4. **Notifications**: Customer email communications
5. **Reporting**: Comprehensive analytics and summaries

## 📊 Generated Reports

- **Steel Order Summary**: Order statistics and totals
- **Production Metrics**: Production line performance
- **Quality Analysis**: Quality control and compliance
- **Customer Analytics**: Customer order patterns
- **System Performance**: Technical performance metrics
- **Validation Report**: Detailed validation results

## 🛠️ Development

### Architecture
- **Modular Design**: Separated concerns with clear interfaces
- **Performance Optimized**: Vectorized operations for large datasets
- **Error Resilient**: Comprehensive error handling and recovery
- **Configurable**: YAML-based configuration system
- **Extensible**: Plugin architecture for custom validators

### Steel Industry Standards
- **ASTM Standards**: American Society for Testing and Materials
- **ISO Standards**: International Organization for Standardization
- **JIS Standards**: Japanese Industrial Standards
- **Custom Validation**: Company-specific business rules

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact the development team
- Check the documentation in `docs/`

---

**Steel Industry Automation System** - Production-ready automation for steel manufacturing operations.
