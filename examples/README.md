# Examples

This directory contains example scripts and data files demonstrating how to use the Data Masking Library.

## Basic Examples

### 1. Simple Text Masking

```python
from data_masker import DataMasker

# Basic masking
masker = DataMasker()
text = "Contact John Doe at john.doe@company.com or call +1-555-123-4567"
masked = masker.mask_text(text)
print(masked)
# Output: Contact ████ ███ at ████████@company.com or call +1-███-███-████
```

### 2. Dictionary Masking

```python
from data_masker import DataMasker

data = {
    "users": [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "ssn": "123-45-6789",
            "phone": "(555) 987-6543"
        }
    ]
}

masker = DataMasker()
masked_data = masker.mask(data)
print(masked_data)
```

### 3. Different Masking Strategies

```python
from data_masker import DataMasker, MaskingConfig, MaskingStrategy

# Redaction strategy
config = MaskingConfig(strategy=MaskingStrategy.REDACT)
masker = DataMasker(config)
result = masker.mask_text("Email: user@domain.com")
print(result)  # Email: [REDACTED]

# Faker strategy
config = MaskingConfig(strategy=MaskingStrategy.FAKER)
masker = DataMasker(config)
result = masker.mask_text("Email: user@domain.com")
print(result)  # Email: synthetic.email@example.org

# Tokenization strategy
config = MaskingConfig(strategy=MaskingStrategy.TOKENIZE)
masker = DataMasker(config)
result = masker.mask_text("Email: user@domain.com")
print(result)  # Email: [EMAIL_TOKEN_1234]
```

## File Examples

Run the example scripts:

```bash
python examples/basic_usage.py
python examples/csv_masking.py
python examples/json_masking.py
```
