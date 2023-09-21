from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get('https://www.google.com/recaptcha/api2/demo')

for x in range(21, 26):
    try:
        button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'g-recaptcha'))).click()
    except TimeoutException:
        print("btn time")
        break
    
    try: 
        iframe = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[4]/iframe')))
        driver.switch_to.frame(iframe)
        img = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect-target"]/table')))
        img.screenshot('images/orig/captcha' + str(x) + '.png')
        driver.switch_to.default_content()
    except TimeoutException:
        print("img time")
        break

    driver.refresh()

driver.quit()