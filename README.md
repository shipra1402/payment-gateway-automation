
 E-Commerce Test Automation Framework
![Tests](https://github.com/shipra1402/payment-gateway-automation/actions/workflows/run-tests.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![Selenium](https://img.shields.io/badge/Selenium-4.x-green)
![pytest](https://img.shields.io/badge/pytest-9.x-orange)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)

## About
A production-grade test automation framework for e-commerce
web application testing built with Python, Selenium WebDriver, and pytest.
Covers UI automation, REST API testing, and MySQL DB validation.

## Tech Stack
| Layer | Technology |
|-------|-----------|
| UI Automation | Selenium WebDriver + POM |
| Test Framework | pytest + markers |
| API Testing | Python requests |
| Database | MySQL 8 + pymysql |
| Reports | pytest-html + Allure |
| Config | configparser (config.ini) |

## Project Structure
```
ECommerce_Automation/
├── config/          # config.ini — URLs, DB, credentials
├── pages/           # Page Object Model classes
│   ├── base_page.py
│   └── login_page.py
├── api/             # API helper classes
│   └── api_helper.py
├── db/              # Database helper
│   └── db_helper.py
├── tests/
│   ├── ui/          # Selenium UI tests (10 tests)
│   └── api/         # API + DB tests (11 tests — 8 API + 3 DB)
├── reports/         # HTML + Allure reports
├── conftest.py      # Fixtures + screenshot hook
├── pytest.ini       # Test configuration
└── requirements.txt
```

## Test Coverage
| Suite | Tests | Type |
|-------|-------|------|
| Login & UI flows    | 10 | UI — Selenium        |
| API validation      | 8  | REST API — requests  |
| DB validation       | 3  | MySQL — pymysql      |
| **Total**           | **21** | **100% Pass Rate** |

## How to Run
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest -v

# Run by marker
pytest -m smoke -v        # smoke tests only
pytest -m ui -v           # UI tests only
pytest -m api -v          # API + DB tests only
pytest -m regression -v   # regression suite

# Generate Allure report
pytest -v --alluredir=reports/allure
allure serve reports/allure
```

## Key Features
- Page Object Model for maintainable UI tests
- 3-layer validation: UI + API response + MySQL DB
- Auto screenshot on every test failure
- pytest-html + Allure visual reports
- Data-driven test support via configparser
- Auto ChromeDriver management (webdriver-manager)
- pytest markers for selective test execution
- MySQL transaction validation with pymysql


## Test Sites

| Layer | Site | Purpose |
|-------|------|---------|
| UI Automation | https://www.saucedemo.com | Login, session, navigation flows |
| API Testing | https://jsonplaceholder.typicode.com | REST API — GET, POST, PUT, DELETE |
| DB Testing | MySQL local instance | Transaction validation and integrity checks |



## Test Execution Report

![Allure Report](docs/allure_report.png)

> 21 test cases | 100% Pass Rate | UI + API Coverage