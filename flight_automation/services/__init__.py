"""
External services for flight booking automation.

This package contains integrations with external systems like email and reporting.
"""

from .email_service import EmailService
from .reporting import ReportGenerator

__all__ = ["EmailService", "ReportGenerator"]
