# LY005.py
import sys
import os
import time
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.Driver import create_driver, close_driver, BrowserUtils
from utils.SendKeysUtils import SendKeysUtils
from utils.ClickUtils import ClickUtils
from LoyalPages import HomePages
from ConReq import testData

# Spesifik degerlerle dirver olustur 
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

# mailBox gecerli E-Posta adresi gir 
SendKeysUtils.force_send_keys_with_js(
    driver=driver,
    xpath=HomePages.mailBox_Xpath,
    color="red",
    text=testData.mail,
    input_name="Mail Kutusu"
)
time.sleep(3)

# passwordBox gecerli E-Posta adresi gir 
SendKeysUtils.force_send_keys_with_js(
    driver=driver,
    xpath=HomePages.passwordBox_Xpath,
    color="red",
    text=testData.password,
    input_name="Şifre Kutusu"
)
time.sleep(3)

# sonraki oturumlarda beni hatırla butonuna tıkla
ClickUtils.force_click_with_js(
    driver=driver,
    xpath=HomePages.rememberMeCheckBox_Xpath,
    color="red",
    button_name="Beni Hatırla"
)
time.sleep(3)
# signUpButtona tikla 
ClickUtils.force_click_with_js(
    driver=driver,
    xpath=HomePages.loginButton_Xpath,
    color="red",
    button_name="SignUp Butonu"
)





# Driver'ı kapat
close_driver(driver)