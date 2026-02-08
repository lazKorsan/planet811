# SendKeysUtils.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    ElementNotInteractableException, 
    StaleElementReferenceException,
    InvalidElementStateException,
    NoSuchElementException
)
import time

class SendKeysUtils:
    
    @staticmethod
    def highlight_input(driver, element, color="red", border_width=3, duration=1):
        """
        Input elementini belirtilen renkle vurgular
        """
        try:
            # Mevcut stilini sakla
            original_style = element.get_attribute("style")
            
            # Yeni stil ekle
            highlight_style = f"border: {border_width}px solid {color}; background-color: #f0f8ff;"
            driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                 element, f"{original_style}; {highlight_style}")
            
            # Belirtilen süre bekleyip eski haline döndür
            if duration > 0:
                time.sleep(duration)
                driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", 
                                     element, original_style)
            
            return True
        except Exception as e:
            print(f"❌ Input vurgulanamadı: {str(e)}")
            return False
    
    @staticmethod
    def check_input_field(driver, element, input_name="Unknown"):
        """
        Input alanının durumunu kontrol eder
        """
        try:
            # Temel özellikler
            is_displayed = element.is_displayed()
            is_enabled = element.is_enabled()
            is_editable = element.get_attribute("readonly") is None and element.get_attribute("disabled") is None
            
            # Mevcut değer
            current_value = element.get_attribute("value") or ""
            placeholder = element.get_attribute("placeholder") or ""
            
            # Input tipi
            input_type = element.get_attribute("type") or "text"
            tag_name = element.tag_name
            
            # CSS durumu
            opacity = element.value_of_css_property("opacity")
            pointer_events = element.value_of_css_property("pointer-events")
            
            return {
                "input_name": input_name,
                "editable": is_displayed and is_enabled and is_editable,
                "displayed": is_displayed,
                "enabled": is_enabled,
                "readonly": element.get_attribute("readonly") is not None,
                "disabled": element.get_attribute("disabled") is not None,
                "current_value": current_value,
                "placeholder": placeholder,
                "input_type": input_type,
                "tag_name": tag_name,
                "maxlength": element.get_attribute("maxlength"),
                "required": element.get_attribute("required") is not None,
                "css_editable": opacity != "0" and pointer_events != "none",
                "opacity": opacity,
                "pointer_events": pointer_events
            }
        except Exception as e:
            print(f"❌ [{input_name}] Input kontrolü başarısız: {str(e)}")
            return {"editable": False, "displayed": False, "enabled": False}
    
    @staticmethod
    def force_send_keys_with_js(driver, element=None, xpath=None, color="red", text="", input_name="Input"):
        """
        JS ile zorla yazma - Etkileşime kapalı inputlar için
        """
        print(f"⚡️ [{input_name}] JS ile zorla yazma başlatıldı: '{text}'")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Input kontrolü yap
            input_info = SendKeysUtils.check_input_field(driver, element, input_name)
            
            print(f"📋 [{input_name}] INPUT BİLGİLERİ:")
            print(f"   • Düzenlenebilir mi: {input_info['editable']}")
            print(f"   • Görünür mü: {input_info['displayed']}")
            print(f"   • Etkin mi: {input_info['enabled']}")
            print(f"   • Readonly: {input_info['readonly']}")
            print(f"   • Disabled: {input_info['disabled']}")
            print(f"   • Mevcut değer: '{input_info['current_value']}'")
            print(f"   • Placeholder: '{input_info['placeholder']}'")
            print(f"   • Tip: {input_info['input_type']}")
            print(f"   • Max length: {input_info['maxlength']}")
            
            # Input'u vurgula
            if color:
                SendKeysUtils.highlight_input(driver, element, color, 3, 1)
            
            # JS ile scroll ve değer ata
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            driver.execute_script("arguments[0].value = arguments[1];", element, text)
            
            # Değişiklik event'larını tetikle
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, element)
            
            print(f"✅ [{input_name}] JS ile zorla yazma BAŞARILI!")
            return True
            
        except Exception as e:
            print(f"❌ [{input_name}] JS ile zorla yazma BAŞARISIZ: {str(e)}")
            return False
    
    @staticmethod
    def smart_send_keys(driver, element=None, xpath=None, text="", input_name="Input", color="green"):
        """
        Akıllı SendKeys - Tüm senaryolar için
        """
        print(f"⌨️ [{input_name}] SmartSendKeys başlatıldı: '{text}'")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Input kontrolü yap
            input_info = SendKeysUtils.check_input_field(driver, element, input_name)
            
            if not input_info['editable']:
                print(f"⚠️  [{input_name}] Input düzenlenebilir değil, JS ile yazılacak...")
                SendKeysUtils.highlight_input(driver, element, "yellow", 2, 0.5)
                return SendKeysUtils.force_send_keys_with_js(driver, element, None, "yellow", text, input_name)
            
            # Vurgula
            SendKeysUtils.highlight_input(driver, element, color, 2, 0.3)
            
            # 1. DENEME: Normal sendKeys
            element.clear()
            element.send_keys(text)
            print(f"✅ [{input_name}] Normal sendKeys BAŞARILI!")
            return True
            
        except ElementNotInteractableException as e:
            # 2. DENEME: JS ile sendKeys
            print(f"🔄 [{input_name}] Element etkileşime kapalı, JS ile yazılıyor...")
            return SendKeysUtils.force_send_keys_with_js(driver, element, None, "blue", text, input_name)
            
        except InvalidElementStateException as e:
            # 3. DENEME: Clear + sendKeys
            print(f"🔄 [{input_name}] Element durumu geçersiz, temizleyip yazılıyor...")
            SendKeysUtils.clear_with_js(driver, element)
            return SendKeysUtils.send_keys_with_js(driver, element, text, input_name)
            
        except StaleElementReferenceException as e:
            # 4. DENEME: Element yenilenmiş
            print(f"🔄 [{input_name}] Element referansı geçersiz. Elementi yeniden bulmalısınız.")
            raise e
            
        except Exception as e:
            print(f"❌ [{input_name}] SmartSendKeys sırasında beklenmedik hata: {str(e)}")
            return False
    
    @staticmethod
    def smart_send_keys_with_wait(driver, element=None, xpath=None, text="", timeout_seconds=10, input_name="Input"):
        """
        Beklemeli SendKeys - Düzeltilmiş versiyon
        """
        print(f"⏳ [{input_name}] Beklemeli SmartSendKeys: '{text}' (timeout: {timeout_seconds}s)")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Input'u vurgula
            SendKeysUtils.highlight_input(driver, element, "orange", 2, 0.5)
            
            # Bekle ve yaz
            wait = WebDriverWait(driver, timeout_seconds)
            wait.until(EC.element_to_be_clickable(element))
            
            element.clear()
            element.send_keys(text)
            print(f"✅ [{input_name}] Beklemeli sendKeys BAŞARILI!")
            return True
            
        except TimeoutException:
            print(f"❌ [{input_name}] Element {timeout_seconds} saniyede hazır olmadı, JS ile yazılıyor...")
            return SendKeysUtils.force_send_keys_with_js(driver, element, None, "red", text, input_name)
            
        except Exception as e:
            print(f"❌ [{input_name}] Beklenmeyen hata, normal SmartSendKeys deneniyor...")
            return SendKeysUtils.smart_send_keys(driver, element, None, text, input_name)
    
    @staticmethod
    def slow_send_keys(driver, element=None, xpath=None, text="", delay_ms=100, input_name="Input"):
        """
        Yavaş SendKeys - İnsan gibi yazar
        """
        print(f"🐌 [{input_name}] Yavaş yazılıyor: '{text}' ({delay_ms}ms gecikmeli)")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Vurgula
            SendKeysUtils.highlight_input(driver, element, "purple", 2, 0.5)
            
            element.clear()
            
            for i, char in enumerate(text):
                element.send_keys(char)
                print(f"   ↳ Karakter {i+1}/{len(text)}: '{char}'")
                time.sleep(delay_ms / 1000)  # ms'yi saniyeye çevir
            
            print(f"✅ [{input_name}] Yavaş sendKeys BAŞARILI!")
            return True
            
        except Exception as e:
            print(f"❌ [{input_name}] Yavaş yazma başarısız, normal yazılıyor...")
            return SendKeysUtils.smart_send_keys(driver, element, None, text, input_name)
    
    @staticmethod
    def clear_and_send_keys(driver, element=None, xpath=None, text="", input_name="Input"):
        """
        Temizle & Yaz - Önce temizler sonra yazar
        """
        print(f"🧹 [{input_name}] Temizle & Yaz: '{text}'")
        
        try:
            # Element bulunmamışsa xpath ile bul
            if element is None and xpath:
                element = driver.find_element(By.XPATH, xpath)
            elif element is None:
                raise ValueError("Element veya XPath sağlanmalıdır")
            
            # Vurgula
            SendKeysUtils.highlight_input(driver, element, "lightblue", 2, 0.5)
            
            element.clear()
            time.sleep(0.5)  # Kısa bekleme
            element.send_keys(text)
            
            print(f"✅ [{input_name}] Clear & SendKeys BAŞARILI!")
            return True
            
        except Exception as e:
            print(f"❌ [{input_name}] Clear başarısız, JS ile temizlenip yazılıyor...")
            SendKeysUtils.clear_with_js(driver, element)
            return SendKeysUtils.send_keys_with_js(driver, element, text, input_name)
    
    # ✅ PRIVATE YARDIMCI METHODLAR
    @staticmethod
    def send_keys_with_js(driver, element, text, input_name="Input"):
        """
        JS ile yazma yardımcı methodu
        """
        try:
            driver.execute_script("arguments[0].value = arguments[1];", element, text)
            
            # Tüm gerekli event'ları tetikle
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('keyup', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
            """, element)
            
            print(f"✅ [{input_name}] JS sendKeys BAŞARILI!")
            return True
        except Exception as e:
            print(f"❌ [{input_name}] JS sendKeys de başarısız: {str(e)}")
            return False
    
    @staticmethod
    def clear_with_js(driver, element):
        """
        JS ile temizleme
        """
        try:
            driver.execute_script("arguments[0].value = '';", element)
            
            # Clear event'larını tetikle
            driver.execute_script("""
                arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
                arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            """, element)
            
            return True
        except Exception as e:
            print(f"❌ JS clear başarısız: {str(e)}")
            return False
    
    @staticmethod
    def validate_input_after_fill(driver, element, expected_text, input_name="Input"):
        """
        Yazma işleminden sonra input değerini doğrular
        """
        try:
            # Biraz bekle (AJAX vs. için)
            time.sleep(0.5)
            
            # Mevcut değeri al
            current_value = element.get_attribute("value") or ""
            
            print(f"🔍 [{input_name}] DOĞRULAMA:")
            print(f"   • Beklenen: '{expected_text}'")
            print(f"   • Gerçek: '{current_value}'")
            print(f"   • Eşleşme: {current_value == expected_text}")
            
            if current_value == expected_text:
                SendKeysUtils.highlight_input(driver, element, "lightgreen", 2, 1)
                return True
            else:
                SendKeysUtils.highlight_input(driver, element, "orange", 2, 1)
                return False
                
        except Exception as e:
            print(f"❌ [{input_name}] Doğrulama başarısız: {str(e)}")
            return False