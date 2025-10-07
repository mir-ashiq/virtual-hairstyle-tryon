# Contributing to Virtual Hairstyle Try-On

Thank you for considering contributing to this project!

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Your environment details

### Suggesting Enhancements

1. Check if the enhancement has been suggested
2. Create a new issue with:
   - Clear use case description
   - Expected behavior
   - Why this would be useful
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Follow the code style guidelines
5. Add tests if applicable
6. Update documentation
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/mir-ashiq/virtual-hairstyle-tryon.git
cd virtual-hairstyle-tryon

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python tests/run_tests.py
```

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use type hints where possible
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to all public functions and classes

### Code Formatting

We use automated tools for code formatting:

```bash
# Format code with black
black src/ tests/ app_enhanced.py

# Sort imports with isort
isort src/ tests/ app_enhanced.py

# Check code quality with flake8
flake8 src/ tests/ app_enhanced.py
```

### Documentation

- Update README.md if adding features
- Add docstrings to new functions/classes
- Update API documentation for interface changes
- Include inline comments for complex logic

## Testing

### Writing Tests

- Add tests for new features
- Follow existing test structure
- Use descriptive test names
- Test edge cases and error conditions

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python -m unittest tests/test_validators.py

# Run with coverage
coverage run -m unittest discover tests/
coverage report
```

## Project Structure

```
virtual-hairstyle-tryon/
├── src/
│   ├── config/          # Configuration management
│   ├── models/          # AI model implementations
│   ├── services/        # Business logic
│   └── utils/           # Utility functions
├── tests/              # Test suite
├── docs/               # Documentation
├── hairstyles/         # Hairstyle gallery
├── examples/           # Example images
└── app_enhanced.py     # Main application
```

## Commit Message Guidelines

Format: `<type>: <description>`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat: Add batch processing support
fix: Resolve image validation error
docs: Update API documentation
test: Add tests for image processor
```

## Review Process

1. Automated checks run on all PRs
2. Code review by maintainers
3. Tests must pass
4. Documentation must be updated
5. No merge conflicts

## Adding New Features

### New Model Support

1. Extend `BaseModel` class
2. Implement required methods
3. Add tests
4. Update documentation
5. Add example usage

### New Service Features

1. Add to appropriate service class
2. Follow service layer pattern
3. Add validation
4. Include error handling
5. Add tests

### UI Enhancements

1. Update `app_enhanced.py`
2. Follow existing UI patterns
3. Test across browsers
4. Update screenshots
5. Document new features

## Questions?

- Open an issue for questions
- Check existing documentation
- Review closed issues for similar questions

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

Thank you for contributing! 🎉
