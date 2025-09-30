# Contributing to CloudCurio

We love your input! We want to make contributing to CloudCurio as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## We Develop with Github

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## We Use [Github Flow](https://guides.github.com/introduction/flow/index.html)

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `develop`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using Github's [issues](https://github.com/cbwinslow/cloudcurio-monorepo/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/cbwinslow/cloudcurio-monorepo/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can.
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

People *love* thorough bug reports. I'm not even kidding.

## Use a Consistent Coding Style

We use several tools to maintain code quality and consistency:

### Code Formatting
- [Black](https://black.readthedocs.io/) for automatic code formatting
- Line length: 88 characters (default Black setting)
- Double quotes for strings

### Linting
- [Flake8](https://flake8.pycqa.org/) for code linting
- Follow PEP 8 style guidelines
- Import order: Standard library, third-party, first-party

### Type Hinting
- [MyPy](http://mypy-lang.org/) for static type checking
- Use type hints for all function signatures
- Include return type annotations

### Documentation
- [Sphinx](https://www.sphinx-doc.org/) for documentation generation
- Google-style docstrings
- Include examples in docstrings when appropriate
- Update README.md and other documentation files

## License

By contributing, you agree that your contributions will be licensed under its MIT License.

## References

This document was adapted from the open-source contribution guidelines for [Facebook's Draft](https://github.com/facebook/draft-js/blob/a9316a723f9e918af3e794e03df812cac6ddfe55/CONTRIBUTING.md).

## Development Process

### Setting Up Your Development Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/your-username/cloudcurio-monorepo.git
   cd cloudcurio-monorepo
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   make install-dev
   ```

4. Set up pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

We use pytest for testing. Run the full test suite:

```bash
make test
```

Or run specific test categories:

```bash
make test-unit
make test-integration
make test-e2e
```

### Code Quality Checks

Ensure your code passes all quality checks:

```bash
make check
```

This runs:
- Black formatting check
- Flake8 linting
- MyPy type checking
- Bandit security scanning
- Safety dependency vulnerability scanning

### Making Changes

1. Create a feature branch from `develop`:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit them:
   ```bash
   git add .
   git commit -m "feat: Add your feature description

   - Implement core functionality
   - Add unit tests
   - Update documentation"
   ```

3. Push your branch and create a pull request:
   ```bash
   git push origin feature/your-feature-name
   ```

### Pull Request Process

1. Ensure any install or build dependencies are removed before the end of the layer when doing a build.
2. Update the README.md with details of changes to the interface, this includes new environment variables, exposed ports, useful file locations and container parameters.
3. Increase the version numbers in any examples files and the README.md to the new version that this Pull Request would represent. The versioning scheme we use is [SemVer](http://semver.org/).
4. You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Code Review Process

All submissions require review. We use GitHub pull requests for this purpose. Consult [GitHub Help](https://help.github.com/articles/about-pull-requests/) for more information on using pull requests.

### Community and Behavioral Expectations

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Development Guidelines

### Branch Naming Convention

Use descriptive branch names:
- `feature/descriptive-feature-name`
- `bugfix/issue-description`
- `hotfix/critical-fix-description`
- `experiment/exploratory-work-name`

### Commit Message Convention

Follow conventional commit messages:
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no logic changes)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Other changes that don't modify src or test files
- `perf`: Performance improvements
- `ci`: CI/CD configuration changes

### Documentation Standards

#### Docstrings
Use Google-style docstrings:
```python
def example_function(param1: str, param2: Optional[int] = None) -> bool:
    """Example function with types documented in the docstring.

    Args:
        param1: The first parameter.
        param2: The second parameter. Defaults to None.

    Returns:
        True if successful, False otherwise.

    Raises:
        ValueError: If param1 is invalid.
    """
    if not param1:
        raise ValueError("param1 cannot be empty")
    return True
```

#### README Updates
Always update README.md when making user-facing changes:
- New features
- API changes
- Configuration updates
- Installation process changes

### Testing Guidelines

#### Unit Tests
- Test individual functions and classes
- Mock external dependencies
- Aim for >80% code coverage
- Test edge cases and error conditions

#### Integration Tests
- Test service interactions
- Use actual databases and external services
- Test complete workflows
- Include setup and teardown

#### End-to-End Tests
- Test complete user journeys
- Use real browsers with Selenium
- Include happy path and error scenarios
- Test accessibility and usability

### Security Considerations

#### Credential Handling
- Never hardcode secrets
- Use environment variables or secure storage
- Encrypt sensitive data at rest
- Rotate credentials regularly

#### Input Validation
- Validate all user inputs
- Sanitize data before processing
- Use parameterized queries for databases
- Implement rate limiting

#### Dependency Management
- Regularly update dependencies
- Use safety to scan for vulnerabilities
- Pin versions in requirements files
- Review license compatibility

### Performance Guidelines

#### Code Optimization
- Profile code to identify bottlenecks
- Use appropriate data structures
- Minimize I/O operations
- Cache expensive computations

#### Memory Management
- Avoid memory leaks
- Use context managers for resource management
- Close files and connections properly
- Monitor memory usage in long-running processes

#### Scalability
- Design for horizontal scaling
- Use connection pooling
- Implement proper error handling
- Plan for load distribution

### Accessibility Guidelines

#### Code Readability
- Use descriptive variable and function names
- Include meaningful comments
- Follow consistent naming conventions
- Break complex logic into smaller functions

#### Documentation
- Write clear documentation
- Include code examples
- Provide troubleshooting guides
- Update documentation with code changes

## Getting Help

If you need help with your contribution:

1. Check the existing [issues](https://github.com/cbwinslow/cloudcurio-monorepo/issues) and [pull requests](https://github.com/cbwinslow/cloudcurio-monorepo/pulls)
2. Join our [Discord server](link-to-discord) (if available)
3. Email the maintainers at [maintainer-email]
4. Ask questions in new issues

## Recognition

Contributions to CloudCurio are recognized in several ways:

1. **GitHub Contributions**: All contributors appear in the GitHub contributor graph
2. **Release Notes**: Significant contributions are mentioned in release notes
3. **Contributors List**: Major contributors are added to the CONTRIBUTORS file
4. **Special Mentions**: Outstanding contributions may receive special recognition

We appreciate all contributions, big and small, and thank you for helping make CloudCurio better for everyone!