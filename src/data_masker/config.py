"""
Configuration classes for the data masking library.
"""

from enum import Enum
from typing import Dict, Optional, Any
from pydantic import BaseModel, Field


class MaskingStrategy(str, Enum):
    """Available masking strategies."""
    REPLACE = "replace"  # Replace with placeholder characters
    REDACT = "redact"    # Replace with [REDACTED]
    ENCRYPT = "encrypt"  # Encrypt the data
    TOKENIZE = "tokenize"  # Replace with tokens
    FAKER = "faker"      # Replace with fake data


class MaskingConfig(BaseModel):
    """Configuration for data masking operations."""
    
    strategy: MaskingStrategy = Field(
        default=MaskingStrategy.REPLACE,
        description="The masking strategy to use"
    )
    
    preserve_format: bool = Field(
        default=True,
        description="Whether to preserve the original format"
    )
    
    mask_character: str = Field(
        default="█",
        description="Character to use for replacement masking"
    )
    
    partial_mask: bool = Field(
        default=True,
        description="Whether to partially mask (show some characters)"
    )
    
    encryption_key: Optional[str] = Field(
        default=None,
        description="Key for encryption strategy"
    )
    
    custom_patterns: Dict[str, str] = Field(
        default_factory=dict,
        description="Custom regex patterns for detection"
    )
    
    locale: str = Field(
        default="en_US",
        description="Locale for faker strategy"
    )
    
    confidence_threshold: float = Field(
        default=0.8,
        description="Minimum confidence for PII detection"
    )
    
    preserve_domains: bool = Field(
        default=True,
        description="Whether to preserve email domains and phone area codes"
    )
    
    whitelist: list[str] = Field(
        default_factory=list,
        description="Values to never mask"
    )
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True
