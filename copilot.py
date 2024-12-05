from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

# Folder paths for different categories
folders = {
    'people': './images/people',
    'cars': './images/cars',
    'houses': './images/houses'
}

# Set up Chrome options to use the custom profile
options = webdriver.ChromeOptions()
# Replace with the path to your Chrome user data directory
options.add_argument("user-data-dir=C:/temp/chrome-profile")

# Initialize WebDriver with the custom profile
driver = webdriver.Chrome(options=options)

# Navigate to Copilot
url = "https://copilot.microsoft.com/"
driver.get(url)

# Function to ensure message is processed before sending the next
def wait_for_copilot_response():
    try:
        print("Waiting for Copilot response...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@data-content='ai-message']"))
        )

        # Scroll the element into view
        element = driver.find_element(By.XPATH, "//div[@data-content='ai-message']")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        print("Copilot response received.")
    except Exception as e:
        print(f"Error while waiting for response: {e}")
        print("Page source for debugging:")
        print(driver.page_source)

# Step 1: Initialize Copilot with the prompt
initial_text = """
Copilot can you analyze the following images by:
2c. If a person, what activity are they doing and how many people?
2b. If a car, what is the type and what side is the car facing?
2a. If a house, what is the type and the weather conditions? (Type: Colonial, Farmhouse, Modern; Weather: Sunny, Raining, Night, Snowing)
1. Determine what the object is.
"""
try:
    user_input_box = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "#userInput"))
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", user_input_box)
    time.sleep(1)
    user_input_box = WebDriverWait(driver, 10).until(
        EC.visibility_of(user_input_box)
    )
    user_input_box.clear()
    user_input_box.send_keys(initial_text)
    actions = ActionChains(driver)
    actions.send_keys(Keys.RETURN).perform()
    print("Sent initial analysis prompt to Copilot.")
    wait_for_copilot_response()
    time.sleep(3)
except Exception as e:
    print("Error while sending initial prompt:", e)
    driver.quit()
    exit()

# Function to upload images, click submit and retrieve results
def upload_images_and_submit(folder_path, category):
    results = []
    for image_file in os.listdir(folder_path):
        if image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, image_file)
            try:
                # Locate and upload the image file
                upload_input = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
                )
                upload_input.send_keys(os.path.abspath(image_path))
                print(f"Uploaded {image_file}")
                time.sleep(2)  # Short wait for the upload to register
            except Exception as e:
                print(f"Error uploading {image_file}: {e}")
                continue

            try:
                # Click the submit button
                submit_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[@title='Submit message']"))
                )
                submit_button.click()
                print(f"Submitted {image_file} for processing.")
                time.sleep(2)  # Short wait before attempting result retrieval
            except Exception as e:
                print(f"Error clicking submit button for {image_file}: {e}")
                continue

            try:
                # Wait for at least one result element with the specified class to appear
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@class='space-y-3 break-words']"))
                )

                # Locate all result elements
                result_elements = driver.find_elements(By.XPATH, "//div[@class='space-y-3 break-words']")

                # Introduce a short delay to ensure the latest message is fully rendered
                time.sleep(10)

                if result_elements:
                    # Re-fetch elements to ensure the latest message is included
                    result_elements = driver.find_elements(By.XPATH, "//div[@class='space-y-3 break-words']")

                    # Get the very last result element (most recent message)
                    latest_result_element = result_elements[-1]

                    # Scroll to the latest element
                    driver.execute_script("arguments[0].scrollIntoView(true);", latest_result_element)

                    # Extract text from all <p> elements within the result
                    paragraphs = latest_result_element.find_elements(By.TAG_NAME, "p")
                    result_text = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

                    # Validate that result_text contains meaningful content
                    if result_text:
                        print(f"Image: {image_file}, Analysis: {result_text}")
                        results.append({'image': image_file, 'category': category, 'analysis': result_text})
                    else:
                        print(f"No meaningful content found for {image_file}.")
                else:
                    print(f"No result found for {image_file}.")
            except Exception as e:
                print(f"Error retrieving result for {image_file}: {e}")
                print("Page source for debugging:")
                print(driver.page_source)
                continue
    return results

# Step 2: Iterate over categories and folders to upload images
all_results = []
for category, folder_path in folders.items():
    print(f"Processing category: {category}")
    results = upload_images_and_submit(folder_path, category)
    all_results.extend(results)

# Step 3: Save results to a file
with open('analysis_results.json', 'w') as f:
    json.dump(all_results, f, indent=4)

# Step 4: Close the browser
driver.quit()
