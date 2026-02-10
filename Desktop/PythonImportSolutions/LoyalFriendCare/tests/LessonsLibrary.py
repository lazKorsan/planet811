import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import time

from utils.reusable_methods import setup_driver

driver = setup_driver()
driver.get("https://docs.python.org/3/using/windows.html#configuration")
time.sleep(5)

driver.get("https://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#getting-more-information")
time.sleep(5)



# Driver'ı kapat
driver.quit()