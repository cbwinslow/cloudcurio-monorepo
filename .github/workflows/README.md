# CloudCurio GitHub Workflows

This directory contains all GitHub Actions workflows for the CloudCurio project.

## Workflow Overview

### Continuous Integration & Delivery (CI/CD)
- **File**: `cicd.yaml`
- **Triggers**: Push to `main`/`develop`/`release/*`, Pull Requests
- **Purpose**: Complete CI/CD pipeline including testing, security scanning, building, and deployment
- **Jobs**:
  - Code Quality Checks
  - Security Scanning
  - Unit Testing
  - Integration Testing
  - AI Code Review with Ollama
  - Build Packages
  - Release Management
  - Docker Hub Release
  - Notification

### Code Quality Checks
- **File**: `code-quality.yaml`
- **Triggers**: Push to `main`/`develop`, Pull Requests, Scheduled Weekly
- **Purpose**: Static analysis, linting, formatting, and type checking
- **Jobs**:
  - Linting with Flake8
  - Formatting with Black
  - Type checking with MyPy
  - Code analysis with Pylint

### Security Scanning
- **File**: `security-scan.yaml`
- **Triggers**: Push to `main`/`develop`, Pull Requests, Scheduled Daily
- **Purpose**: Security vulnerability scanning and dependency checking
- **Jobs**:
  - Bandit security scanning
  - Safety dependency vulnerability checking

### Automated Testing
- **File**: `testing.yaml`
- **Triggers**: Push to `main`/`develop`, Pull Requests, Scheduled Nightly
- **Purpose**: Comprehensive test suite execution
- **Jobs**:
  - Unit tests with multiple Python versions
  - Integration tests with database and Redis services
  - End-to-end tests

### Release Management
- **File**: `release.yaml`
- **Triggers**: Git tags (`v*`), Manual dispatch
- **Purpose**: Package building and publishing
- **Jobs**:
  - Create GitHub Release
  - Publish to PyPI
  - Publish to Docker Hub

### Documentation Generation
- **File**: `documentation.yaml`
- **Triggers**: Push to `main`/`develop`, Pull Requests
- **Purpose**: Auto-generate and deploy documentation
- **Jobs**:
  - Generate Sphinx documentation
  - Deploy to GitHub Pages

### Branch Management
- **File**: `branch-management.yaml`
- **Triggers**: Push to `develop`, Merged Pull Requests, Manual dispatch, Scheduled
- **Purpose**: Automated branch maintenance and cleanup
- **Jobs**:
  - Clean up merged branches
  - Configure branch protection rules
  - Sync branches
  - Notify about stale branches

## Workflow Details

### CI/CD Pipeline (`cicd.yaml`)

The main CI/CD pipeline includes comprehensive checks and validations:

1. **Code Quality Checks**
   - Multiple Python versions (3.10, 3.11)
   - Linting with Flake8
   - Code formatting with Black
   - Type checking with MyPy
   - Security scanning with Bandit
   - Dependency vulnerability scanning with Safety

2. **Testing**
   - Unit tests with pytest and coverage reporting
   - Integration tests with PostgreSQL and Redis services
   - Coverage upload to Codecov

3. **AI Code Review**
   - Local AI model (Ollama) for intelligent code review
   - Automated feedback on pull requests
   - Code quality and security analysis

4. **Building and Publishing**
   - Build Python packages (wheel and source distribution)
   - Build Docker images for multiple architectures
   - Publish to PyPI and Docker Hub
   - Create GitHub Releases

### Security Scanning (`security-scan.yaml`)

Daily security scanning to detect vulnerabilities:

1. **Static Analysis**
   - Bandit for Python security issues
   - Detection of common security pitfalls
   - High severity issue blocking

2. **Dependency Scanning**
   - Safety for vulnerable package versions
   - Scanning of all requirements files
   - Regular updates to vulnerability database

### Automated Testing (`testing.yaml`)

Comprehensive test coverage:

1. **Unit Testing**
   - Matrix testing across Python versions
   - Code coverage reporting
   - Fast feedback on code changes

2. **Integration Testing**
   - Database integration with PostgreSQL
   - Redis service for caching tests
   - Real service integration validation

3. **End-to-End Testing**
   - Browser automation with Selenium
   - Full application flow testing
   - User experience validation

### Release Management (`release.yaml`)

Automated release process:

1. **Package Building**
   - Semantic versioning compliance
   - Wheel and source distribution formats
   - Integrity checking

2. **Publication**
   - PyPI publishing with trusted publishing
   - Docker Hub multi-architecture images
   - GitHub Release creation with assets

## Configuration

### Secrets Required

The following secrets should be configured in the GitHub repository:

- `PYPI_API_TOKEN`: For PyPI publishing
- `DOCKER_USERNAME`: For Docker Hub publishing
- `DOCKER_PASSWORD`: For Docker Hub publishing
- `SLACK_WEBHOOK_URL`: For CI/CD notifications (optional)
- `DISCORD_WEBHOOK`: For CI/CD notifications (optional)

### Environment Variables

Key environment variables used in workflows:

- `OPENROUTER_API_KEY`: For AI provider testing
- `OPENAI_API_KEY`: For AI provider testing
- `GEMINI_API_KEY`: For AI provider testing

## Customization

### Adding New Workflows

To add a new workflow:

1. Create a new YAML file in this directory
2. Follow the naming convention `descriptive-name.yaml`
3. Use appropriate triggers and jobs
4. Include proper error handling and notifications
5. Document the workflow in this README

### Modifying Existing Workflows

When modifying workflows:

1. Test changes in a feature branch
2. Use workflow_dispatch for testing
3. Update this README with changes
4. Ensure backward compatibility
5. Monitor pipeline performance

## Monitoring and Alerts

### Notifications

Workflows include notification mechanisms:

- Slack alerts for failures
- Discord notifications for critical issues
- Email notifications through GitHub settings

### Performance Monitoring

Workflow performance is monitored through:

- Execution time tracking
- Resource usage monitoring
- Success/failure rate analysis

## Best Practices

### Workflow Design

1. **Keep workflows focused**: Each workflow should have a single responsibility
2. **Use caching**: Cache dependencies to speed up builds
3. **Fail fast**: Order jobs to fail early on critical issues
4. **Use matrix builds**: Test across multiple environments
5. **Include cleanup**: Remove artifacts and temporary files

### Security Considerations

1. **Least privilege**: Grant minimum required permissions
2. **Secrets management**: Never hardcode sensitive information
3. **Dependency scanning**: Regular security audits
4. **Code review**: All workflow changes require review
5. **Audit logging**: Maintain logs of workflow executions

### Performance Optimization

1. **Parallel execution**: Use matrix builds where possible
2. **Caching**: Cache dependencies and build artifacts
3. **Selective triggering**: Use paths and branch filters
4. **Resource allocation**: Match job requirements to runners
5. **Cleanup**: Remove unnecessary files and artifacts

This comprehensive workflow system ensures CloudCurio maintains high code quality, security, and reliability while enabling rapid development and deployment.