# CloudCurio Git Workflow: Branching and Tagging Strategy

## Overview

This document outlines the Git branching and tagging strategy for the CloudCurio monorepo. The strategy ensures organized development, clear versioning, and proper release management across all platform components.

## Repository Structure

The CloudCurio repository follows a monorepo architecture:

```
cloudcurio/
├── crew/                    # AI crew management
├── ai_tools/               # Multi-provider AI integration  
├── sysmon/                 # System monitoring
├── config_editor/          # Web-based configuration editor
├── agentic_platform/       # Multi-agent system
├── feature_tracking/       # Feature usage tracking
├── container/              # Docker configurations
├── docs/                   # Documentation
├── examples/               # Examples and tutorials
├── tests/                  # Test suites
├── scripts/                # Utility scripts
├── releases/               # Release artifacts
└── ...
```

## Branching Strategy

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **State**: Always deployable
- **Access**: Protected branch (requires PR approval)
- **Merge Policy**: Through pull requests only
- **CI/CD**: Full testing pipeline triggers

#### `develop` 
- **Purpose**: Integration branch for features
- **State**: Ready for next release
- **Merge Policy**: Feature branches merge here
- **CI/CD**: Testing pipeline triggers

### Supporting Branches

#### `feature/*`
- **Naming**: `feature/short-description` (e.g., `feature/ai-provider-integration`)
- **Source**: Branch from `develop`
- **Target**: Merge back to `develop`
- **Naming Convention**: Use kebab-case
- **Lifecycle**: Deleted after merging

#### `release/*` 
- **Naming**: `release/vX.Y.Z` (e.g., `release/v2.1.0`)
- **Source**: Branch from `develop`
- **Purpose**: Prepare for release
- **Target**: Merge to `main` and back to `develop`
- **Lifecycle**: Deleted after release

#### `hotfix/*`
- **Naming**: `hotfix/issue-description` (e.g., `hotfix/critical-security-fix`)
- **Source**: Branch from `main` (or latest release tag)
- **Target**: Merge to both `main` and `develop`
- **Purpose**: Critical fixes for production

#### `enhancement/*`
- **Naming**: `enhancement/description` (e.g., `enhancement/feature-tracking-system`)
- **Source**: Branch from `develop`
- **Target**: Merge back to `develop`
- **Purpose**: Major new functionality

## Tagging Strategy

### Version Tags

#### Semantic Versioning: `v{MAJOR}.{MINOR}.{PATCH}`

- **MAJOR**: Breaking changes, significant rewrites
- **MINOR**: New features, enhancements  
- **PATCH**: Bug fixes, patches

**Examples**:
- `v1.0.0` - Initial release
- `v1.1.0` - New features added
- `v1.1.1` - Bug fix release
- `v2.0.0` - Breaking changes or major rewrite

#### Pre-release Tags

- `vX.Y.Z-alpha.N` - Alpha releases (early testing)
- `vX.Y.Z-beta.N` - Beta releases (feature complete, testing)
- `vX.Y.Z-rc.N` - Release candidates (stable, final testing)

### Component-Specific Tags

#### For Monorepo Components
- `crew/vX.Y.Z` - Specific crew component versions
- `ai/vX.Y.Z` - AI tools component versions
- `sysmon/vX.Y.Z` - SysMon component versions
- `mcp/vX.Y.Z` - MCP server component versions

## Git Workflow

### Feature Development

1. **Create Feature Branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/my-feature
   ```

2. **Develop and Commit**:
   ```bash
   # Make changes
   git add .
   git commit -m "feat: Add new AI provider integration
   
   - Implement OpenRouter provider
   - Add secure credential storage
   - Update provider manager"
   ```

3. **Push and Create PR**:
   ```bash
   git push origin feature/my-feature
   # Create PR to develop branch
   ```

4. **Code Review and Merge**:
   - PR review process
   - Automated testing passes
   - Merge to develop branch

### Release Process

1. **Start Release Branch**:
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b release/v2.1.0
   ```

2. **Update Version**:
   ```bash
   # Update version in setup.py, package files, etc.
   python scripts/release_manager.py bump --part minor
   ```

3. **Final Testing**:
   - Run full test suite
   - Manual testing as needed
   - Update documentation

4. **Merge to Main**:
   ```bash
   git checkout main
   git pull origin main
   git merge --no-ff release/v2.1.0
   git tag -a v2.1.0 -m "Release version 2.1.0"
   git push origin main --tags
   ```

5. **Merge Back to Develop**:
   ```bash
   git checkout develop
   git merge --no-ff release/v2.1.0
   git push origin develop
   ```

6. **Clean Up**:
   ```bash
   git branch -d release/v2.1.0
   ```

### Hotfix Process

1. **Create Hotfix Branch**:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b hotfix/critical-bug-fix
   ```

2. **Implement Fix**:
   ```bash
   # Make minimal necessary changes
   git commit -m "fix: Critical security vulnerability
   
   - Fix buffer overflow in input validation
   - Add input sanitization
   - Related to #1234"
   ```

3. **Update Version**:
   ```bash
   # Increment patch version
   python scripts/release_manager.py bump --part patch
   ```

4. **Merge to Main**:
   ```bash
   git checkout main
   git merge --no-ff hotfix/critical-bug-fix
   git tag -a v2.1.1 -m "Hotfix release v2.1.1"
   git push origin main --tags
   ```

5. **Merge to Develop**:
   ```bash
   git checkout develop
   git merge --no-ff hotfix/critical-bug-fix
   git push origin develop
   ```

## Commit Message Conventions

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
- Update CLI tool
- Update documentation
```

```
fix(crew): Fix memory leak in crew execution

- Fix resource cleanup in crew execution loop
- Add proper context management
- Update tests to verify fix
- Related to issue #456
```

## Tagging Best Practices

### When to Create Tags
- Each production release
- Significant milestones
- Major feature completions
- Critical bug fixes

### Tag Messages
- Use annotated tags: `git tag -a v1.0.0 -m "Release message"`
- Include release highlights
- Mention breaking changes if any
- Reference related issues

### Example Tag Creation
```bash
git tag -a v2.0.0 -m "Release version 2.0.0

Major features:
- Agentic platform with multi-agent support
- Comprehensive feature tracking system
- Advanced AI provider integration
- Improved MCP server performance

Breaking changes:
- Updated API endpoints
- Changed configuration format

Fixed issues:
- #123 - Memory leak in crew execution
- #456 - Security vulnerability in authentication"
```

## Release Automation

### Scripts Used
- `scripts/release_manager.py` - Version bumping and release management
- `Makefile` - Build and packaging automation
- `.github/workflows/cicd.yml` - CI/CD pipeline
- `.gitlab-ci.yml` - GitLab CI pipeline

### Automated Tasks
- Version bumping
- Git tagging
- Changelog generation
- Package building
- PyPI publishing
- Docker image building and pushing
- GitHub release creation

## Merge Strategies

### Pull Request Requirements
- All automated tests pass
- Code review approval (at least 1 reviewer)
- Documentation updates if needed
- Changelog entry for user-facing changes
- Branch up-to-date with target branch

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

### GitLab CI
- Parallel testing pipelines
- Container security scanning
- Performance testing
- Automated tagging

## Versioning Strategy

### Semantic Versioning Guidelines

#### MAJOR version when:
- Breaking API changes
- Major architectural changes
- Removal of features
- Significant performance changes

#### MINOR version when:
- New features added
- Backward-compatible functionality
- Non-breaking changes
- New provider integrations

#### PATCH version when:
- Bug fixes
- Security patches
- Performance improvements
- Documentation updates

### Component-Specific Versioning
- Monorepo version applies to entire platform
- Individual components can have their own semantic versioning
- Feature tracking system: `feature_tracking/v1.0.0`
- AI tools: `ai/v2.1.0`

## Documentation Versioning

- Documentation tagged with code releases
- API documentation generated with each release
- User guides updated with new features
- Breaking changes clearly documented

## Branch Cleanup

### Automated Cleanup
- Feature branches deleted after merge (GitHub setting)
- Release branches deleted after merge
- PR branches cleaned up automatically

### Manual Cleanup
```bash
# Clean up local branches
git fetch --prune
git branch --merged | grep -v main | grep -v develop | xargs git branch -d
```

## Emergency Procedures

### Hotfix Protocol
- Critical bugs: Use hotfix branch from main
- Security vulnerabilities: Immediate patch
- Rollback procedures: Documented and tested
- Communication: Stakeholders notified immediately

### Release Rollback
- Tag the old version as latest if needed
- Create hotfix to address issues
- Update documentation with rollback instructions
- Monitor systems post-rollback

This strategy ensures organized development while maintaining code quality and release stability across the CloudCurio monorepo.