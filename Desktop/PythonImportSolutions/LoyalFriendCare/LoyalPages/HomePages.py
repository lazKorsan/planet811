# C:\Users\user\Desktop\PythonImportSolutions\LoyalFriendCare\LoyalPages\HomePages.py
import sys
import os
import time
from datetime import datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.SendKeysUtils import SendKeysUtils
from utils.ClickUtils import ClickUtils
from LoyalPages import HomePages

mailBox_Xpath = '//input[@id="email"]'
passwordBox_Xpath = '//*[@id="password"]'
loginButton_Xpath = '//button[@type="submit"]'
rememberMeCheckBox_Xpath = '/html/body/div[1]/div[2]/div/form/div[3]/div[1]/div/label'
signUpButton_Xpath = '//button[@class="btn btn-primary btn-cons m-t-10"]'
homeButton_Xpath = '//a[@href="https://qa.loyalfriendcare.com"]'



def loginMethodtoLoyalFriendCare(driver, mail, password):
    """
    Loyal Friend Care'a giriş yapma fonksiyonu (try-except ile güvenli hale getirilmiş)
    """
    try:
        # mailBox gecerli E-Posta adresi gir 
        SendKeysUtils.force_send_keys_with_js(
            driver=driver,
            xpath=HomePages.mailBox_Xpath,
            color="red",
            text=mail,
            input_name="Mail Kutusu"
        )
        time.sleep(3)

        # passwordBox gecerli şifre gir 
        SendKeysUtils.force_send_keys_with_js(
            driver=driver,
            xpath=HomePages.passwordBox_Xpath,
            color="red",
            text=password,
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
        
        # login butonuna tıkla 
        ClickUtils.force_click_with_js(
            driver=driver,
            xpath=HomePages.loginButton_Xpath,
            color="red",
            button_name="Login Butonu"
        )
        
        print("Başarılı: Giriş işlemi tamamlandı")
        return True
        
    except Exception as e:
        print(f"Hata: Giriş işlemi sırasında hata oluştu: {str(e)}")
        print(f"Hata detayı: {type(e).__name__}")
        
        # Hata durumunda ekran görüntüsü almak isteyebilirsiniz
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/login_error_{timestamp}.png"
            driver.save_screenshot(screenshot_path)
            print(f"Ekran görüntüsü kaydedildi: {screenshot_path}")
        except Exception as screenshot_error:
            print(f"Ekran görüntüsü alınamadı: {screenshot_error}")
        
        return False

    
