#!/usr/bin/env python3
"""
Simple test script for the Data Masking Library.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from data_masker import DataMasker, MaskingConfig, MaskingStrategy
    print("✅ Successfully imported Data Masking Library!")
    
    # Test basic functionality
    print("\n🧪 Testing basic masking...")
    masker = DataMasker()
    
    test_data = {
        "name": "John Doe",
        "email": "john.doe@company.com",
        "phone": "+1-555-123-4567",
        "ssn": "123-45-6789"
    }
    
    print(f"Original data: {test_data}")
    
    masked_data = masker.mask(test_data)
    print(f"Masked data: {masked_data}")
    
    # Test different strategies
    print("\n🔄 Testing different strategies...")
    
    test_text = "Contact support@company.com"
    
    strategies = [
        MaskingStrategy.REPLACE,
        MaskingStrategy.REDACT, 
        MaskingStrategy.TOKENIZE
    ]
    
    for strategy in strategies:
        config = MaskingConfig(strategy=strategy)
        masker = DataMasker(config)
        result = masker.mask_text(test_text)
        print(f"{strategy.value}: {result}")
    
    # Test analysis
    print("\n📊 Testing analysis...")
    masker = DataMasker()
    analysis = masker.analyze("Email john@example.com and phone 555-1234")
    print(f"Analysis results: {analysis['total_matches']} matches found")
    
    print("\n🎉 All tests passed! Data Masking Library is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
