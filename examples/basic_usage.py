#!/usr/bin/env python3
"""
Basic usage examples for the Data Masking Library.
"""

from data_masker import DataMasker, MaskingConfig, MaskingStrategy


def basic_text_masking():
    """Demonstrate basic text masking."""
    print("=== Basic Text Masking ===")
    
    masker = DataMasker()
    
    texts = [
        "Contact John Doe at john.doe@company.com or call +1-555-123-4567",
        "SSN: 123-45-6789, Credit Card: 4532-1234-5678-9012",
        "Visit us at 123 Main Street, New York, NY 10001",
        "IP Address: 192.168.1.1, MAC: 00:1B:44:11:3A:B7"
    ]
    
    for text in texts:
        masked = masker.mask_text(text)
        print(f"Original: {text}")
        print(f"Masked:   {masked}")
        print()


def dictionary_masking():
    """Demonstrate dictionary masking."""
    print("=== Dictionary Masking ===")
    
    masker = DataMasker()
    
    user_data = {
        "id": 12345,
        "personal_info": {
            "full_name": "Alice Johnson",
            "email": "alice.johnson@company.com",
            "phone": "(555) 987-6543",
            "ssn": "987-65-4321"
        },
        "address": {
            "street": "456 Oak Avenue",
            "city": "San Francisco",
            "zip": "94102"
        },
        "metadata": {
            "created_at": "2023-01-15",
            "is_active": True
        }
    }
    
    print("Original data:")
    print(user_data)
    print()
    
    masked_data = masker.mask(user_data)
    print("Masked data:")
    print(masked_data)
    print()


def different_strategies():
    """Demonstrate different masking strategies."""
    print("=== Different Masking Strategies ===")
    
    test_text = "Contact support at support@company.com or call 1-800-555-0199"
    
    strategies = [
        (MaskingStrategy.REPLACE, "Replace with mask characters"),
        (MaskingStrategy.REDACT, "Redact with [REDACTED]"),
        (MaskingStrategy.TOKENIZE, "Replace with tokens"),
        (MaskingStrategy.FAKER, "Replace with fake data")
    ]
    
    for strategy, description in strategies:
        print(f"{description}:")
        config = MaskingConfig(strategy=strategy)
        masker = DataMasker(config)
        masked = masker.mask_text(test_text)
        print(f"  {masked}")
        print()


def custom_patterns():
    """Demonstrate custom pattern detection."""
    print("=== Custom Patterns ===")
    
    # Add custom pattern for employee IDs
    config = MaskingConfig(
        custom_patterns={
            "employee_id": r"EMP\d{6}",
            "product_code": r"PROD-[A-Z]{2}\d{4}"
        }
    )
    
    masker = DataMasker(config)
    
    text = "Employee EMP123456 worked on product PROD-AB1234 last month"
    masked = masker.mask_text(text)
    
    print(f"Original: {text}")
    print(f"Masked:   {masked}")
    print()


def analysis_example():
    """Demonstrate PII analysis without masking."""
    print("=== PII Analysis ===")
    
    masker = DataMasker()
    
    text = """
    Dear John Smith,
    
    Thank you for your inquiry. Please contact us at support@company.com
    or call our office at (555) 123-4567. For reference, your customer
    ID is CUST-001234 and your SSN on file is 123-45-6789.
    
    Best regards,
    Customer Service Team
    """
    
    analysis = masker.analyze(text)
    
    print("Analysis Results:")
    print(f"Total PII matches found: {analysis['total_matches']}")
    print(f"Categories detected: {list(analysis['categories'].keys())}")
    print(f"Patterns detected: {list(analysis['patterns'].keys())}")
    print()
    
    print("Confidence distribution:")
    conf_dist = analysis['confidence_distribution']
    print(f"  High confidence (≥0.9): {conf_dist['high']}")
    print(f"  Medium confidence (≥0.7): {conf_dist['medium']}")
    print(f"  Low confidence (<0.7): {conf_dist['low']}")
    print()


if __name__ == "__main__":
    print("Data Masking Library - Basic Usage Examples")
    print("=" * 50)
    print()
    
    basic_text_masking()
    dictionary_masking()
    different_strategies()
    custom_patterns()
    analysis_example()
    
    print("Examples completed!")
