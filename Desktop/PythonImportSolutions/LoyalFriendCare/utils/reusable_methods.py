# src/utils/reusable_methods.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Initializes and returns a Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless") # Uncomment if you want to run headlessly
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    GRAY = '\033[90m'

class ReusableMethods:
    @staticmethod
    def validateElementClick(driver: WebDriver, xpath: str, highlight_color: str, button_name: str, timeout: int = 10):
        """
        Validates the visibility and clickability of a button, highlights it, and prints a report.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            xpath (str): The XPath of the button element.
            highlight_color (str): The color to highlight the button (e.g., 'red', 'yellow').
            button_name (str): A user-friendly name for the button.
            timeout (int): The maximum time to wait for the element to be visible and clickable.
        """
        element = None
        is_visible = False
        is_clickable = False
        original_style = ""

        try:
            # Wait for element to be visible
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            is_visible = True
            print(f"{Colors.GREEN}{button_name} gorunur.{Colors.ENDC}")

            # Highlight the element
            original_style = driver.execute_script("var elem = arguments[0]; var original_style = elem.style.border; elem.style.border = '3px solid " + highlight_color + "'; return original_style;", element)

            # Wait for element to be clickable
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            is_clickable = True
            print(f"{Colors.GREEN}{button_name} Tıklanabilir.{Colors.ENDC}")

            # Assertions
            assert is_visible, f"{button_name} gorunur degil!"
            assert is_clickable, f"{button_name} Tıklanabilir degil!"

        except Exception as e:
            print(f"{Colors.RED}Hata: {button_name} kontrol edilirken bir sorun oluştu: {e}{Colors.ENDC}")
            # Ensure the test fails if any exception occurs during visibility/clickability checks
            assert False, f"{button_name} kontrolu basarisiz oldu: {e}"
        finally:
            # Remove highlight after a short delay (optional, or removed by navigation)
            # For immediate removal after check, uncomment the following line
            if element and original_style:
                 driver.execute_script("arguments[0].style.border = arguments[1];", element, original_style)
            pass # Keep highlight for visual inspection if needed, or remove later in the test flow

    @staticmethod
    def enter_text(driver: WebDriver, xpath: str, text: str, field_name: str, timeout: int = 10):
        """
        Enters text into an input field after waiting for it to be visible.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            xpath (str): The XPath of the input field.
            text (str): The text to enter.
            field_name (str): A user-friendly name for the input field.
            timeout (int): The maximum time to wait for the element to be visible.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            element.clear()
            element.send_keys(text)
            print(f"{Colors.GREEN}{field_name}: '{text}' başarıyla girildi.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}Hata: '{field_name}' alanına metin girilirken sorun oluştu: {e}{Colors.ENDC}")
            assert False, f"Metin girişi başarısız oldu: {e}"

    @staticmethod
    def get_element_text(driver: WebDriver, xpath: str, element_name: str, timeout: int = 10) -> str:
        """
        Retrieves the visible text of an element after waiting for its presence.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            xpath (str): The XPath of the element.
            element_name (str): A user-friendly name for the element.
            timeout (int): The maximum time to wait for the element to be present.

        Returns:
            str: The visible text of the element.
        """
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            text = element.text
            print(f"{Colors.CYAN}{element_name} metni alındı: '{text}'{Colors.ENDC}")
            return text
        except Exception as e:
            print(f"{Colors.RED}Hata: '{element_name}' metni alınırken sorun oluştu: {e}{Colors.ENDC}")
            assert False, f"Metin alma başarısız oldu: {e}"

def greet(name):
    """
    Returns a greeting message.
    """
    return f"Hello, {name}!"

def add_numbers(a, b):
    """
    Adds two numbers and returns the result.
    """
    return a + b

# Export static methods as module-level functions
validateElementClick = ReusableMethods.validateElementClick
enter_text = ReusableMethods.enter_text
get_element_text = ReusableMethods.get_element_text
