# Contributing to CloudCurio

Thank you for your interest in contributing to CloudCurio! We welcome contributions from the community and are excited to work with you to make this project even better.

## Table of Contents
1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Style](#code-style)
4. [Testing](#testing)
5. [Documentation](#documentation)
6. [Issue Reporting](#issue-reporting)
7. [Pull Request Process](#pull-request-process)
8. [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites
- Python 3.10+
- Git
- Docker (for containerized development)
- Node.js (for UI components, if applicable)

### Initial Setup
1. Fork the repository on GitHub
2. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cloudcurio.git
   cd cloudcurio
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/cbwinslow/cloudcurio.git
   ```
4. Install dependencies:
   ```bash
   pip install -r crew/requirements.txt
   pip install -r config_editor/requirements.txt
   ```

## Development Workflow

### Branch Management
- Create feature branches from `develop` (main development branch)
- Use descriptive branch names: `feature/add-openai-provider`, `bugfix/sysmon-crash`
- Keep branches small and focused
- Rebase regularly on `develop` to keep up to date

### Local Development
1. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name develop
   ```
2. Make your changes
3. Test your changes thoroughly
4. Commit your changes:
   ```bash
   git add .
   git commit -m "feat: Add new AI provider integration
   - Implement OpenAI provider class
   - Add secure credential storage
   - Update provider manager
   - Update documentation"
   ```
5. Push your branch:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

### Python
- Follow PEP 8 style guide
- Use type hints for all function signatures
- Aim for 100 character line length
- Use descriptive variable and function names
- Write docstrings for all public functions and classes
- Use f-strings for string formatting
- Import statements at the top of the file

### Example Python Style
```python
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class AIProviderConfig:
    """Configuration for an AI provider."""
    
    name: str
    api_key: str
    base_url: Optional[str] = None
    default_model: str = "gpt-4"

def get_model_list(provider_config: AIProviderConfig) -> List[str]:
    """Get available models for the provider.
    
    Args:
        provider_config: Configuration for the AI provider
        
    Returns:
        List of available model names
    """
    # Implementation here
    pass
```

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters or less
- Reference relevant issue numbers when applicable

### Branch Names
- Use kebab-case: `feature/user-authentication`
- Prefix with type: `feature/`, `bugfix/`, `refactor/`, `docs/`, `test/`

## Testing

### Test Framework
- Use pytest for Python testing
- Place tests in `tests/` directory
- Use descriptive test names
- Test edge cases and error conditions
- Maintain high code coverage

### Running Tests
```bash
# Run all tests
pytest

# Run tests for a specific module
pytest tests/test_ai_providers.py

# Run with coverage
pytest --cov=.
```

## Documentation

### Code Documentation
- Write clear docstrings for all functions, classes, and modules
- Use Google or NumPy style docstrings
- Document all parameters, return values, and exceptions
- Update documentation when making changes

### External Documentation
- Update README files when adding new features
- Add examples to the examples repository
- Update procedure handbook for new workflows
- Create/update API documentation

## Issue Reporting

### Bug Reports
When reporting bugs, please include:
- Clear title and description
- Steps to reproduce
- Expected behavior vs actual behavior
- Environment information (OS, Python version, etc.)
- Relevant logs or error messages
- Screenshots if applicable

### Feature Requests
When requesting features, please include:
- Clear description of the requested feature
- Use cases and benefits
- Potential implementation approaches
- Related issues or discussions

## Pull Request Process

### Before Submitting
1. Ensure your code follows the style guidelines
2. Run all tests and ensure they pass
3. Add tests for new functionality
4. Update documentation as needed
5. Squash commits if necessary
6. Ensure your PR description clearly explains what you've done

### Submitting a PR
1. Push your branch to your fork
2. Open a PR to the `develop` branch
3. Follow the PR template
4. Include screenshots if applicable
5. Link related issues
6. Request reviews from maintainers

### PR Review Process
- PRs require at least one approval
- Maintainers may request changes
- PRs should be up to date with `develop`
- Documentation and tests are required for new features
- Changes should be small and focused

## Community Guidelines

### Code of Conduct
- Be respectful and inclusive
- Provide constructive feedback
- Be patient with new contributors
- Help others learn
- Focus on the technical aspects

### Communication
- Use professional language
- Be specific and clear
- Provide context when asking for help
- Follow up on discussions
- Keep conversations on topic

## Areas for Contribution

### High Priority
- Performance improvements
- Security enhancements
- Documentation improvements
- Test coverage expansion
- New AI provider integrations

### Good First Issues
- Documentation updates
- Bug fixes for existing features
- Minor enhancements
- Test improvements
- UI/UX improvements

### Advanced Contributions
- New feature implementations
- Architecture improvements
- Performance optimizations
- Security hardening
- DevOps and deployment improvements

## Recognition

We appreciate all contributions, big and small. Contributors will be:
- Added to the contributors list in the README
- Mentioned in release notes when appropriate
- Given credit for significant contributions
- Welcomed as community members

## Questions?

If you have questions about contributing:
- Check the existing issues and discussions
- Ask in a new issue if you can't find an answer
- Join us in community discussions
- Email the maintainers if needed

Thank you for contributing to CloudCurio!