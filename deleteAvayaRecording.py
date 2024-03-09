# Delete Avaya recordings from search results using Selenium, by Cuauhtemoc Guerrero 2023-12-15
# Chrome browser is required

# We need to use the Chrome browser default user to keep cookies
# To do this, we need to find the default user profile directory
# To find the default user profile directory, open Chrome and type chrome://version in the address bar
# The profile path will be listed under Profile Path
# Copy the path and paste it in the options.add_argument("user-data-dir=") line below
# The path should look something like this: C:\\Users\\coder\\AppData\\Local\\Google\\Chrome\\User Data\\Default
# The path must be double backslash, not single backslash, must end with \\Default, must not have any spaces, must be in double quotes, and must be preceded by user-data-dir=.
#
#The credentials to access Avaya cloud site are required and must be entered in the username and password variables below
#
# To succesfully run this script, the search with the required parameters must first be manually create
# then the url must be copied and entered in the driver.get("") line below.

import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By  # import the By class
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Enter the username and password to access Avaya cloud site
username = "username"
password = "password"

attempt = 0  # Initialize the attempt variable
max_attempts = 3  # Define the maximum number of attempts
deleted_count = 0  # Initialize counter
start_time = time.time()  # Capture start time

logging.basicConfig(filename='deleteAvayaRecording.log', level=logging.INFO, format='%(asctime)s %(message)s')

# Selenium setup options
options = Options()
# Use defult profile on Chrome
options.add_argument("user-data-dir=C:\\Users\\cguer\\AppData\\Local\\Google\\Chrome\\User Data\\Default")
# Set up the driver to use the chrome browser default user to keep cookies
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

# Login to Avaya
# Enter the url for the required search parameters to delete recordings
driver.get("https://wfo-app.glb.nar.company.avayacloud.com/wfo/ui/#wsm%5Bws%5D=qm_SearchResultsWorkspace&navparent%5BworkspaceId%5D=qm_SearchWorkspace&qm_ctx%5Bts%5D=1706633018618")

# Enter the username and password to access Avaya cloud site
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
        if element.text == 'Found 0 results':
            logging.info("No recordings found")
            break
        else:
            # If recordings are found, click expansion button
            time.sleep(3)
            driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[2]/div[4]/div/div/div[2]/div/div/div/div/div[2]/div/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div[6]/div/div').click()
            for attempt in range(max_attempts):                
                try:
                    # Try to click the delete button
                    wait1 = WebDriverWait(driver, 2)
                    element1 = wait1.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[2]/div/div/div/div/div/a[4]/span/span/span[1]')))
                    element1.click()
                    # Confirm delete
                    driver.find_element(By.XPATH, '/html/body/div[20]/div[4]/div/div/a[2]/span/span | /html/body/div[21]/div[4]/div/div/a[2]/span/span/span[2] | /html/body/div[22]/div[4]/div/div/a[2]/span/span/span[2] | /html/body/div[23]/div[4]/div/div/a[2]/span/span/span[2]').click()
                    #Increment counter
                    deleted_count += 1
                    minutes, seconds = divmod(time.time() - start_time, 60)
                    logging.info(f"Recording deleted, count: {deleted_count}, elapsed time: {minutes} minutes {seconds:.1f} seconds")
                    print(f"Recording deleted, count: {deleted_count}")
                    break
                except NoSuchElementException:
                    # If delete button element is not found, return to search results
                    logging.error("Delete button not found, returning to search results")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2] | /html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a/span/span/span[2]').click()
                    break
                except TimeoutException:
                    # If the expansion button is not found, try return to search results
                    logging.info("Expasion button not found, returning to search results (Timeout))")
                    driver.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a[2]/span/span/span[2] | /html/body/div[1]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[2]/div/div/div[1]/div/div/div/div/div/a/span/span/span[2]').click() #click back to search results
                    # break
                    logging.error("Timeout while waiting for the element button to be clickable, attempt: %s", attempt + 1)
                    if attempt + 1 == max_attempts:
                       raise  # If this was the last attempt, re-raise the exception so that the script fails          
    except NoSuchElementException:
        # If the expansion button is not found, try return to search results
        logging.info("Expasion button not found, returning to search results (No Such Element)")
        
# ToDo: print the number of recordings deleted and time taken        
end_time = time.time()  # Capture end time
running_time = end_time - start_time  # Calculate running time
fminutes, fseconds = divmod(running_time, 60)
logging.info(f"Total recordings deleted: {deleted_count}, Total running time: {fminutes} minutes {fseconds:.1f} seconds")
print(f"Total recordings deleted: {deleted_count}, Total running time: {fminutes} minutes {fseconds:.1f} seconds")
