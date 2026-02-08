import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.reusable_methods import setup_driver
from utils.SendKeysUtils import SendKeysUtils
from utils.ClickUtils import ClickUtils


driver = setup_driver()
driver.get("https://qa.loyalfriendcare.com/en")

ClickUtils.force_click_with_js(
    driver=driver,
    xpath="(//*[@href='https://qa.loyalfriendcare.com'])[5]",
    color="red",
    button_name="Home Butonu"
)

time.sleep(3)

SendKeysUtils.force_send_keys_with_js(
    driver=driver,
    xpath='//input[@class="form-control"]',
    color="red",
    text="re",
    input_name="Arama Kutusu"
)

time.sleep(3)
# Driver'ı kapat
driver.quit(
)