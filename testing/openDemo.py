from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ultralytics import YOLO
import cv2, os, time

optionsc = webdriver.ChromeOptions()
optionsc.add_argument('lang=en_US')
driver = webdriver.Chrome(options=optionsc)
driver.get('https://www.google.com/recaptcha/api2/demo')
model = YOLO('yolov8m.pt')

# grid4 = [[], [], [], []]
# grid3 = [['//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[3]'], ['//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[3]'], ['//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[3]']]
gridtype = 3

while True: # repeat until success
    
    try: # check if suceeded
        iframe = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        # check = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div')))
        print("iframe found")
        driver.switch_to.frame(iframe)
        x = driver.find_element(By.ID, 'recaptcha-anchor')
        print(x.get_attribute("aria-checked"))
    except TimeoutException:
        print("check time")
    time.sleep(1)

for x in range(3):
    try: # click button
            button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'g-recaptcha'))).click()
    except TimeoutException:
        print("btn time")
        break

    while True: # repeat until success
        try: # check if suceeded
            checked = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[3]/div[1]/div/div/span')))
            if checked.get_attribute("aria-checked") == "true":
                print("Success")
                break
            elif checked.get_attribute("aria-checked") == "false":
                print("Failed")
            else:
                print("Check Error")
                break
        except TimeoutException:
            print("check time")
            break

        try: # check type
            driver.switch_to.frame(iframe)
            captype = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-verify-button"]'))).text
            gridt = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect-target"]/table')))
            objtype = WebDriverWait(driver, 3).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect"]/div[2]/div[1]/div[1]/div/strong'))).text
            if gridt.get_attribute("class") == "rc-imageselect-table-44":
                gridtype = 4
            elif gridt.get_attribute("class") == "rc-imageselect-table-33":
                gridtype = 3
            else:
                print("Grid Error")
                break
        except TimeoutException:
            print("img time")
            break
        
        # captype, gridtype, objtype
        driver.switch_to.default_content()
    driver.switch_to.default_content()
    driver.refresh()
        
driver.quit()    