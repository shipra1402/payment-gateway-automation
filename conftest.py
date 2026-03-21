import pytest
import configparser
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


# ══════════════════════════════════════════════════
#  FIXTURE 1 — Config Reader
#  Reads config/config.ini ONCE for entire session
# ══════════════════════════════════════════════════
@pytest.fixture(scope="session")
def config():
    cfg = configparser.ConfigParser()
    cfg.read("config/config.ini")
    return cfg


# ══════════════════════════════════════════════════
#  FIXTURE 2 — Chrome WebDriver
#  Opens browser before test, closes after test
# ══════════════════════════════════════════════════
@pytest.fixture(scope="function")
def driver(config):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )

    drv = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    drv.implicitly_wait(
        int(config["BASE"]["implicit_wait"])
    )
    drv.get(config["BASE"]["url"])
    yield drv          # test runs here
    drv.quit()          # always runs after test — pass or fail


# ══════════════════════════════════════════════════
#  FIXTURE 3 — API Session
#  Creates requests session with Razorpay auth
# ══════════════════════════════════════════════════
@pytest.fixture(scope="session")
def api_session(config):
    import requests
    session = requests.Session()

    session.headers.update({
        "Content-Type": "application/json"
    })
    yield session
    session.close()


# ══════════════════════════════════════════════════
#  FIXTURE 4 — MySQL DB Connection
#  Connects to MySQL before test, closes after
# ══════════════════════════════════════════════════
@pytest.fixture(scope="function")
def db_connection(config):
    import pymysql
    conn = pymysql.connect(
        host=config["DATABASE"]["host"],
        port=int(config["DATABASE"]["port"]),
        user=config["DATABASE"]["user"],
        password=config["DATABASE"]["password"],
        database=config["DATABASE"]["database"],
        cursorclass=pymysql.cursors.DictCursor
    )
    yield conn          # test uses this connection
    conn.close()        # always closes — no connection leak


# ══════════════════════════════════════════════════
#  HOOK — Screenshot on every test failure
#  Auto-saves PNG to reports/screenshots/
# ══════════════════════════════════════════════════
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report  = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv:
            ts   = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            name = item.name.replace("[","_").replace("]","")
            path = f"reports/screenshots/{name}_{ts}.png"
            os.makedirs("reports/screenshots", exist_ok=True)
            drv.save_screenshot(path)
            print(f"\n📸 Screenshot: {path}")