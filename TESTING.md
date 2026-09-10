# Testing Guide

This document outlines the testing requirements and best practices for the **stock-intelligence-engine** project.

---

## 📋 Table of Contents

- [Testing Philosophy](#-testing-philosophy)
- [Testing Levels](#-testing-levels)
- [Manual Testing](#-manual-testing)
- [Automated Testing](#-automated-testing)
- [Test Environments](#-test-environments)
- [Test Data Management](#-test-data-management)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Test Checklists](#-test-checklists)

---

## 🎯 Testing Philosophy

### Core Principles

1. **Safety First**: Never test with production credentials or real money
2. **Isolation**: Each test should be independent and not affect others
3. **Reproducibility**: Tests should produce consistent results
4. **Coverage**: Test both happy paths and error cases
5. **Documentation**: All tests should be documented and maintainable
6. **Paper Trading**: Always use simulated/sandbox environments for trading

### What Must Be Tested

Every component **MUST** be tested for:
- ✅ Data accuracy and validation
- ✅ API connectivity and error handling
- ✅ Input validation and sanitization
- ✅ Rate limiting behavior
- ✅ Authentication and authorization
- ✅ Security considerations
- ✅ Financial calculations accuracy
- ✅ Performance under load

---

## 🏗️ Testing Levels

### Level 1: Unit Testing (Recommended)

Test individual functions and components in isolation.

**Example**: Testing financial calculation functions
```python
# tests/test_calculations.py
import pytest
from stock_intelligence_engine import calculate_pnl, calculate_sma

def test_calculate_pnl_basic():
    """Test profit and loss calculation"""
    entry_price = 100
    exit_price = 150
    quantity = 10
    assert calculate_pnl(entry_price, exit_price, quantity) == 500

def test_calculate_pnl_loss():
    """Test PnL with loss"""
    entry_price = 100
    exit_price = 80
    quantity = 10
    assert calculate_pnl(entry_price, exit_price, quantity) == -200

def test_calculate_sma():
    """Test simple moving average"""
    prices = [10, 12, 15, 14, 16]
    assert calculate_sma(prices, 3) == [12.33, 13.67, 15.00]
```

### Level 2: Integration Testing (Recommended)

Test the complete flow from data fetch to analysis.

**Example**: Testing the complete analysis flow
```python
# tests/test_integration.py
from stock_intelligence_engine import StockAnalyzer

def test_complete_analysis_flow():
    """Test the complete stock analysis flow"""
    analyzer = StockAnalyzer(sandbox=True)
    
    # Step 1: Fetch data
    data = analyzer.fetch_stock_data("AAPL", days=30)
    assert len(data) == 30
    
    # Step 2: Calculate indicators
    indicators = analyzer.calculate_indicators(data)
    assert "sma" in indicators
    assert "rsi" in indicators
    
    # Step 3: Generate analysis
    analysis = analyzer.generate_analysis(indicators)
    assert "trend" in analysis
```

### Level 3: End-to-End Testing (Required)

Test the complete user experience with a real (sandbox) environment.

**Manual Test Script**:
```
1. Start with fresh state (no active connections)
2. Agent receives trigger: "Analyze AAPL stock"
3. Agent executes: data fetch -> analysis -> report
4. Expected: Analysis report with recommendations
5. Verify: Data accuracy, calculations correct
6. Cleanup: Close all connections
```

---

## 👤 Manual Testing

### Required Manual Tests

For **every component**, manually test:

#### Positive Tests (Happy Path)
- [ ] Basic stock data retrieval
- [ ] Technical indicator calculations
- [ ] Pattern recognition
- [ ] Report generation
- [ ] All authentication flows
- [ ] All data provider APIs

#### Negative Tests (Error Cases)
- [ ] Invalid stock symbols
- [ ] Invalid date ranges
- [ ] Missing API credentials
- [ ] Invalid API responses
- [ ] Rate limit exceeded
- [ ] Network failures
- [ ] Invalid configuration

#### Edge Cases
- [ ] Maximum length inputs
- [ ] Special characters in stock symbols
- [ ] Empty data sets
- [ ] Concurrent requests
- [ ] Token expiration scenarios
- [ ] Market closed/holiday scenarios

### Manual Testing Checklist Template

```markdown
# Testing Checklist: [Component Name]

## Setup
- [ ] Sandbox/test environment available
- [ ] Test credentials configured
- [ ] Network connectivity verified
- [ ] Test data cleaned up from previous runs

## Happy Path Tests
- [ ] Test 1: Basic stock analysis
- [ ] Test 2: Pattern recognition
- [ ] Test 3: Report generation
- [ ] Test 4: Custom query

## Error Handling Tests
- [ ] Invalid symbol: _______________
- [ ] Invalid date range: _____________
- [ ] Invalid API key: _____________
- [ ] Rate limit: __________________
- [ ] Network error: _______________
- [ ] Platform error: ______________

## Security Tests
- [ ] Credentials not logged
- [ ] Sensitive data masked
- [ ] Input validation works
- [ ] No hardcoded credentials
- [ ] Rate limiting respected

## Cleanup
- [ ] All test connections closed
- [ ] All test data removed
- [ ] No orphaned resources
- [ ] Environment restored to initial state

## Results
- [ ] All tests passed
- [ ] Issues found: _______________
- [ ] Notes: _____________________
```

---

## 🤖 Automated Testing

### Test File Structure

```
stock-intelligence-engine/
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Fixtures and setup
│   ├── test_calculations.py # Financial calculation tests
│   ├── test_data_fetch.py    # Data fetching tests
│   ├── test_indicators.py    # Technical indicator tests
│   ├── test_analysis.py      # Analysis logic tests
│   ├── test_validation.py   # Input validation tests
│   └── test_errors.py        # Error handling tests
```

### Example Test File

```python
# tests/test_data_fetch.py
import pytest
from unittest.mock import patch, MagicMock
from stock_intelligence_engine import DataFetcher


@pytest.fixture
def mock_api():
    """Create a mock API client"""
    with patch('requests.get') as mock_get:
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "symbol": "AAPL",
            "prices": [100, 101, 102, 103, 104]
        }
        yield mock_get


def test_fetch_stock_data(mock_api):
    """Test fetching stock data"""
    fetcher = DataFetcher(api_key="test-key", sandbox=True)
    data = fetcher.fetch("AAPL", days=5)
    
    assert data["symbol"] == "AAPL"
    assert len(data["prices"]) == 5


def test_fetch_invalid_symbol():
    """Test handling of invalid stock symbol"""
    with pytest.raises(ValueError):
        fetcher = DataFetcher(api_key="test-key")
        fetcher.fetch("INVALID", days=5)
```

### Using pytest

Install pytest:
```bash
pip install pytest pytest-mock pytest-cov
```

Run tests:
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_calculations.py

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=stock_intelligence_engine --cov-report=html

# Run specific test
pytest tests/test_data_fetch.py::test_fetch_stock_data
```

---

## 🌍 Test Environments

### Sandbox Environments

Always use sandbox/test environments for testing:

| Provider | Sandbox URL | Notes |
|----------|-------------|-------|
| Alpha Vantage | https://www.alphavantage.co | Use demo API key |
| Yahoo Finance | N/A | Public data, rate limited |
| Finnhub | https://finnhub.io | Sandbox available |
| Polygon | https://polygon.io | Sandbox available |

### Test Accounts

**For each data provider**:
1. Use demo/sandbox API keys
2. Never use production API keys for testing
3. Respect rate limits (usually 5-30 requests/minute)
4. Cache responses to avoid repeated API calls

### Environment Variables

Use environment variables for test configuration:

```bash
# .env.test
export ALPHA_VANTAGE_API_KEY=demo
export FINNHUB_API_KEY=sandbox_key
export POLYGON_API_KEY=sandbox_key
export SANDBOX_MODE=true
```

**Never commit .env files to version control!**

Add to .gitignore:
```
.env
.env.*
*.env
```

---

## 🗃️ Test Data Management

### Test Data Principles

1. **Use fake data**: Never use real financial data for unit tests
2. **Clean up**: Close all connections after tests complete
3. **Isolate**: Each test should use unique data
4. **Cache**: Cache API responses to avoid rate limits

### Generating Test Data

```python
import pytest
from datetime import datetime, timedelta


def generate_test_stock_data(days=30):
    """Generate test stock price data"""
    base_price = 100
    data = []
    for i in range(days):
        date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
        price = base_price + (i * 0.5) + (i % 2)  # Simulate growth with noise
        data.append({
            "date": date,
            "open": price - 1,
            "high": price + 2,
            "low": price - 2,
            "close": price,
            "volume": 1000000 + (i * 1000)
        })
    return data


@pytest.fixture
def test_stock_data():
    """Provide test stock data"""
    return generate_test_stock_data(30)
```

### Test Data Cleanup

Every test file should include cleanup:

```python
import pytest


@pytest.fixture(scope="session")
def cleanup():
    """Clean up all test resources after session"""
    yield
    # Close all API connections
    close_all_connections()
    # Clear all caches
    clear_test_caches()
```

---

## ⚙️ CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/test.yml`:

```yaml
name: Test Stock Intelligence Engine

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install pytest pytest-mock pytest-cov
        pip install -r requirements.txt
    
    - name: Run unit tests
      run: |
        pytest tests/ -v --tb=short --cov=stock_intelligence_engine --cov-report=xml
    
    - name: Run linting
      run: |
        pip install markdown-lint
        find . -name "*.md" -type f -exec markdownlint-cli2 {} \;
```

### Pre-commit Hooks

Add `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: debug-statements
      - id: detect-private-key
      - id: check-json
      - id: pretty-format-json
  
  - repo: https://github.com/DavidAnson/markdownlint-cli2
    rev: v0.8.1
    hooks:
      - id: markdownlint-cli2
        args: [--config, .markdownlint.json, --fix]
        exclude: CHANGELOG.md
```

---

## ✅ Test Checklists

### New Feature Checklist

Before adding a new feature to the repository:

- [ ] Manual testing completed for all flows
- [ ] All error cases tested
- [ ] Input validation implemented and tested
- [ ] Rate limiting verified
- [ ] Security considerations documented
- [ ] Usage examples included
- [ ] Testing checklist in documentation
- [ ] README.md updated with new feature
- [ ] All links work
- [ ] No hardcoded credentials

### Existing Feature Update Checklist

Before updating an existing feature:

- [ ] Changes tested with existing functionality
- [ ] No breaking changes (or documented if breaking)
- [ ] Version bumped appropriately
- [ ] Changelog updated
- [ ] New tests added for new functionality
- [ ] Existing tests still pass
- [ ] Documentation updated

### Pre-PR Checklist

Before opening a pull request:

- [ ] All manual tests pass
- [ ] Automated tests pass (if applicable)
- [ ] Code follows repository standards
- [ ] Documentation is complete
- [ ] No sensitive data committed
- [ ] Version numbers updated
- [ ] Testing checklist completed

---

## 📊 Test Coverage Reports

Generate coverage reports to identify untested areas:

```bash
# Install coverage
pip install pytest-cov

# Run tests with coverage
pytest --cov=stock_intelligence_engine --cov-report=html

# Open coverage report
open htmlcov/index.html
```

Aim for **80%+ coverage** for production components.

---

## 🛠️ Test Utilities

### Mock Server

For testing API interactions without hitting real services:

```python
# tests/conftest.py
import pytest
from unittest.mock import Mock
import requests


@pytest.fixture
def mock_requests():
    """Mock requests library for API testing"""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post:
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        
        mock_post.return_value = Mock()
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {}
        
        yield mock_get, mock_post
```

### Test Data Factories

```python
# tests/factories.py
from datetime import datetime, timedelta


def create_test_candlestick(price=100, volume=1000000):
    """Create a test candlestick data point"""
    return {
        "date": datetime.now().strftime('%Y-%m-%d'),
        "open": price - 1,
        "high": price + 2,
        "low": price - 2,
        "close": price,
        "volume": volume
    }


def create_test_stock(symbol="AAPL"):
    """Create test stock data"""
    return {
        "symbol": symbol,
        "name": f"{symbol} Company",
        "sector": "Technology",
        "market_cap": 1000000000,
        "pe_ratio": 25.0
    }
```

---

## 🎯 Summary

| Aspect | Requirement |
|--------|-------------|
| Manual Testing | ✅ Required for all components |
| Automated Testing | ⚠️ Recommended for all components |
| Test Coverage | ≥ 80% for production components |
| Test Environment | Sandbox only, never production |
| Test Data | Fake data only, cleaned up after |
| Test Credentials | Sandbox/demo keys only |
| CI/CD | ✅ Required for all PRs |

**Remember**: The quality of your tests directly impacts the reliability and accuracy of financial analysis and trading decisions.

---

*Last updated: September 11, 2026*
