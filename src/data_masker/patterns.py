"""
Pattern registry for PII detection.
"""

import re
from typing import Dict, Pattern, List, Tuple
from dataclasses import dataclass


@dataclass
class PatternInfo:
    """Information about a PII pattern."""
    name: str
    pattern: Pattern[str]
    confidence: float
    category: str
    description: str


class PatternRegistry:
    """Registry of patterns for detecting personally identifiable information."""
    
    def __init__(self):
        self._patterns: Dict[str, PatternInfo] = {}
        self._initialize_default_patterns()
    
    def _initialize_default_patterns(self) -> None:
        """Initialize the registry with default patterns."""
        
        # Email patterns
        self.register(
            "email",
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            0.95,
            "contact",
            "Email addresses"
        )
        
        # Phone number patterns
        self.register(
            "phone_us",
            r'(\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            0.9,
            "contact",
            "US phone numbers"
        )
        
        self.register(
            "phone_international",
            r'\+?[1-9]\d{1,14}',
            0.8,
            "contact",
            "International phone numbers"
        )
        
        # Social Security Number
        self.register(
            "ssn",
            r'\b\d{3}-?\d{2}-?\d{4}\b',
            0.95,
            "identification",
            "US Social Security Numbers"
        )
        
        # Credit card numbers
        self.register(
            "credit_card",
            r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
            0.9,
            "financial",
            "Credit card numbers"
        )
        
        # Names (basic patterns)
        self.register(
            "name_title",
            r'\b(Mr|Mrs|Ms|Dr|Prof|Sir|Madam)\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b',
            0.8,
            "personal",
            "Names with titles"
        )
        
        # IP addresses
        self.register(
            "ip_address",
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b',
            0.95,
            "technical",
            "IPv4 addresses"
        )
        
        # MAC addresses
        self.register(
            "mac_address",
            r'\b([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})\b',
            0.95,
            "technical",
            "MAC addresses"
        )
        
        # URLs
        self.register(
            "url",
            r'https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?',
            0.9,
            "technical",
            "URLs"
        )
        
        # Address patterns (basic)
        self.register(
            "street_address",
            r'\d+\s+[A-Za-z0-9\s,.-]+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Way|Place|Pl)\b',
            0.7,
            "location",
            "Street addresses"
        )
        
        # Postal codes
        self.register(
            "zip_code",
            r'\b\d{5}(?:-\d{4})?\b',
            0.8,
            "location",
            "US ZIP codes"
        )
        
        # Date of birth patterns
        self.register(
            "date_birth",
            r'\b(?:0[1-9]|1[0-2])[-/](?:0[1-9]|[12][0-9]|3[01])[-/](?:19|20)\d{2}\b',
            0.8,
            "personal",
            "Dates (potential birth dates)"
        )
    
    def register(
        self, 
        name: str, 
        pattern: str, 
        confidence: float, 
        category: str, 
        description: str
    ) -> None:
        """Register a new pattern."""
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        self._patterns[name] = PatternInfo(
            name=name,
            pattern=compiled_pattern,
            confidence=confidence,
            category=category,
            description=description
        )
    
    def get_pattern(self, name: str) -> PatternInfo:
        """Get a pattern by name."""
        if name not in self._patterns:
            raise ValueError(f"Pattern '{name}' not found")
        return self._patterns[name]
    
    def get_patterns_by_category(self, category: str) -> List[PatternInfo]:
        """Get all patterns in a category."""
        return [
            pattern for pattern in self._patterns.values()
            if pattern.category == category
        ]
    
    def get_all_patterns(self) -> List[PatternInfo]:
        """Get all registered patterns."""
        return list(self._patterns.values())
    
    def find_matches(self, text: str, min_confidence: float = 0.8) -> List[Tuple[PatternInfo, List[re.Match]]]:
        """Find all pattern matches in text above confidence threshold."""
        matches = []
        
        for pattern_info in self._patterns.values():
            if pattern_info.confidence >= min_confidence:
                pattern_matches = list(pattern_info.pattern.finditer(text))
                if pattern_matches:
                    matches.append((pattern_info, pattern_matches))
        
        return matches
    
    def list_categories(self) -> List[str]:
        """List all available categories."""
        return list(set(pattern.category for pattern in self._patterns.values()))
