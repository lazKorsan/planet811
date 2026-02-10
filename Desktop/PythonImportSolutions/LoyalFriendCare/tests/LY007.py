# C:\Users\user\Desktop\PythonImportSolutions\LoyalFriendCare\tests\LY006.py
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..'
        )
    )
)

from utils.Driver import create_driver, close_driver, BrowserUtils
from LoyalPages import HomePages  # Sadece bu şekilde import et
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

# Eğer fonksiyon HomePages.py'de yoksa, kendiniz oluşturun:
email_box = BrowserUtils.find_element(driver, HomePages.mailBox_Xpath)
if email_box:
    email_box.clear()
    email_box.send_keys(testData.mail)

password_box = BrowserUtils.find_element(driver, HomePages.passwordBox_Xpath)
if password_box:
    password_box.clear()
    password_box.send_keys(testData.password)

login_button = BrowserUtils.find_element(driver, HomePages.loginButton_Xpath)
if login_button:
    login_button.click()

# Veya fonksiyonu burada tanımlayın:
def loginMethodtoLoyalFriendCare(driver, email, password):
    email_box = BrowserUtils.find_element(driver, HomePages.mailBox_Xpath)
    if email_box:
        email_box.clear()
        email_box.send_keys(email)
    
    password_box = BrowserUtils.find_element(driver, HomePages.passwordBox_Xpath)
    if password_box:
        password_box.clear()
        password_box.send_keys(password)
    
    login_button = BrowserUtils.find_element(driver, HomePages.loginButton_Xpath)
    if login_button:
        login_button.click()
    
    BrowserUtils.wait_for_page_load(driver, timeout=10)

# Sonra fonksiyonu çağırın:
loginMethodtoLoyalFriendCare(driver, testData.mail, testData.password)

# Driver'ı kapat
close_driver(driver)