from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time

# Web driver setup
driver = webdriver.Chrome()

# Sample image path
test_image_path = os.path.abspath('./images/people/running 1.jpg')  # Replace with the path to your test image

# Step 1: Navigate to Copilot
url = "https://copilot.microsoft.com/"
driver.get(url)

# Step 2: Click "Get started" button
try:
    get_started_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Get started']")))
    get_started_button.click()
    print("Clicked 'Get Started' button.")
except Exception as e:
    print("Error while clicking 'Get Started' button:", e)
    driver.quit()
    exit()

# Step 3: Enter username ("Tester")
try:
    username_input = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "userInput")))
    username_input.click()
    username_input.clear()
    username_input.send_keys("Tester")  # Automatically input username
    username_input.send_keys(Keys.RETURN)  # Submit the username
    print("Entered 'Tester' as the username.")
except Exception as e:
    print("Error while entering username:", e)
    driver.quit()
    exit()

# Step 4: Skip voice selection
try:
    next_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Next']")))
    next_button.click()
    print("Clicked 'Next' button to skip voice selection.")
except Exception as e:
    print("Error while clicking 'Next' button:", e)
    driver.quit()
    exit()

# Step 5: Upload test image
try:
    # Locate the file input element
    upload_input = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']")))
    upload_input.send_keys(test_image_path)  # Send the test image path to the file input
    print(f"Uploaded test image: {test_image_path}")

    # Optional: Wait for upload confirmation or processing message
    time.sleep(5)  # Adjust time if needed based on upload speed

except Exception as e:
    print("Error during image upload:", e)
    driver.quit()
    exit()

# Step 6: Verify Upload and Close Browser
try:
    # Example: Check if a processing message or result appears
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'result-text')]"))
    )
    print("Image upload was successful and processed.")

except Exception as e:
    print("Image upload may not have been processed correctly:", e)

# Close the browser
driver.quit()
