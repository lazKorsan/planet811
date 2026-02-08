# LY003.py
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Driver import create_driver, close_driver, BrowserUtils
from utils.SendKeysUtils import SendKeysUtils
from utils.ClickUtils import ClickUtils



# Yeni Driver yapısıyla driver oluştur
driver = create_driver(
    browser="chrome",
    headless=False,
    window_size="1920x1080",
    timeout=30,
    disable_notifications=True,
    incognito=False,
    disable_images=False
)

driver.get("https://qa.loyalfriendcare.com/en")

# Sayfanın yüklenmesini bekle
BrowserUtils.wait_for_page_load(driver, timeout=10)

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

ClickUtils.force_click_with_js(
    driver=driver,
    xpath= '//input[@type="submit"]',
    color="red",
    button_name="Search Butonu"
)




time.sleep(3)

# Driver'ı kapat
close_driver(driver)