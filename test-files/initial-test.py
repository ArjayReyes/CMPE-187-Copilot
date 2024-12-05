from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Web driver setup
driver = webdriver.Chrome()

# Navigate to Copilot
url = "https://copilot.microsoft.com/"
driver.get(url)

# Wait for the "Get started" button to appear and click it
try:
    # Wait until the "Get Started" button is visible and click it
    get_started_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Get started']")))
    get_started_button.click()
    print("Clicked 'Get Started' button.")
except Exception as e:
    print("Error while clicking 'Get Started' button:", e)
    driver.quit()
    exit()

# Wait for the "Your first name" input to appear and enter the username
try:
    # Wait until the "Your first name" text area is visible
    username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "userInput")))
    username_input.clear()
    username_input.send_keys("Tester")  # Automatically input username
    username_input.send_keys(Keys.RETURN)  # Submit the username
    print("Entered 'Tester' as the username.")
except Exception as e:
    print("Error while entering username:", e)
    driver.quit()
    exit()

# Wait for the "Next" button (to skip voice selection) to appear and click it
try:
    # Wait until the "Next" button is visible and click it
    next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Next']")))
    next_button.click()
    print("Clicked 'Next' button to skip voice selection.")
except Exception as e:
    print("Error while clicking 'Next' button:", e)
    driver.quit()
    exit()

# Proceed with any other interactions (e.g., image uploads) here...
# Example of waiting for the next element, uploading images, etc.

# Close the browser after the operations
driver.quit()
