"""
Core data masking functionality.
"""

import json
import re
from typing import Any, Dict, List, Optional, Union
from faker import Faker
from cryptography.fernet import Fernet

from .config import MaskingConfig, MaskingStrategy
from .detectors import PIIDetector, PIIMatch


class DataMasker:
    """Main class for masking personally identifiable information."""
    
    def __init__(self, config: Optional[MaskingConfig] = None):
        self.config = config or MaskingConfig()
        self.detector = PIIDetector(self.config)
        self.faker = Faker(self.config.locale)
        
        # Initialize encryption if needed
        self._fernet = None
        if self.config.strategy == MaskingStrategy.ENCRYPT:
            if self.config.encryption_key:
                self._fernet = Fernet(self.config.encryption_key.encode())
            else:
                # Generate a key for this session
                key = Fernet.generate_key()
                self._fernet = Fernet(key)
                print(f"Generated encryption key: {key.decode()}")
    
    def mask_text(self, text: str) -> str:
        """Mask PII in a text string."""
        if not isinstance(text, str):
            return text
        
        matches = self.detector.detect_in_text(text)
        if not matches:
            return text
        
        # Process matches in reverse order to maintain positions
        masked_text = text
        for match in reversed(matches):
            masked_value = self._apply_masking_strategy(
                match.text, match.pattern_name, match.category
            )
            masked_text = (
                masked_text[:match.start] + 
                masked_value + 
                masked_text[match.end:]
            )
        
        return masked_text
    
    def mask_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask PII in a dictionary."""
        masked_data = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                masked_data[key] = self.mask_text(value)
            elif isinstance(value, dict):
                masked_data[key] = self.mask_dict(value)
            elif isinstance(value, list):
                masked_data[key] = self.mask_list(value)
            else:
                masked_data[key] = value
        
        return masked_data
    
    def mask_list(self, data: List[Any]) -> List[Any]:
        """Mask PII in a list."""
        masked_data = []
        
        for item in data:
            if isinstance(item, str):
                masked_data.append(self.mask_text(item))
            elif isinstance(item, dict):
                masked_data.append(self.mask_dict(item))
            elif isinstance(item, list):
                masked_data.append(self.mask_list(item))
            else:
                masked_data.append(item)
        
        return masked_data
    
    def mask(self, data: Any) -> Any:
        """Mask PII in any supported data structure."""
        if isinstance(data, str):
            return self.mask_text(data)
        elif isinstance(data, dict):
            return self.mask_dict(data)
        elif isinstance(data, list):
            return self.mask_list(data)
        else:
            return data
    
    def _apply_masking_strategy(
        self, 
        text: str, 
        pattern_name: str, 
        category: str
    ) -> str:
        """Apply the configured masking strategy to a piece of text."""
        
        if self.config.strategy == MaskingStrategy.REPLACE:
            return self._replace_strategy(text, pattern_name)
        
        elif self.config.strategy == MaskingStrategy.REDACT:
            return "[REDACTED]"
        
        elif self.config.strategy == MaskingStrategy.ENCRYPT:
            return self._encrypt_strategy(text)
        
        elif self.config.strategy == MaskingStrategy.TOKENIZE:
            return self._tokenize_strategy(text, pattern_name)
        
        elif self.config.strategy == MaskingStrategy.FAKER:
            return self._faker_strategy(text, pattern_name, category)
        
        else:
            # Default to replace
            return self._replace_strategy(text, pattern_name)
    
    def _replace_strategy(self, text: str, pattern_name: str) -> str:
        """Replace characters with mask character."""
        if not self.config.preserve_format:
            return self.config.mask_character * len(text)
        
        # Preserve format for specific patterns
        if pattern_name == "email":
            return self._mask_email(text)
        elif pattern_name.startswith("phone"):
            return self._mask_phone(text)
        elif pattern_name == "ssn":
            return self._mask_ssn(text)
        elif pattern_name == "credit_card":
            return self._mask_credit_card(text)
        else:
            # General masking with partial reveal
            if self.config.partial_mask and len(text) > 4:
                visible_chars = min(2, len(text) // 4)
                masked_chars = len(text) - (2 * visible_chars)
                return (
                    text[:visible_chars] + 
                    self.config.mask_character * masked_chars + 
                    text[-visible_chars:]
                )
            else:
                return self.config.mask_character * len(text)
    
    def _mask_email(self, email: str) -> str:
        """Mask email while preserving domain if configured."""
        if '@' not in email:
            return self.config.mask_character * len(email)
        
        local, domain = email.split('@', 1)
        
        if self.config.preserve_domains:
            masked_local = self.config.mask_character * len(local)
            return f"{masked_local}@{domain}"
        else:
            return self.config.mask_character * len(email)
    
    def _mask_phone(self, phone: str) -> str:
        """Mask phone number while preserving format."""
        # Keep non-digit characters, mask digits
        masked = ""
        for char in phone:
            if char.isdigit():
                masked += self.config.mask_character
            else:
                masked += char
        return masked
    
    def _mask_ssn(self, ssn: str) -> str:
        """Mask SSN with standard format."""
        # Remove non-digits
        digits = re.sub(r'\D', '', ssn)
        if len(digits) == 9:
            if '-' in ssn:
                return f"{self.config.mask_character * 3}-{self.config.mask_character * 2}-{self.config.mask_character * 4}"
            else:
                return self.config.mask_character * 9
        return self.config.mask_character * len(ssn)
    
    def _mask_credit_card(self, card: str) -> str:
        """Mask credit card number, showing last 4 digits."""
        digits = re.sub(r'\D', '', card)
        if len(digits) >= 12:
            masked_digits = self.config.mask_character * (len(digits) - 4) + digits[-4:]
            # Restore original formatting
            result = ""
            digit_index = 0
            for char in card:
                if char.isdigit():
                    result += masked_digits[digit_index]
                    digit_index += 1
                else:
                    result += char
            return result
        return self.config.mask_character * len(card)
    
    def _encrypt_strategy(self, text: str) -> str:
        """Encrypt the text."""
        if self._fernet:
            encrypted = self._fernet.encrypt(text.encode())
            return f"[ENCRYPTED:{encrypted.decode()}]"
        return "[ENCRYPTION_ERROR]"
    
    def _tokenize_strategy(self, text: str, pattern_name: str) -> str:
        """Replace with a token."""
        return f"[{pattern_name.upper()}_TOKEN_{hash(text) % 10000:04d}]"
    
    def _faker_strategy(self, text: str, pattern_name: str, category: str) -> str:
        """Replace with fake data."""
        try:
            if pattern_name == "email":
                return self.faker.email()
            elif pattern_name.startswith("phone"):
                return self.faker.phone_number()
            elif pattern_name == "ssn":
                return self.faker.ssn()
            elif pattern_name == "credit_card":
                return self.faker.credit_card_number()
            elif pattern_name.startswith("name"):
                return self.faker.name()
            elif category == "location":
                return self.faker.address()
            elif category == "personal":
                return self.faker.name()
            else:
                # Fallback to generic text
                return self.faker.word()
        except Exception:
            # Fallback to replace strategy
            return self._replace_strategy(text, pattern_name)
    
    def decrypt(self, encrypted_text: str) -> str:
        """Decrypt text that was encrypted by this masker."""
        if not self._fernet:
            raise ValueError("No encryption key available")
        
        if encrypted_text.startswith("[ENCRYPTED:") and encrypted_text.endswith("]"):
            encrypted_data = encrypted_text[11:-1]  # Remove wrapper
            try:
                decrypted = self._fernet.decrypt(encrypted_data.encode())
                return decrypted.decode()
            except Exception as e:
                raise ValueError(f"Failed to decrypt: {e}")
        else:
            raise ValueError("Text is not in encrypted format")
    
    def analyze(self, data: Any) -> Dict[str, Any]:
        """Analyze data and return PII detection statistics."""
        if isinstance(data, str):
            return self.detector.analyze_text(data)
        elif isinstance(data, (dict, list)):
            # Convert to JSON string for analysis
            json_str = json.dumps(data, default=str)
            return self.detector.analyze_text(json_str)
        else:
            return {"error": "Unsupported data type for analysis"}
