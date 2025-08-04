#!/usr/bin/env python
"""Setup script for Flight Automation System."""

from setuptools import setup, find_packages
import os

# Read the README file
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
def read_requirements(filename):
    """Read requirements from file."""
    with open(os.path.join(here, filename), encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="flight-automation-system",
    version="1.0.0",
    description="Production-ready flight booking automation system with performance optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Flight Automation Team",
    author_email="automation@company.com",
    url="https://github.com/company/flight-automation-system",
    
    # Package configuration
    packages=find_packages(exclude=['tests*', 'docs*']),
    python_requires=">=3.8",
    
    # Dependencies
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'pytest-mock>=3.10.0',
        ],
    },
    
    # Entry points for CLI commands
    entry_points={
        'console_scripts': [
            'flight-automation=scripts.run_automation:main',
            'generate-data=scripts.generate_data:main',
        ],
    },
    
    # Package data
    package_data={
        'flight_automation': [
            'config/*.yaml',
            'data/*.csv',
        ],
    },
    include_package_data=True,
    
    # Metadata
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Office/Business :: Financial",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="automation, flight booking, data processing, performance optimization",
    project_urls={
        "Bug Reports": "https://github.com/company/flight-automation-system/issues",
        "Source": "https://github.com/company/flight-automation-system",
        "Documentation": "https://flight-automation-system.readthedocs.io/",
    },
    
    # Development
    zip_safe=False,
)
