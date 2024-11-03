from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from flask import Flask, jsonify, request
import time  # Importing time to use sleep

app = Flask(__name__)

# Define the function for Selenium automation
def run_selenium_automation(email, password, listeners_emails):
    # Set up the browser (using Chrome in this example)
    driver = webdriver.Chrome()
    try:
        # Open the target page
        driver.get("https://app.mysoundwise.com/dashboard/subscribers")

        # Fill out the form
        # Locate email input by CSS selector
        email_input = driver.find_element(By.CSS_SELECTOR, ".SignInForm__Label-sc-1kk8vaz-3 + div input[type='email']")
        email_input.send_keys(email)

        # Locate password input by CSS selector
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys(password)

        # Locate and click the login button using the ID
        login_button = driver.find_element(By.ID, "appSigninBtnTest")
        login_button.click()

        # Wait for the page to load and for the Listeners button to be clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'dashboard__VerticalMenuItemTitle-sc-4xnn47-6') and contains(., 'Listeners')]"))
        ).click()
        print("Clicked on Listeners button successfully.")

        # Wait for the dropdown to be visible and interactable
        dropdown = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "styled__Select-b4uju-14"))
        )
        
        # Click the dropdown to open it and select the desired option
        dropdown.click()
        select = Select(dropdown)
        select.select_by_visible_text("Die YouTuber Insel")
        print("Selected the option 'Die YouTuber Insel.")

        # Wait for the Grant Access button to be clickable and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Grant Access')]"))
        ).click()
        print("Clicked on Grant Access button successfully.")

        # Wait for the textarea and fill in the email addresses
        textarea = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "textarea[placeholder='Enter listener email addresses, separated by commas']"))
        )
        textarea.send_keys(listeners_emails)
        print("Filled in the listener email addresses.")

        # Wait for the Submit button to be clickable and click it
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Submit')]"))
        ).click()
        print("Clicked on Submit button successfully.")

        # Delay to observe the result
        time.sleep(10)
        
        return {"status": "success", "message": "Automation completed successfully"}

    except TimeoutException:
        return {"status": "error", "message": "Timeout: Element not found or not clickable"}
    except Exception as e:
        return {"status": "error", "message": f"An error occurred: {e}"}
    finally:
        # Close the browser
        driver.quit()

# Define the API route
@app.route('/run_automation', methods=['POST'])
def run_automation():
    # Extract data from the request
    data = request.json
    email = data.get("email")
    password = data.get("password")
    listeners_emails = data.get("listeners_emails")

    # Ensure all required data is provided
    if not email or not password or not listeners_emails:
        return jsonify({"status": "error", "message": "Missing required parameters"}), 400

    # Run the Selenium automation function
    result = run_selenium_automation(email, password, listeners_emails)
    return jsonify(result)


# Run the Flask application
if __name__ == "__main__":
    app.run(debug=True)
