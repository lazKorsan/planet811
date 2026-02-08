import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.reusable_methods import setup_driver, validateElementClick
from utils.ClickUtils import ClickUtils


driver = setup_driver()
driver.get("https://qa.loyalfriendcare.com/en")

#ClickUtils.force_click_with_js(driver, "(//*[@href='https://qa.loyalfriendcare.com'])[5]")

ClickUtils.force_click_with_js(
    driver=driver,
    xpath="(//*[@href='https://qa.loyalfriendcare.com'])[5]",
    color="red",
    button_name="Home Butonu"
)

#validateElementClick(driver, "(//*[@href='https://qa.loyalfriendcare.com'])[5]", "red", "HomeButton")

# Driver'ı kapat
driver.quit()