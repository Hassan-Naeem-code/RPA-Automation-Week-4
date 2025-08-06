#!/usr/bin/env python
"""Setup script for Steel Industry Automation System."""

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
    name="steel-automation-system",
    version="1.0.0",
    description="Steel Industry Automation System for order processing and manufacturing workflow",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Steel Automation Team",
    author_email="automation@steelcompany.com",
    url="https://github.com/steel-automation/steel-automation-system",
    
    # Packages
    packages=find_packages(),
    python_requires=">=3.11",
    
    # Dependencies
    install_requires=read_requirements('requirements.txt'),
    extras_require={
        'dev': read_requirements('requirements-dev.txt'),
    },
    
    # Metadata
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Manufacturing",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Office/Business :: Steel Manufacturing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Industrial Engineering",
    ],
    
    # Entry points
    entry_points={
        'console_scripts': [
            'steel-automation=main_steel:main',
            'steel-test=test_steel_automation:test_steel_automation',
            'steel-quick-test=quick_test:quick_test',
        ],
    },
    
    # Package data
    include_package_data=True,
    package_data={
        'steel_automation': [
            'config/*.yaml',
            'templates/*.html',
            'data/*.csv',
        ],
        '': ['*.md', '*.txt', '*.yml', '*.yaml'],
    },
    
    # Project URLs
    project_urls={
        'Bug Reports': 'https://github.com/steel-automation/steel-automation-system/issues',
        'Source': 'https://github.com/steel-automation/steel-automation-system',
        'Documentation': 'https://steel-automation.readthedocs.io/',
    },
    
    # Keywords
    keywords='steel automation manufacturing industry orders processing validation',
    
    # Test suite
    test_suite='tests',
    tests_require=[
        'pytest>=7.0.0',
        'pytest-cov>=4.0.0',
    ],
)
