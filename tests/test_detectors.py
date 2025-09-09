"""
Test the pattern detection functionality.
"""

import pytest
from data_masker.patterns import PatternRegistry, PatternInfo
from data_masker.detectors import PIIDetector, PIIMatch
from data_masker.config import MaskingConfig


class TestPatternRegistry:
    """Test cases for PatternRegistry class."""
    
    def test_default_patterns_loaded(self):
        """Test that default patterns are loaded."""
        registry = PatternRegistry()
        patterns = registry.get_all_patterns()
        
        assert len(patterns) > 0
        
        # Check for essential patterns
        pattern_names = [p.name for p in patterns]
        assert "email" in pattern_names
        assert "phone_us" in pattern_names
        assert "ssn" in pattern_names
        assert "credit_card" in pattern_names
    
    def test_register_custom_pattern(self):
        """Test registering a custom pattern."""
        registry = PatternRegistry()
        
        registry.register(
            "test_pattern",
            r"TEST\d{3}",
            0.9,
            "test",
            "Test pattern"
        )
        
        pattern = registry.get_pattern("test_pattern")
        assert pattern.name == "test_pattern"
        assert pattern.confidence == 0.9
        assert pattern.category == "test"
    
    def test_find_matches(self):
        """Test finding pattern matches in text."""
        registry = PatternRegistry()
        text = "Contact john@example.com or call 555-123-4567"
        
        matches = registry.find_matches(text, min_confidence=0.8)
        
        assert len(matches) > 0
        # Should find email and phone
        pattern_names = [match[0].name for match in matches]
        assert "email" in pattern_names
        assert "phone_us" in pattern_names
    
    def test_get_patterns_by_category(self):
        """Test getting patterns by category."""
        registry = PatternRegistry()
        contact_patterns = registry.get_patterns_by_category("contact")
        
        assert len(contact_patterns) > 0
        pattern_names = [p.name for p in contact_patterns]
        assert "email" in pattern_names


class TestPIIDetector:
    """Test cases for PIIDetector class."""
    
    def test_detect_email(self):
        """Test email detection."""
        detector = PIIDetector()
        text = "Send report to admin@company.com"
        
        matches = detector.detect_in_text(text)
        
        assert len(matches) == 1
        assert matches[0].text == "admin@company.com"
        assert matches[0].pattern_name == "email"
        assert matches[0].category == "contact"
    
    def test_detect_phone(self):
        """Test phone number detection."""
        detector = PIIDetector()
        text = "Call us at (555) 123-4567"
        
        matches = detector.detect_in_text(text)
        
        assert len(matches) >= 1
        phone_match = next(m for m in matches if m.pattern_name.startswith("phone"))
        assert "(555) 123-4567" in phone_match.text
    
    def test_detect_ssn(self):
        """Test SSN detection."""
        detector = PIIDetector()
        text = "SSN: 123-45-6789"
        
        matches = detector.detect_in_text(text)
        
        assert len(matches) >= 1
        ssn_match = next(m for m in matches if m.pattern_name == "ssn")
        assert ssn_match.text == "123-45-6789"
    
    def test_detect_in_dict(self):
        """Test detection in dictionary."""
        detector = PIIDetector()
        data = {
            "user": {
                "email": "user@example.com",
                "phone": "555-1234"
            },
            "admin_contact": "admin@company.com"
        }
        
        results = detector.detect_in_dict(data)
        
        assert "user" in results
        assert "admin_contact" in results
    
    def test_confidence_threshold(self):
        """Test confidence threshold filtering."""
        config = MaskingConfig(confidence_threshold=0.95)
        detector = PIIDetector(config)
        
        text = "Contact us at info@example.com"
        matches = detector.detect_in_text(text)
        
        # Should only return high-confidence matches
        for match in matches:
            assert match.confidence >= 0.95
    
    def test_whitelist(self):
        """Test whitelisting functionality."""
        config = MaskingConfig(whitelist=["public@company.com"])
        detector = PIIDetector(config)
        
        text = "Contact public@company.com or private@company.com"
        matches = detector.detect_in_text(text)
        
        # Should not detect whitelisted email
        detected_texts = [match.text for match in matches]
        assert "public@company.com" not in detected_texts
        assert "private@company.com" in detected_texts
    
    def test_custom_patterns(self):
        """Test custom pattern detection."""
        config = MaskingConfig(
            custom_patterns={"product_code": r"PROD-\d{4}"}
        )
        detector = PIIDetector(config)
        
        text = "Product code: PROD-1234"
        matches = detector.detect_in_text(text)
        
        assert len(matches) >= 1
        product_match = next(m for m in matches if m.pattern_name == "product_code")
        assert product_match.text == "PROD-1234"
    
    def test_analyze_text(self):
        """Test text analysis functionality."""
        detector = PIIDetector()
        text = "John Doe's email is john@example.com and phone is 555-123-4567"
        
        analysis = detector.analyze_text(text)
        
        assert analysis["total_matches"] > 0
        assert "contact" in analysis["categories"]
        assert "email" in analysis["patterns"]
        assert len(analysis["matches"]) > 0
