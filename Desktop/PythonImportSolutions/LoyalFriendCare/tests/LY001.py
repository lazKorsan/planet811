import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.reusable_methods import setup_driver, validateElementClick

driver = setup_driver()
driver.get("https://qa.loyalfriendcare.com/en")
validateElementClick(driver, "(//*[@href='https://qa.loyalfriendcare.com'])[5]", "red", "HomeButton")

# Driver'ı kapat
driver.quit()