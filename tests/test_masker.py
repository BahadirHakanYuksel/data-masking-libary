"""
Test the basic masking functionality.
"""

import pytest
from data_masker import DataMasker, MaskingConfig, MaskingStrategy


class TestDataMasker:
    """Test cases for DataMasker class."""
    
    def test_mask_email(self):
        """Test email masking."""
        masker = DataMasker()
        text = "Contact us at john.doe@example.com for more info"
        masked = masker.mask_text(text)
        
        assert "john.doe@example.com" not in masked
        assert "@example.com" in masked  # Domain preserved by default
        assert "Contact us at" in masked
    
    def test_mask_phone(self):
        """Test phone number masking."""
        masker = DataMasker()
        text = "Call us at +1-555-123-4567"
        masked = masker.mask_text(text)
        
        assert "+1-555-123-4567" not in masked
        assert "+█-███-███-████" in masked
    
    def test_mask_ssn(self):
        """Test SSN masking."""
        masker = DataMasker()
        text = "SSN: 123-45-6789"
        masked = masker.mask_text(text)
        
        assert "123-45-6789" not in masked
        assert "███-██-████" in masked
    
    def test_mask_dict(self):
        """Test dictionary masking."""
        masker = DataMasker()
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "555-123-4567",
            "age": 30
        }
        
        masked = masker.mask(data)
        
        assert masked["email"] != "john@example.com"
        assert "@example.com" in masked["email"]
        assert masked["phone"] != "555-123-4567"
        assert masked["age"] == 30  # Not PII, should remain unchanged
    
    def test_redact_strategy(self):
        """Test redaction strategy."""
        config = MaskingConfig(strategy=MaskingStrategy.REDACT)
        masker = DataMasker(config)
        
        text = "Email: john@example.com"
        masked = masker.mask_text(text)
        
        assert "[REDACTED]" in masked
        assert "john@example.com" not in masked
    
    def test_tokenize_strategy(self):
        """Test tokenization strategy."""
        config = MaskingConfig(strategy=MaskingStrategy.TOKENIZE)
        masker = DataMasker(config)
        
        text = "Email: john@example.com"
        masked = masker.mask_text(text)
        
        assert "[EMAIL_TOKEN_" in masked
        assert "john@example.com" not in masked
    
    def test_custom_patterns(self):
        """Test custom pattern detection."""
        config = MaskingConfig(
            custom_patterns={"employee_id": r"EMP\d{6}"}
        )
        masker = DataMasker(config)
        
        text = "Employee ID: EMP123456"
        masked = masker.mask_text(text)
        
        assert "EMP123456" not in masked
    
    def test_whitelist(self):
        """Test whitelisting functionality."""
        config = MaskingConfig(whitelist=["admin@company.com"])
        masker = DataMasker(config)
        
        text = "Contact admin@company.com or user@example.com"
        masked = masker.mask_text(text)
        
        assert "admin@company.com" in masked  # Whitelisted
        assert "user@example.com" not in masked  # Should be masked
    
    def test_analyze(self):
        """Test analysis functionality."""
        masker = DataMasker()
        text = "Contact John Doe at john@example.com or 555-123-4567"
        
        analysis = masker.analyze(text)
        
        assert analysis["total_matches"] > 0
        assert "contact" in analysis["categories"]
        assert analysis["confidence_distribution"]["high"] > 0


class TestMaskingConfig:
    """Test cases for MaskingConfig class."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = MaskingConfig()
        
        assert config.strategy == MaskingStrategy.REPLACE
        assert config.preserve_format is True
        assert config.mask_character == "█"
        assert config.confidence_threshold == 0.8
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = MaskingConfig(
            strategy=MaskingStrategy.FAKER,
            mask_character="*",
            confidence_threshold=0.9
        )
        
        assert config.strategy == MaskingStrategy.FAKER
        assert config.mask_character == "*"
        assert config.confidence_threshold == 0.9
