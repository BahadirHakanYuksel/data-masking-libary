"""
PII detection functionality.
"""

import re
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass

from .patterns import PatternRegistry, PatternInfo
from .config import MaskingConfig


@dataclass
class PIIMatch:
    """Represents a detected PII match."""
    text: str
    start: int
    end: int
    pattern_name: str
    confidence: float
    category: str


class PIIDetector:
    """Detects personally identifiable information in text and structured data."""
    
    def __init__(self, config: Optional[MaskingConfig] = None):
        self.config = config or MaskingConfig()
        self.pattern_registry = PatternRegistry()
        
        # Add custom patterns from config
        for name, pattern in self.config.custom_patterns.items():
            self.pattern_registry.register(
                name, pattern, 0.9, "custom", f"Custom pattern: {name}"
            )
    
    def detect_in_text(self, text: str) -> List[PIIMatch]:
        """Detect PII in a string."""
        if not isinstance(text, str):
            return []
        
        matches = []
        pattern_matches = self.pattern_registry.find_matches(
            text, self.config.confidence_threshold
        )
        
        for pattern_info, regex_matches in pattern_matches:
            for match in regex_matches:
                # Skip if in whitelist
                if match.group() in self.config.whitelist:
                    continue
                
                pii_match = PIIMatch(
                    text=match.group(),
                    start=match.start(),
                    end=match.end(),
                    pattern_name=pattern_info.name,
                    confidence=pattern_info.confidence,
                    category=pattern_info.category
                )
                matches.append(pii_match)
        
        # Sort by position for easier processing
        matches.sort(key=lambda x: x.start)
        return matches
    
    def detect_in_dict(self, data: Dict[str, Any]) -> Dict[str, List[PIIMatch]]:
        """Detect PII in a dictionary."""
        results = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                matches = self.detect_in_text(value)
                if matches:
                    results[key] = matches
            elif isinstance(value, dict):
                nested_results = self.detect_in_dict(value)
                if nested_results:
                    results[key] = nested_results
            elif isinstance(value, list):
                list_results = self.detect_in_list(value)
                if list_results:
                    results[key] = list_results
        
        return results
    
    def detect_in_list(self, data: List[Any]) -> Dict[int, Any]:
        """Detect PII in a list."""
        results = {}
        
        for i, item in enumerate(data):
            if isinstance(item, str):
                matches = self.detect_in_text(item)
                if matches:
                    results[i] = matches
            elif isinstance(item, dict):
                nested_results = self.detect_in_dict(item)
                if nested_results:
                    results[i] = nested_results
            elif isinstance(item, list):
                list_results = self.detect_in_list(item)
                if list_results:
                    results[i] = list_results
        
        return results
    
    def detect(self, data: Any) -> Any:
        """Detect PII in any supported data structure."""
        if isinstance(data, str):
            return self.detect_in_text(data)
        elif isinstance(data, dict):
            return self.detect_in_dict(data)
        elif isinstance(data, list):
            return self.detect_in_list(data)
        else:
            return []
    
    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze text and return detailed statistics."""
        matches = self.detect_in_text(text)
        
        stats = {
            "total_matches": len(matches),
            "categories": {},
            "patterns": {},
            "confidence_distribution": {"high": 0, "medium": 0, "low": 0},
            "matches": matches
        }
        
        for match in matches:
            # Count by category
            if match.category not in stats["categories"]:
                stats["categories"][match.category] = 0
            stats["categories"][match.category] += 1
            
            # Count by pattern
            if match.pattern_name not in stats["patterns"]:
                stats["patterns"][match.pattern_name] = 0
            stats["patterns"][match.pattern_name] += 1
            
            # Confidence distribution
            if match.confidence >= 0.9:
                stats["confidence_distribution"]["high"] += 1
            elif match.confidence >= 0.7:
                stats["confidence_distribution"]["medium"] += 1
            else:
                stats["confidence_distribution"]["low"] += 1
        
        return stats
