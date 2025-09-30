# CloudCurio Git Workflow and Branching Strategy

## Overview

This document describes the Git workflow and branching strategy for the CloudCurio project. The strategy is based on the GitFlow model with some adaptations for continuous delivery.

## Branching Strategy

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: Strict protection rules
- **Merges**: Only through pull requests with code review
- **Releases**: Tagged releases are created from this branch
- **CI/CD**: Full testing and security scanning

#### `develop`
- **Purpose**: Integration branch for features
- **Protection**: Moderately protected
- **Merges**: Feature branches merged here
- **CI/CD**: Testing pipeline runs

#### `release/*`
- **Purpose**: Prepare for releases
- **Naming**: `release/v1.2.3`
- **Lifecycle**: Created from `develop`, merged to `main` and `develop`, then deleted
- **CI/CD**: Full testing pipeline

#### `hotfix/*`
- **Purpose**: Emergency fixes for production
- **Naming**: `hotfix/issue-description`
- **Lifecycle**: Created from `main`, merged to `main` and `develop`, then deleted
- **CI/CD**: Full testing pipeline

### Supporting Branches

#### `feature/*`
- **Purpose**: New features and enhancements
- **Naming**: `feature/short-description` (e.g., `feature/ai-code-review`)
- **Source**: Branch from `develop`
- **Target**: Merge back to `develop`
- **Lifecycle**: Deleted after merging

#### `bugfix/*`
- **Purpose**: Non-critical bug fixes
- **Naming**: `bugfix/issue-description` (e.g., `bugfix/fix-login-issue`)
- **Source**: Branch from `develop`
- **Target**: Merge back to `develop`
- **Lifecycle**: Deleted after merging

#### `experiment/*`
- **Purpose**: Experimental features and spikes
- **Naming**: `experiment/feature-name` (e.g., `experiment/new-ml-model`)
- **Source**: Branch from `develop`
- **Target**: May be merged to `develop` or deleted
- **Lifecycle**: Variable

## Git Workflow

### Feature Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-awesome-feature
   ```

2. **Develop Feature**
   ```bash
   # Make changes
   git add .
   git commit -m "feat: Add awesome feature
   
   - Implement core functionality
   - Add unit tests
   - Update documentation"
   ```

3. **Push and Create Pull Request**
   ```bash
   git push origin feature/my-awesome-feature
   # Create PR on GitHub
   ```

4. **Code Review and Merge**
   - PR review process
   - Automated testing passes
   - Merge to `develop`

### Release Workflow

1. **Create Release Branch**
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v1.2.0
   ```

2. **Prepare Release**
   ```bash
   # Update version numbers
   # Update changelog
   # Final testing
   ```

3. **Merge to Main**
   ```bash
   git checkout main
   git pull origin main
   git merge --no-ff release/v1.2.0
   git tag -a v1.2.0 -m "Release version 1.2.0"
   git push origin main --tags
   ```

4. **Merge Back to Develop**
   ```bash
   git checkout develop
   git merge --no-ff release/v1.2.0
   git push origin develop
   ```

5. **Clean Up**
   ```bash
   git branch -d release/v1.2.0
   ```

### Hotfix Workflow

1. **Create Hotfix Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-security-issue
   ```

2. **Implement Fix**
   ```bash
   # Make minimal necessary changes
   git commit -m "fix: Critical security vulnerability"
   ```

3. **Merge to Main and Develop**
   ```bash
   # Merge to main
   git checkout main
   git merge --no-ff hotfix/critical-security-issue
   git tag -a v1.2.1 -m "Hotfix release v1.2.1"
   git push origin main --tags
   
   # Merge to develop
   git checkout develop
   git merge --no-ff hotfix/critical-security-issue
   git push origin develop
   ```

4. **Clean Up**
   ```bash
   git branch -d hotfix/critical-security-issue
   ```

## Commit Message Convention

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (no logic changes)
- `refactor`: Code changes that neither fix a bug nor add a feature
- `test`: Adding missing tests or correcting existing tests
- `chore`: Other changes that don't modify src or test files
- `perf`: Performance improvements
- `ci`: CI/CD configuration changes

### Scopes
- `ai`: AI tools and providers
- `crew`: Crew management system
- `mcp`: MCP server
- `sysmon`: System monitoring
- `config`: Configuration editor
- `agentic`: Agentic platform
- `tracking`: Feature tracking system
- `ci`: CI/CD configuration

### Examples
```
feat(ai): Add support for new AI provider OpenRouter

- Implement OpenRouter provider class
- Add secure credential storage
- Update provider manager
```

```
fix(crew): Fix memory leak in crew execution

- Fix resource cleanup in crew execution loop
- Add proper context management
- Update tests to verify fix
```

## Tagging Strategy

### Version Tags
- Format: `v{MAJOR}.{MINOR}.{PATCH}`
- Example: `v1.2.3`

### Pre-release Tags
- Format: `v{MAJOR}.{MINOR}.{PATCH}-{prerelease}.{number}`
- Examples: 
  - `v1.2.3-alpha.1`
  - `v1.2.3-beta.2`
  - `v1.2.3-rc.1`

### Component Tags
- Format: `{component}/v{version}`
- Examples:
  - `ai/v1.2.3`
  - `mcp/v1.2.3`
  - `sysmon/v1.2.3`

## Merge Strategies

### Pull Request Requirements
- All automated tests pass
- Code review approval (at least 1 reviewer)
- Documentation updates if needed
- Changelog entry for user-facing changes

### Merge Types
- **Squash and Merge**: For feature branches (clean history)
- **Create Merge Commit**: For release and hotfix branches (preserve branch history)
- **Rebase**: For small fixes, when appropriate

## Branch Protection Rules

### Main Branch
- Require pull request reviews
- Require status checks to pass
- Include administrators
- Allow force pushes: disabled
- Require linear history: enabled

### Develop Branch
- Require pull request reviews
- Require status checks to pass
- Allow force pushes: disabled for non-admins

## Workflow Automation

### GitHub Actions
- Automated testing on PRs
- Security scanning
- Code quality checks
- Package building and deployment
- Release automation

### Pre-commit Hooks
- Code formatting with Black
- Linting with Flake8
- Type checking with MyPy
- Security scanning with Bandit
- AI code review

## Merge Conflicts Resolution

### Process
1. Identify conflicting files
2. Pull latest changes from target branch
3. Resolve conflicts manually
4. Test thoroughly
5. Commit and push resolution

### Tools
```bash
# Identify conflicts
git status

# Pull latest changes
git pull origin develop

# Use merge tool
git mergetool

# Commit resolution
git commit -m "resolve: Merge conflicts with develop"
```

## Release Process

### Versioning
Follows Semantic Versioning 2.0.0:
- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Steps
1. Create release branch from `develop`
2. Update version numbers
3. Update changelog
4. Final testing
5. Merge to `main` with tag
6. Merge back to `develop`
7. Create GitHub release
8. Publish to package registries

## Emergency Procedures

### Hotfix Process
1. Create hotfix branch from `main`
2. Implement minimal fix
3. Thorough testing
4. Merge to `main` with version bump
5. Merge to `develop`
6. Create release
7. Communicate with stakeholders

### Rollback Process
1. Identify problematic commit
2. Create revert commit
3. Test rollback
4. Deploy rollback
5. Monitor systems
6. Plan permanent fix

This strategy ensures organized development while maintaining code quality and release stability.