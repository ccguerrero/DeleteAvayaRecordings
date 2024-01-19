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
deleted_count = 0  # Initialize counter
start_time = time.time()  # Capture start time

logging.basicConfig(filename='deleteAvayaRecording.log', level=logging.INFO, format='%(asctime)s %(message)s')

options = Options()
# Use defult profile on Chrome
options.add_argument("user-data-dir=C:\\Users\\cguer\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
# Set up the driver to use the chrome browser default user to keep cookies
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# Login to Avaya
# Use the url for the required search parameters to delete recordings
driver.get("https://wfo-app.glb.nar.fusion.avayacloud.com/wfo/ui/#wsm%5Bws%5D=qm_SearchResultsWorkspace&navparent%5BworkspaceId%5D=qm_SearchWorkspace&qm_ctx%5Bts%5D=1705640819247")
driver.find_element(By.ID, "username").send_keys(username)  # use By.ID
driver.find_element(By.CLASS_NAME, "loginButtonLabel").click()
logging.info("Username entered")
driver.find_element(By.ID, "password").send_keys(password)  # use By.ID
driver.find_element(By.CLASS_NAME, "loginButtonLabel").click()
logging.info("Password entered")

# Run until no recordings found


while True:
    try:
        # Try to find the number of recordings left on search
        element = driver.find_element(By.XPATH, '//*[contains(@class, "verint-search-label-found")]')
        # If the element's text is 'Retrieved 0 items', break the loop
        if element.text == 'Retrieved 0 items':
            logging.info("No recordings found")
            break
        else:
            time.sleep(2)
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[6]/div/div').click()
            for attempt in range(max_attempts):                
                try:
                    wait1 = WebDriverWait(driver, 2)
                    # Click the first element
                    element1 = wait1.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/a[4]/span/span/span[1]')))
                    element1.click()
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
                        except TimeoutException:
                            logging.error("Timeout while waiting for the delete button to be clickable, attempt: %s", attempt + 1)
                            if attempt + 1 == max_attempts:
                                raise  # If this was the last attempt, re-raise the exception so that the script fails
                except NoSuchElementException:
                    # If neither element is found, return to search results
                    logging.error("Delete button not found, returning to search results")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2]').click()
                    break
                except TimeoutException:
                    # If the expansion button is not found, try return to search results
                    logging.info("Expasion button not found, returning to search results")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2]').click() #click back to search results
                    # break
                    logging.error("Timeout while waiting for the delete button to be clickable, attempt: %s", attempt + 1)
                    if attempt + 1 == max_attempts:
                       raise  # If this was the last attempt, re-raise the exception so that the script fails          
    except NoSuchElementException:
        # If the expansion button is not found, try return to search results
        logging.info("Expasion button not found, returning to search results")
        #driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2]').click() #click back to search results
end_time = time.time()  # Capture end time
running_time = end_time - start_time  # Calculate running time
logging.info(f"Total recordings deleted: {deleted_count}, Total running time: {running_time} seconds (end)")
