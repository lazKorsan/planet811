# C:\Users\user\Desktop\PythonImportSolutions\LoyalFriendCare\tests\LY006.py
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Driver import create_driver, close_driver, BrowserUtils
from LoyalPages import HomePages
from ConReq import testData

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

# url adresini gir
driver.get(testData.loginURL)

# Sayfanın yüklenmesini bekle
BrowserUtils.wait_for_page_load(driver, timeout=10) 

HomePages.loginMethodtoLoyalFriendCare(driver, testData.mail, testData.password)


# Driver'ı kapat
close_driver(driver)



