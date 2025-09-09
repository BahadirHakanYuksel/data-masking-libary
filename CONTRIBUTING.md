# Contributing to Data Masking Library

Thank you for your interest in contributing to the Data Masking Library! This document provides guidelines for contributing to this open-source project.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/yourusername/data-masking-library.git
   cd data-masking-library
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**

   ```bash
   pip install -r requirements-dev.txt
   pip install -e .
   ```

4. **Install pre-commit hooks**
   ```bash
   pre-commit install
   ```

## 🔄 Development Workflow

### Making Changes

1. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**

   - Write clean, readable code
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run tests**

   ```bash
   pytest
   pytest --cov=src/data_masker  # With coverage
   ```

4. **Run linting and formatting**

   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add new masking strategy"
   ```

### Commit Message Format

We follow the [Conventional Commits](https://conventionalcommits.org/) specification:

- `feat:` new features
- `fix:` bug fixes
- `docs:` documentation changes
- `test:` adding or modifying tests
- `refactor:` code refactoring
- `perf:` performance improvements
- `chore:` maintenance tasks

Examples:

```
feat: add encryption masking strategy
fix: resolve email domain preservation issue
docs: update installation instructions
test: add tests for custom patterns
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/data_masker --cov-report=html

# Run specific test file
pytest tests/test_masker.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Aim for high test coverage (>90%)
- Use descriptive test names
- Include both positive and negative test cases
- Test edge cases and error conditions

Example test structure:

```python
class TestNewFeature:
    """Test cases for new feature."""

    def test_basic_functionality(self):
        """Test basic functionality works."""
        # Arrange
        masker = DataMasker()
        data = "test data"

        # Act
        result = masker.new_method(data)

        # Assert
        assert result is not None

    def test_edge_case(self):
        """Test edge case handling."""
        # Test implementation
        pass
```

## 📝 Code Style

### Python Style Guide

- Follow [PEP 8](https://peps.python.org/pep-0008/)
- Use [Black](https://black.readthedocs.io/) for code formatting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Use [mypy](https://mypy.readthedocs.io/) for type checking

### Code Organization

- Keep functions and classes focused and small
- Use descriptive names for variables and functions
- Add type hints to all public functions
- Write docstrings for all public classes and methods
- Use dataclasses or Pydantic models for structured data

### Documentation

- Use Google-style docstrings
- Include examples in docstrings where helpful
- Update README.md for significant changes
- Add inline comments for complex logic

Example docstring:

```python
def mask_data(self, data: str, strategy: str = "replace") -> str:
    """Mask PII in the provided data.

    Args:
        data: The input data to mask
        strategy: The masking strategy to use

    Returns:
        The masked data string

    Raises:
        ValueError: If strategy is not supported

    Example:
        >>> masker = DataMasker()
        >>> masker.mask_data("john@example.com")
        "████@example.com"
    """
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the bug
3. **Expected behavior** vs actual behavior
4. **Environment details** (Python version, OS, etc.)
5. **Sample code** that demonstrates the issue
6. **Error messages** or stack traces

Use this template:

````markdown
## Bug Description

Brief description of the bug.

## Steps to Reproduce

1. Step one
2. Step two
3. Step three

## Expected Behavior

What you expected to happen.

## Actual Behavior

What actually happened.

## Environment

- Python version: 3.9.0
- OS: Ubuntu 20.04
- Library version: 0.1.0

## Code Sample

```python
# Minimal code that reproduces the issue
```
````

```

## 💡 Feature Requests

When requesting features:

1. **Explain the use case** and problem it solves
2. **Describe the proposed solution**
3. **Consider alternatives** you've thought about
4. **Provide examples** of how it would be used

## 🔐 Security

If you discover a security vulnerability:

1. **Do not** create a public issue
2. **Email** the maintainers privately
3. **Include** details about the vulnerability
4. **Wait** for a response before public disclosure

## 📋 Pull Request Process

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted with Black
- [ ] Linting passes (flake8)
- [ ] Type checking passes (mypy)
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated (if applicable)

### PR Description

Include in your PR description:

- **Summary** of changes made
- **Motivation** for the changes
- **Testing** performed
- **Breaking changes** (if any)
- **Related issues** (if any)

### Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. Address any requested changes
4. Squash commits before merging (if requested)

## 🏷️ Release Process

Releases follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Documentation**: Check the docs first
- **Code of Conduct**: Be respectful and inclusive

## 🎯 Good First Issues

Look for issues labeled `good first issue` or `help wanted`. These are great starting points for new contributors.

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the Data Masking Library! 🙏
```
