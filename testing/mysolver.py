from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from ultralytics import YOLO
import cv2, os

driver = webdriver.Chrome()
driver.get('https://www.google.com/recaptcha/api2/demo')
model = YOLO('yolov8m.pt')

grid4 = []
grid3 = [['//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[3]'], ['//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[2]/td[3]'], ['//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[1]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[2]', '//*[@id="rc-imageselect-target"]/table/tbody/tr[3]/td[3]']]

for x in range(10):
    try:
        button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CLASS_NAME, 'g-recaptcha'))).click()
        
    except TimeoutException:
        print("btn time")
        break

    try: 
        iframe = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[4]/iframe')))
        driver.switch_to.frame(iframe)
        captype = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="recaptcha-verify-button"]')))
        gridtype = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="rc-imageselect-target"]/table')))
        
        if gridtype.get_attribute("class") == "rc-imageselect-table-44":
            print(4)
        elif gridtype.get_attribute("class") == "rc-imageselect-table-33":
            print(3)
        else:
            print("Grid Error")
        
        if captype.text == "확인":
            print("확인")
        elif captype.text == "건너뛰기":
            print("건너뛰기")
        else:
            print("Type Error")

        driver.switch_to.default_content()
    
    except TimeoutException:
        print("img time")
        break

    driver.refresh()

driver.quit()    