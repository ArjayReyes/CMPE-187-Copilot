from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up the Chrome options for the temporary profile
options = Options()
options.add_argument("user-data-dir=C:/temp/chrome-profile")  # Temporary profile directory

# Set up the WebDriver
chrome_driver_path = "C:/path-to-your-chromedriver.exe"  # Update this path
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Open the login page
driver.get("https://example.com/login")  # Replace with your login URL

# Pause the script to allow manual login
input("Please log in manually, then press Enter to continue...")

# Close the browser after manual login
driver.quit()
