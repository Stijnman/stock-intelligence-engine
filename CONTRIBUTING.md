# Contributing Guide

Thank you for your interest in contributing to **stock-intelligence-engine**! 
This document outlines how to contribute new features, improve existing ones, and help maintain this repository.

---

## 📋 Table of Contents

- [Code of Conduct](#-code-of-conduct)
- [How to Contribute](#-how-to-contribute)
- [Adding a New Feature](#-adding-a-new-feature)
- [Improving Existing Features](#-improving-existing-features)
- [Testing Requirements](#-testing-requirements)
- [Pull Request Process](#-pull-request-process)
- [Commit Message Guidelines](#-commit-message-guidelines)
- [Review Process](#-review-process)
- [Maintenance](#-maintenance)

---

## 🤝 Code of Conduct

By participating in this project, you agree to abide by the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). 
We are committed to providing a welcoming and inspiring community for all.

---

## 🚀 How to Contribute

### Reporting Bugs

If you find a bug, please [open an issue](https://github.com/Stijnman/stock-intelligence-engine/issues/new) with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Data provider involved (if applicable)
- Any error messages
- Screenshot or output (if applicable)

### Suggesting Enhancements

For feature requests or improvements:
1. Check existing issues for duplicates
2. Open a new issue with:
   - Detailed description of the enhancement
   - Use case or problem it solves
   - Proposed solution (if you have one)

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests (see [Testing Requirements](#-testing-requirements))
5. Commit your changes
6. Push to your fork
7. Open a Pull Request

---

## ✨ Adding a New Feature

### Before You Start

1. **Check for duplicates**: Search existing features to ensure the capability isn't already covered
2. **Verify data availability**: Ensure the required financial data is available from providers
3. **Review compliance**: Confirm the feature complies with data provider terms of service
4. **Test manually**: Verify the feature works with available data

### Directory Structure

```
stock-intelligence-engine/
├── [existing files...]
└── new_feature/
    ├── __init__.py
    ├── module.py          # Main feature code
    ├── tests/
    │   └── test_feature.py # Feature tests
    └── README.md         # Feature documentation
```

### Feature Requirements

Every new feature **MUST** include:

1. **Module docstring**: Clear description of what the feature does
2. **Function docstrings**: All public functions documented
3. **Type hints**: All function parameters and return types
4. **Examples**: Usage examples in docstrings or README
5. **Configuration**: Document required configuration

---

## 🔧 Improving Existing Features

### Before Submitting Changes

1. **Verify the issue**: Ensure the change addresses a real problem or improvement
2. **Check existing PRs**: Avoid duplicate work
3. **Test locally**: Verify your changes work as expected

### Types of Improvements

- Fix typos or unclear language
- Add missing examples
- Clarify ambiguous instructions
- Add warnings or notes
- Add new data provider support
- Update deprecated API endpoints
- Improve error handling
- Add input validation
- Optimize performance
- Enhance calculation accuracy

---

## 🧪 Testing Requirements

All contributions **MUST** include testing. At minimum:

### Manual Testing Checklist

- [ ] Feature works with valid inputs
- [ ] Feature handles invalid inputs gracefully
- [ ] All error cases are handled
- [ ] Rate limiting is respected
- [ ] Input validation works correctly

### Automated Testing (Recommended)

Create a `tests/test_feature.py` file with:

```python
import pytest
from your_feature import YourClass

class TestYourFeature:
    @pytest.fixture
    def setup(self):
        pass
    
    def test_basic_functionality(self, setup):
        pass
```

---

## 📤 Pull Request Process

### 1. Fork and Branch

```bash
git clone https://github.com/YOUR_USERNAME/stock-intelligence-engine.git
cd stock-intelligence-engine
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Follow coding standards
- Add documentation
- Include tests

### 3. Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
feat: add new technical indicator for RSI
fix: correct SMA calculation edge case
```

**Guidelines:**
- Use present tense
- Limit first line to 50 characters
- Separate subject from body with blank line
- Wrap body at 72 characters

### 4. Push Changes

```bash
git push origin feature/your-feature-name
```

### 5. Open Pull Request

1. Go to https://github.com/Stijnman/stock-intelligence-engine
2. Click "New Pull Request"
3. Select your fork and feature branch
4. Fill in PR template
5. Click "Create Pull Request"

---

## 👀 Pull Request Template

```markdown
## Description

[Clear description of the changes]

## Related Issues

[Link to any related issues]

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Security improvement
- [ ] Performance improvement
- [ ] Code refactoring
- [ ] Test addition/improvement
- [ ] Dependency update

## Testing

- [ ] Manual testing completed
- [ ] All error cases tested
- [ ] Unit tests added
- [ ] Integration tests pass

## Checklist

- [ ] Code follows repository standards
- [ ] I have read CONTRIBUTING.md
- [ ] Documentation added
- [ ] All tests pass
- [ ] No sensitive data
- [ ] Version numbers updated
```

---

## 🔍 Review Process

1. **Automated Checks**: CI pipeline runs tests, linting, and security scans
2. **Maintainer Review**: Repository maintainer reviews the PR
3. **Feedback**: You may receive requests for changes
4. **Approval**: PR is approved and merged

### Review Criteria

- [ ] Follows repository standards
- [ ] Clear and readable
- [ ] Well-documented
- [ ] Handles errors appropriately
- [ ] No hardcoded credentials
- [ ] Input validation implemented
- [ ] Existing tests still pass

---

## 🛠️ Maintenance

### Versioning

- `MAJOR`: Breaking changes
- `MINOR`: New features, backwards compatible
- `PATCH`: Bug fixes and documentation updates

### Releases

Releases are created periodically with changelog updates.

---

*Thank you for contributing!*

*Last updated: September 11, 2026*
