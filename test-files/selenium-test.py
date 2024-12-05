from selenium import webdriver

# Start the browser
driver = webdriver.Chrome()  # Or use `webdriver.Firefox()` for GeckoDriver
driver.get("https://example.com")

# Close the browser
driver.quit()
