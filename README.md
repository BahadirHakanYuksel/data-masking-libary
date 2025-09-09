# Open Source Data Masking Library

A comprehensive Python library for automatically masking personal information in test data, ensuring data privacy and compliance with regulations like GDPR, HIPAA, and CCPA.

## 🎯 Features

- **Automatic PII Detection**: Detects and masks names, ID numbers, addresses, phone numbers, emails, and more
- **Multiple Masking Strategies**: Replace, redact, encrypt, or tokenize sensitive data
- **Format Preservation**: Maintains data structure and format while masking content
- **Custom Rules**: Define your own masking patterns and rules
- **Multiple Data Sources**: Support for JSON, CSV, XML, databases, and text files
- **High Performance**: Optimized for large datasets
- **Easy Integration**: Simple API for seamless integration into existing workflows

## 🚀 Quick Start

```python
from data_masker import DataMasker

# Initialize the masker
masker = DataMasker()

# Mask a dictionary
data = {
    "name": "John Doe",
    "ssn": "123-45-6789",
    "email": "john.doe@email.com",
    "phone": "+1-555-123-4567"
}

masked_data = masker.mask(data)
print(masked_data)
# Output: {
#     "name": "████ ███",
#     "ssn": "███-██-████",
#     "email": "████████@████.com",
#     "phone": "+1-███-███-████"
# }
```

## 📦 Installation

```bash
pip install data-masking-library
```

## 🛠️ Development Setup

```bash
# Clone the repository
git clone https://github.com/yourusername/data-masking-library.git
cd data-masking-library

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linting
flake8 src/
black src/
```

## 📋 Supported Data Types

- **Names**: First names, last names, full names
- **Identification**: SSN, driver's license, passport numbers
- **Contact Info**: Email addresses, phone numbers, addresses
- **Financial**: Credit card numbers, bank account numbers
- **Medical**: Patient IDs, medical record numbers
- **Custom Patterns**: Regular expressions for domain-specific data

## 🔧 Configuration

```python
from data_masker import DataMasker, MaskingConfig

config = MaskingConfig(
    strategy="replace",  # replace, redact, encrypt, tokenize
    preserve_format=True,
    custom_patterns={
        "employee_id": r"EMP\d{6}"
    }
)

masker = DataMasker(config)
```

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [Email Phishing Detection Tool](../email-phishing-detector/)
- [Job Posting Analysis Platform](../job-posting-analyzer/)
- [API Documentation Generator](../api-doc-generator/)
- [Digital Footprint Mapper](../digital-footprint-mapper/)

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=BahadirHakanYuksel/data-masking-library&type=Date)](https://star-history.com/#yourusername/data-masking-library&Date)

---

Built with ❤️ by the open-source community
