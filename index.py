import time
import pathlib
import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.service import Service
from selenium.webdriver.common.action_chains import ActionChains

config = configparser.ConfigParser(interpolation=None, allow_no_value=True)
config.read("conf.ini")

driver = webdriver.Chrome(config["REQUIRED"]["web_driver_path"])
driver.set_window_size(1024, 768)
driver.get("https://www.facebook.com/")

# allow cookies
driver.find_element(By.XPATH, value='//*[@title="Only allow essential cookies"]').click()

# Login
driver.find_element(By.CSS_SELECTOR, value='#email').send_keys(config["REQUIRED"]["email"])
driver.find_element(By.CSS_SELECTOR, value='#pass').send_keys(config["REQUIRED"]["password"])
driver.find_element(By.XPATH, value='//*[@name="login"]').click()

time.sleep(2)
driver.get(config["REQUIRED"]["start_image_url"])

# Leave notification focus
zero_elem = driver.find_element(By.CSS_SELECTOR, value="body")
zero_elem.click()
zero_elem.click()

# Perform Download Media
time.sleep(2)
download = driver.find_element(By.CSS_SELECTOR, value="[aria-label=Изтегляне]")

step = 0
actions = ActionChains(driver)
prevDownload = "";

while True:
    time.sleep(1)
    step += 1
    try:
        # Breaking Condition
        if(prevDownload == download.get_attribute("href") or step == config.getint('DEFAULT', 'number_of_images')) :
            break
        prevDownload = download.get_attribute("href")

        # Download Media
        download.click()

        # Reset Cursor Position
        actions.move_to_element_with_offset(zero_elem, 0, 0).click()

        # Find Next Media
        if config.getint('DEFAULT', 'direction'):
            actions.move_by_offset( 460, 100 ).click().perform()
        else :
            actions.move_by_offset( -460, 100 ).click().perform()
    except :
        break

print("Next image is not found!")
print("Total downloaded images: {}".format(step - 1))