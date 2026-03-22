from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """
    Parent class for all Page Objects.
    Every page class inherits from here.
    All common Selenium actions defined once here.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait   = WebDriverWait(driver, 15)  # explicit wait — 15 sec

    # ── FIND ────────────────────────────────────────────
    def find_element(self, by, locator):
        """Wait until element exists in DOM and return it"""
        logger.info(f"Finding element: {locator}")
        return self.wait.until(
            EC.presence_of_element_located((by, locator))
        )

    # ── CLICK ───────────────────────────────────────────
    def click(self, by, locator):
        """Wait until element is clickable, then click"""
        logger.info(f"Clicking: {locator}")
        el = self.wait.until(
            EC.element_to_be_clickable((by, locator))
        )
        el.click()

    # ── TYPE ────────────────────────────────────────────
    def type_text(self, by, locator, text):
        """Clear field and type text"""
        logger.info(f"Typing '{text}' into: {locator}")
        el = self.find_element(by, locator)
        el.clear()
        el.send_keys(text)

    # ── GET TEXT ────────────────────────────────────────
    def get_text(self, by, locator):
        """Return visible text of element"""
        return self.find_element(by, locator).text.strip()

    # ── IS VISIBLE ──────────────────────────────────────
    def is_visible(self, by, locator):
        """Returns True if element visible, False if not"""
        try:
            self.wait.until(
                EC.visibility_of_element_located((by, locator))
            )
            return True
        except TimeoutException:
            return False

    # ── WAIT FOR CLICKABLE ──────────────────────────────
    def wait_for_element_clickable(self, by, locator):
        """Wait until element is clickable — use after menu animations"""
        return self.wait.until(
            EC.element_to_be_clickable((by, locator))
        )

    # ── IFRAME HANDLING ─────────────────────────────────
    def switch_to_frame(self, by, locator):
        """Switch into iframe — needed for embedded forms or popups"""
        logger.info("Switching into iframe")
        self.wait.until(
            EC.frame_to_be_available_and_switch_to_it((by, locator))
        )

    def switch_to_default(self):
        """Switch back to main page from iframe"""
        logger.info("Switching back to main page")
        self.driver.switch_to.default_content()

    # ── WAIT FOR TEXT ───────────────────────────────────
    def wait_for_text(self, by, locator, text):
        """Wait until element contains specific text"""
        return self.wait.until(
            EC.text_to_be_present_in_element((by, locator), text)
        )

    # ── GET URL ─────────────────────────────────────────
    def get_current_url(self):
        """Return current page URL"""
        return self.driver.current_url

    # ── SCROLL ──────────────────────────────────────────
    def scroll_to_element(self, by, locator):
        """Scroll element into view"""
        el = self.find_element(by, locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView(true);", el
        )
