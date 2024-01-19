import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By  # import the By class
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

username = "FMEX000011"
password = "W9W9Kv£E*M7mt}7~"
attempt = 0  # Initialize the attempt variable
max_attempts = 3  # Define the maximum number of attempts

logging.basicConfig(filename='deleteAvayaRecording.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

options = Options()
# Use defult profile on Chrome
options.add_argument("user-data-dir=C:\\Users\\cguer\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
# Set up the driver to use the chrome browser default user to keep cookies
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)

# Login to Avaya
# Use the url for the required search parameters to delete recordings
driver.get("https://wfo-app.glb.nar.fusion.avayacloud.com/wfo/ui/#wsm%5Bws%5D=qm_SearchResultsWorkspace&navparent%5BworkspaceId%5D=qm_SearchWorkspace&qm_ctx%5Bts%5D=1705640819247")
driver.find_element(By.ID, "username").send_keys(username)  # use By.ID
driver.find_element(By.CLASS_NAME, "loginButtonLabel").click()
driver.find_element(By.ID, "password").send_keys(password)  # use By.ID
driver.find_element(By.CLASS_NAME, "loginButtonLabel").click()

# Run until no recordings found


while True:
    try:
        # Try to find the element
        element = driver.find_element(By.XPATH, '//*[contains(@class, "verint-search-label-found")]')
        # If the element's text is 'Retrieved 0 items', break the loop
        if element.text == 'Retrieved 0 items':
            logging.info("No recordings found")
            break
        else:
            time.sleep(2)
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[6]/div/div').click()
            #driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/a[4]/span/span/span[1]').click()
            for attempt in range(max_attempts):
                try:
                    # Click the first element
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/a[4]/span/span/span[1]').click()
                    try:
                        # Try to click the first of the two elements
                        driver.find_element(By.XPATH, '/html/body/div[22]/div[4]/div/div/a[2]/span/span/span[2]').click()
                        logging.info("Recording deleted")
                        break
                    except NoSuchElementException:
                        try:
                            # If the first element is not found, try to click the second element
                            driver.find_element(By.XPATH, '/html/body/div[20]/div[4]/div/div/a[2]/span/span').click()
                            logging.info("Recording deleted")
                            break
                        except NoSuchElementException:
                            # If the second element is not found, try to click the third element
                            driver.find_element(By.XPATH, '/html/body/div[21]/div[4]/div/div/a[2]/span/span/span[2]').click()
                            logging.info("Recording deleted")
                            break
                except NoSuchElementException:
                    # If neither element is found, return to search results
                    logging.error("Delete button not found, returning to search results")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2]').click()
                    break
                except TimeoutException:
                    logging.error("Timeout while waiting for the element to be clickable, attempt: %s", attempt + 1)
                    if attempt + 1 == max_attempts:
                        raise  # If this was the last attempt, re-raise the exception so that the script fails          
    except NoSuchElementException:
        # If the element is not found, wait for a second and then continue the loop
        break