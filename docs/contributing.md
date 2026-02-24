# Contributing Guide

Thank you for your interest in contributing to the E-Commerce Intelligence System! This document provides guidelines and instructions for contributing.

## 🤝 How to Contribute

We welcome all forms of contributions, including but not limited to:
- Bug fixes
- New features
- Documentation improvements
- Performance optimizations
- Test coverage
- Bug reports and feature requests

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style Guidelines](#code-style-guidelines)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- MySQL 8.0 or higher
- Git
- GitHub account

### Step 1: Fork the Repository

1. Navigate to the [repository](https://github.com/yourusername/ecommerce-intelligence-system)
2. Click the "Fork" button in the top-right corner
3. This creates a copy of the repository under your GitHub account

### Step 2: Clone Your Fork

```bash
git clone https://github.com/yourusername/ecommerce-intelligence-system.git
cd ecommerce-intelligence-system
```

### Step 3: Add Upstream Remote

```bash
git remote add upstream https://github.com/original-owner/ecommerce-intelligence-system.git
```

This allows you to keep your fork synchronized with the original repository.

---

## 💻 Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
# Install development dependencies
pip install -r requirements.txt

# Install additional development tools
pip install black flake8 isort pytest pytest-cov
```

### 3. Configure Database

1. Create a local MySQL database:
```bash
mysql -u root -p -e "CREATE DATABASE ecommerce_test_dev;"
```

2. Update `src/utils/db.py` with your local database credentials:
```python
DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "your_password",
    "database": "ecommerce_test_dev",
    "charset": "utf8mb4"
}
```

### 4. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_etl.py
```

---

## 📝 Code Style Guidelines

### Python Code Style

We follow **PEP 8** guidelines with some modifications:

#### Formatting

Use **Black** for code formatting:
```bash
# Format all Python files
black .

# Format specific file
black src/analysis/user_behavior_analysis.py
```

#### Import Sorting

Use **isort** for import organization:
```bash
# Sort all imports
isort .

# Sort specific file
isort src/etl/load_orders.py
```

#### Linting

Use **flake8** for code quality checks:
```bash
# Check all files
flake8 src/

# Check specific file
flake8 src/utils/db.py
```

### Code Formatting Example

**Before**:
```python
import pandas, numpy
from sklearn.cluster import KMeans
def  rfm_analysis ( df ):
    result= df.groupby('customer_id').agg({
        'order_date':'max',
        'order_id':'count'
    })
    return result
```

**After** (formatted with Black and isort):
```python
import numpy as np
import pandas as pd

from sklearn.cluster import KMeans


def rfm_analysis(df):
    """Perform RFM analysis on customer data.

    Args:
        df: Input DataFrame with customer order data

    Returns:
        DataFrame with RFM metrics
    """
    result = df.groupby("customer_id").agg(
        {"order_date": "max", "order_id": "count"}
    )
    return result
```

### Documentation

#### Docstrings

Use **Google style** docstrings:

```python
def analyze_customer_behavior(customer_id: str, engine) -> dict:
    """Analyze customer behavior patterns.

    Args:
        customer_id: Unique customer identifier
        engine: SQLAlchemy database engine

    Returns:
        Dictionary containing:
            - recency: Days since last purchase
            - frequency: Number of purchases
            - monetary: Total amount spent

    Raises:
        ValueError: If customer_id not found

    Example:
        >>> engine = get_engine()
        >>> result = analyze_customer_behavior('12345', engine)
        >>> print(result['recency'])
        45
    """
    # Implementation...
```

#### Comments

- Write **why**, not **what** (the code should show what)
- Use comments to explain complex logic
- Keep comments up-to-date when code changes

**Good**:
```python
# Use window function to calculate ranking efficiently
# This performs better than self-joins on large datasets
df['rank'] = df.groupby('customer_id')['order_date'].rank(method='first')
```

**Bad**:
```python
# Set rank
df['rank'] = ...
```

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Variables | snake_case | `customer_id`, `order_count` |
| Functions | snake_case | `get_connection()`, `analyze_data()` |
| Classes | PascalCase | `UserBehaviorAnalyzer`, `SatisfactionModel` |
| Constants | UPPER_SNAKE_CASE | `DB_CONFIG`, `MAX_BATCH_SIZE` |
| Private | _leading_underscore | `_internal_function()` |

---

## 📜 Commit Message Guidelines

We follow the **Conventional Commits** specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, etc.)
- **refactor**: Code refactoring
- **test**: Adding or updating tests
- **chore**: Build process or auxiliary tool changes

### Examples

**Good commit messages**:

```bash
feat(analysis): add RFM customer segmentation

Implement K-Means clustering for customer segmentation
based on Recency, Frequency, and Monetary metrics.

- Add customer_segmentation() method
- Add RFM scoring logic
- Include visualization function

Closes #123
```

```bash
fix(etl): handle NULL values in product category

Prevents crashes when product_category_name is NULL.
Use 'unknown' as default category.

Fixes #45
```

```bash
docs(api): update database utility documentation

Add examples for execute_many() function.
Clarify connection handling best practices.
```

**Bad commit messages**:
- `update files`
- `fix bug`
- `wip`
- `doing stuff`

### Commit Message Template

Create `.gitmessage` file:
```
# <type>(<scope>): <subject>
# |<----  Using a Maximum Of 50 Characters  ---->|

# Explain why this change is being made
# |<----   Try To Limit Each Line to a Maximum Of 72 Characters   ---->|

# Provide links or keys to any relevant tickets, articles or other resources
# Example: Fixes #23

# --- COMMIT END ---
# Type can be:
#   feat     (new feature)
#   fix      (bug fix)
#   docs     (changes to documentation)
#   style    (formatting, missing semi colons, etc; no code change)
#   refactor (refactoring production code)
#   test     (adding missing tests, refactoring tests; no production code change)
#   chore    (updating build tasks, package manager configs, etc; no production code change)
```

Use it with:
```bash
git commit -F .gitmessage
```

---

## 🔀 Pull Request Process

### Step 1: Create a Branch

From your fork, create a descriptive branch:

```bash
git checkout -b feature/customer-segmentation
# or
git checkout -b fix/database-connection-error
# or
git checkout -b docs/update-readme
```

### Step 2: Make Changes

- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed
- Run tests and ensure they pass

### Step 3: Commit Changes

```bash
git add .
git commit -m "feat(analysis): add customer segmentation model"
```

### Step 4: Push to GitHub

```bash
git push origin feature/customer-segmentation
```

### Step 5: Create Pull Request

1. Navigate to your fork on GitHub
2. Click "Pull Requests" → "New Pull Request"
3. Select your branch
4. Fill out the PR template:

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests added/updated
- [ ] All tests pass

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No new warnings generated

## Related Issues
Fixes #123
```

### Step 6: Review Process

1. **Automated Checks**: CI/CD will run tests
2. **Code Review**: Maintainers will review your code
3. **Feedback**: Address any review comments
4. **Approval**: Once approved, your PR will be merged

### Step 7: Update Your Fork

After your PR is merged, update your fork:

```bash
git fetch upstream
git checkout master
git merge upstream/master
git push origin master
```

---

## 🐛 Reporting Issues

### Before Creating an Issue

1. **Search existing issues**: Check if someone already reported it
2. **Check documentation**: Review docs and README
3. **Reproduce the bug**: Ensure it's reproducible

### Issue Template

When reporting a bug, use this template:

```markdown
## Bug Description
Clear and concise description of the bug

## Reproduction Steps
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

## Expected Behavior
What you expected to happen

## Actual Behavior
What actually happened

## Screenshots
If applicable, add screenshots

## Environment
- OS: [e.g. Windows 10, macOS 11.0]
- Python Version: [e.g. 3.8.10]
- MySQL Version: [e.g. 8.0.26]

## Additional Context
Any other relevant information, error logs, etc.
```

### Feature Request Template

```markdown
## Feature Description
Clear and concise description of the feature

## Problem Statement
What problem does this feature solve?

## Proposed Solution
How should this be implemented?

## Alternatives Considered
What other approaches did you consider?

## Additional Context
Any other relevant information, examples, etc.
```

---

## 📧 Getting Help

If you need help:

1. **Documentation**: Check the [docs](docs/) folder
2. **Issues**: Search or create a GitHub issue
3. **Discussions**: Start a GitHub discussion
4. **Email**: Contact [your.email@example.com]

---

## 🌟 Recognition

Contributors will be:
- Listed in the CONTRIBUTORS.md file
- Mentioned in release notes for significant contributions
- Credited in project documentation

Thank you for contributing! 🎉
