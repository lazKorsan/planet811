from behave import given, when, then
import sys
import os

# Add project root to sys.path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from utils.Driver import create_driver, close_driver, BrowserUtils
from LoyalPages import HomePages
from ConReq import testData

@given('LoyalFriendCare kullanıcısı login sayfasına gider')
def step_given_user_goes_to_login_page(context):
    # Yeni Driver yapısıyla driver oluştur
    context.driver = create_driver(
        browser="chrome",
        headless=False,
        window_size="1920x1080",
        timeout=30,
        disable_notifications=True,
        incognito=False,
        disable_images=False
    )

    # url adresini gir
    context.driver.get(testData.loginURL)
    
    # Sayfanın yüklenmesini bekle
    BrowserUtils.wait_for_page_load(context.driver, timeout=10) 
    
    print("LoyalFriendCare kullanıcısı login sayfasına gitti.")

@when('LoyalFriendCare kullanıcısı doğru bilgilerle siteye giriş yapar')
def step_when_user_logs_in_with_correct_info(context):
    HomePages.loginMethodtoLoyalFriendCare(context.driver, testData.mail, testData.password)

@step('Kullanıcı tarayıcıyı kapatır')
def step_then_user_closes_browser(context):
    # Driver'ı kapat
    close_driver(context.driver)
    print("Kullanıcı tarayıcıyı kapattı.")
