"""
Data Masking Library

A comprehensive Python library for automatically masking personal information in test data.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

from .masker import DataMasker
from .config import MaskingConfig, MaskingStrategy
from .detectors import PIIDetector
from .patterns import PatternRegistry

__all__ = [
    "DataMasker",
    "MaskingConfig", 
    "MaskingStrategy",
    "PIIDetector",
    "PatternRegistry"
]
