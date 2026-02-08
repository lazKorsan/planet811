# ClickUtils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    ElementNotInteractableException, 
    StaleElementReferenceException,
    ElementClickInterceptedException,
    NoSuchElementException
)
import time

class ClickUtils:
    
    @staticmethod
    def highlight_element(driver, element, color="red", border_width=3, duration=1):
        """
        Elementi belirtilen renkle vurgular
        """
        try:
            # Mevcut stilini sakla
            original_style = element.get_attribute("style")
            
            # Yeni stil ekle
            highlight_style = f"border: {border_width}px solid {color}; background-color: yellow;"
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                 element, f"{original_style}; {highlight_style}")
            
            # Belirtilen süre bekleyip eski haline döndür
            if duration > 0:
                time.sleep(duration)
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                     element, original_style)
            
            return True
        except Exception as e:
            print(f"❌ Element vurgulanamadı: {str(e)}")
            return False
    
    @staticmethod
    def check_button_clickable(driver, element):
        """
        Butonun tıklanabilir olup olmadığını kontrol eder
        """
        try:
            # Element görünür ve etkin mi kontrolü
            is_displayed = element.is_displayed()
            is_enabled = element.is_enabled()
            
            # Element üzerinde click olayı dinleyicisi var mı kontrolü (basit)
            onclick = element.get_attribute("onclick")
            has_onclick = onclick is not None and onclick.strip() != ""
            
            return {
                "clickable": is_displayed and is_enabled,
                "displayed": is_displayed,
                "enabled": is_enabled,
                "has_onclick": has_onclick,
                "tag_name": element.tag_name,
                "type": element.get_attribute("type") or "N/A"
            }
        except Exception as e:
            print(f"❌ Buton tıklanabilirlik kontrolü başarısız: {str(e)}")
            return {"clickable": False, "displayed": False, "enabled": False}
    
    @staticmethod
    def check_button_visible(driver, element):
        """
        Butonun görünür olup olmadığını kontrol eder
        """
        try:
            # Selenium'un görünürlük kontrolü
            is_displayed = element.is_displayed()
            
            # Ekran görünümünde mi kontrolü (scroll ile)
            rect = element.rect
            viewport_height = driver.execute_script("return window.innerHeight;")
            viewport_width = driver.execute_script("return window.innerWidth;")
            
            in_viewport = (
                0 <= rect['y'] <= viewport_height and
                0 <= rect['x'] <= viewport_width
            )
            
            # CSS opacity ve visibility kontrolü
            opacity = element.value_of_css_property("opacity")
            visibility = element.value_of_css_property("visibility")
            display = element.value_of_css_property("display")
            
            css_visible = (
                opacity != "0" and 
                visibility != "hidden" and 
                display != "none"
            )
            
            return {
                "visible": is_displayed and css_visible,
                "displayed": is_displayed,
                "in_viewport": in_viewport,
                "css_visible": css_visible,
                "opacity": opacity,
                "visibility": visibility,
                "display": display
            }
        except Exception as e:
            print(f"❌ Buton görünürlük kontrolü başarısız: {str(e)}")
            return {"visible": False, "displayed": False}
    
    @staticmethod
    def force_click_with_js(driver, element=None, xpath=None, color="red", button_name="Unknown"):
        """
        JS ile zorla tıklama - Overlay arkasındaki elementler için
        """
        print(f"⚡️ [{button_name}] JS ile zorla tıklama başlatıldı...")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Buton bilgilerini kontrol et
            clickable_info = ClickUtils.check_button_clickable(driver, element)
            visible_info = ClickUtils.check_button_visible(driver, element)
            
            print(f"📋 [{button_name}] BUTON BİLGİLERİ:")
            print(f"   • Tıklanabilir mi: {clickable_info['clickable']}")
            print(f"   • Görünür mü: {visible_info['visible']}")
            print(f"   • Viewport'ta mı: {visible_info['in_viewport']}")
            print(f"   • Etkin mi: {clickable_info['enabled']}")
            print(f"   • Tag: {clickable_info['tag_name']}")
            
            # Elementi vurgula
            if color:
                ClickUtils.highlight_element(driver, element, color, 3, 1)
            
            # JS ile scroll ve click
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            driver.execute_script("arguments[0].click();", element)
            
            print(f"✅ [{button_name}] JS ile zorla tıklama BAŞARILI!")
            return True
            
        except Exception as e:
            print(f"❌ [{button_name}] JS ile zorla tıklama BAŞARISIZ: {str(e)}")
            return False
    
    @staticmethod
    def smart_click_with_wait(driver, element=None, xpath=None, timeout_in_seconds=10, button_name="Unknown"):
        """
        Beklemeli akıllı tıklama - EN SAĞLAM YÖNTEM
        """
        print(f"⏳ [{button_name}] Beklemeli SmartClick başlatıldı (timeout: {timeout_in_seconds}s)")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Buton bilgilerini kontrol et
            ClickUtils.check_button_clickable(driver, element)
            
            # Vurgula
            ClickUtils.highlight_element(driver, element, "orange", 2, 0.5)
            
            # Bekle ve tıkla
            wait = WebDriverWait(driver, timeout_in_seconds)
            wait.until(EC.element_to_be_clickable(element))
            
            # Akıllı tıklama
            ClickUtils.smart_click(driver, element, button_name)
            
            print(f"✅ [{button_name}] Beklemeli SmartClick BAŞARILI!")
            return True
            
        except TimeoutException:
            print(f"❌ [{button_name}] Element {timeout_in_seconds} saniye içinde tıklanabilir olmadı. JS ile tıklanıyor...")
            return ClickUtils.force_click_with_js(driver, element, None, "red", button_name)
            
        except Exception as e:
            print(f"❌ [{button_name}] Beklemeli SmartClick sırasında beklenmedik bir hata: {str(e)}")
            return ClickUtils.force_click_with_js(driver, element, None, "red", button_name)
    
    @staticmethod
    def smart_click(driver, element=None, xpath=None, button_name="Unknown"):
        """
        Her türlü buton için çalışır
        """
        print(f"🔹 [{button_name}] Smart click başlatıldı")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Buton bilgilerini kontrol et
            clickable_info = ClickUtils.check_button_clickable(driver, element)
            
            if not clickable_info['clickable']:
                print(f"⚠️  [{button_name}] Buton tıklanabilir değil, JS ile tıklanacak...")
                return ClickUtils.force_click_with_js(driver, element, None, "yellow", button_name)
            
            # Vurgula
            ClickUtils.highlight_element(driver, element, "green", 2, 0.3)
            
            # 1. DENEME: Normal click
            element.click()
            print(f"✅ [{button_name}] Normal click BAŞARILI!")
            return True
            
        except (ElementNotInteractableException, ElementClickInterceptedException) as e:
            # 2. DENEME: JS click
            print(f"🔄 [{button_name}] Görünmeyen/engellenen buton, JS ile tıklanıyor...")
            return ClickUtils.force_click_with_js(driver, element, None, "blue", button_name)
            
        except StaleElementReferenceException as e:
            # 3. DENEME: Element yeniden bulunmalı
            print(f"🔄 [{button_name}] Element kayboldu, yeniden bulunmalı")
            raise e
            
        except Exception as e:
            print(f"❌ [{button_name}] SmartClick sırasında beklenmedik hata: {str(e)}")
            return False
    
    @staticmethod
    def scroll_to_element(driver, element=None, xpath=None):
        """
        Elemente scroll yapar
        """
        try:
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            
            driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'center'});", 
                element
            )
            return True
        except Exception as e:
            print(f"❌ Scroll işlemi başarısız: {str(e)}")
            return False