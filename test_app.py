import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service # Or Firefox/Edge service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Optional: Specify WebDriver path if not in PATH
# webdriver_path = '/path/to/your/chromedriver'
# service = Service(executable_path=webdriver_path)

class TravelEasyAppTests(unittest.TestCase):

    def setUp(self):
        # Initialize WebDriver (using Chrome in this example)
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless') # Optional: Run headless
        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        self.driver = webdriver.Chrome(options=options)
        # Use WebDriverWait instead of implicit wait for more control
        self.wait = WebDriverWait(self.driver, 10) # Wait up to 10 seconds
        self.base_url = "http://127.0.0.1:5000" # Assuming app runs locally on port 5000
        # No initial navigation here, start fresh in the test

    def tearDown(self):
        # Close the browser window
        self.driver.quit()

    def _login(self, username="admin", password="admin"): # Default credentials
        """Helper method to log in."""
        driver = self.driver
        driver.get(self.base_url + "/login") # Ensure we start at login page
        print(f"Attempting login as '{username}'...")

        # Find login form elements using WebDriverWait
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Sign In']")))

        username_field.clear() # Clear fields in case of reuse
        password_field.clear()
        username_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()

        try:
            # 1. Wait for the dashboard URL
            self.wait.until(EC.url_to_be(self.base_url + "/dashboard"))

            # 2. Wait for the presence of the container element using its class
            container_xpath = "//div[contains(@class, 'user-greeting')]"
            welcome_container = self.wait.until(EC.presence_of_element_located((By.XPATH, container_xpath)))

            # 3. Verify the text within the container
            container_text = welcome_container.text
            if not ("Welcome back," in container_text and username in container_text):
                self.fail(f"Login Succeeded (URL is /dashboard), but container text did not match. Expected 'Welcome back, {username}'. Found text: '{container_text}'")
            print(f"Login successful for '{username}'.")

        except TimeoutException:
            # If either wait above times out, THEN check if it was a login failure
            current_url_after_wait = driver.current_url
            if "/dashboard" not in current_url_after_wait:
                try:
                    self.wait.until(EC.url_contains("/login")) # Check if back on login page
                    error_message = self.wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]")))
                    self.fail(f"Login failed for '{username}'. Found error message: '{error_message.text}'")
                except TimeoutException:
                    self.fail(f"Login failed for '{username}'. Did not redirect to /dashboard or show error on /login. Current URL: {current_url_after_wait}")
                except NoSuchElementException:
                     self.fail(f"Login failed for '{username}'. Redirected back to /login but no error message found. Current URL: {current_url_after_wait}")
            else:
                self.fail(f"Login Succeeded for '{username}' (URL is /dashboard), but failed to find welcome container element with XPath: {container_xpath}. Current URL: {current_url_after_wait}")
        except Exception as e:
            self.fail(f"An unexpected error occurred during login verification for '{username}': {e}")


    def test_signup_and_login(self):
        """Tests signing up a new user and then logging in with those credentials."""
        print("Running test_signup_and_login...")
        driver = self.driver
        driver.get(self.base_url + "/login") # Start at login page for signup link

        # --- Sign Up Phase ---
        print("Navigating to signup page...")
        signup_link = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Create Account']")))
        signup_link.click()

        self.wait.until(EC.url_to_be(self.base_url + "/signin"))
        self.assertEqual(driver.current_url, self.base_url + "/signin")
        print("On signup page.")

        # Generate unique credentials for signup
        timestamp = int(time.time())
        new_username = f"testuser_{timestamp}" # Make username more specific
        new_email = f"testuser_{timestamp}@example.com"
        new_password = "testpassword123"
        print(f"Generated credentials: Username='{new_username}', Email='{new_email}'")

        # Find signup form elements
        username_field = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        submit_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Account']")))

        # Enter new user details
        username_field.send_keys(new_username)
        email_field.send_keys(new_email)
        password_field.send_keys(new_password)
        print("Submitting signup form...")
        submit_button.click()

        # Wait for redirection back to login page after signup
        self.wait.until(EC.url_to_be(self.base_url + "/login"))
        print("Signup successful, redirected to login page.")
        # --- End Sign Up Phase ---

        # --- Login Phase ---
        # Now, use the _login helper with the newly created credentials
        self._login(new_username, new_password)
        # --- End Login Phase ---

        print("test_signup_and_login PASSED")

    # --- NEW TEST CASE ---
    def test_add_package_to_cart(self):
        """Tests adding a package to the cart and verifying it."""
        print("Running test_add_package_to_cart...")
        driver = self.driver
        # Use admin credentials, ensure this user exists
        self._login("admin", "admin") 

        # --- Booking Phase ---
        # Find the "Book Now" button for the first package (Paris)
        print("Finding 'Book Now' button for the first package...")
        book_button_locator = (By.XPATH, "(//button[normalize-space()='Book Now'])[1]")
        # Find the element first to scroll it
        book_button = self.wait.until(EC.presence_of_element_located(book_button_locator)) 

        # Find package name more reliably
        package_card = driver.find_element(By.XPATH, "(//div[contains(@class, 'dashboard-card')])[1]")
        package_name = package_card.find_element(By.XPATH, ".//h5[@class='card-title']").text
        print(f"Found package: {package_name}. Attempting to click 'Book Now'...")

        try:
            # Scroll the button into the center of the view using JavaScript
            driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", book_button)
            time.sleep(0.5) # Brief pause after scrolling to allow layout to settle

            # Wait until the button is clickable *after* scrolling
            clickable_book_button = self.wait.until(EC.element_to_be_clickable(book_button_locator))
            clickable_book_button.click()
            print("Book Now clicked successfully.")

        except ElementClickInterceptedException:
            print("Standard click failed due to interception. Trying JavaScript click...")
            try:
                # Fallback: Use JavaScript to click - use the 'book_button' element reference
                driver.execute_script("arguments[0].click();", book_button)
                print("Book Now clicked using JavaScript.")
            except Exception as js_e:
                self.fail(f"Both standard and JavaScript clicks failed for 'Book Now' button. JS Error: {js_e}")
        except Exception as e:
             self.fail(f"An unexpected error occurred when trying to click 'Book Now': {e}")

        # --- End Booking Phase ---

        # --- Cart Verification Phase ---
        # Navigate to the cart using WebDriverWait
        print("Navigating to cart...")
        cart_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='View Cart']")))
        cart_button.click()

        # Wait for cart URL
        self.wait.until(EC.url_to_be(self.base_url + "/cart"))
        self.assertEqual(driver.current_url, self.base_url + "/cart")
        print("On cart page.")

        # Check if the booked package is in the cart using WebDriverWait and specific class
        try:
            print(f"Verifying if '{package_name}' is in the cart...")
            # Use a more specific locator for the cart item title
            cart_item_title = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//h3[@class='cart-item-title' and contains(text(), '{package_name}')]")))
            self.assertIsNotNone(cart_item_title, f"{package_name} not found in cart")
            print(f"'{package_name}' found in cart.")
        except TimeoutException:
            self.fail(f"Timed out waiting for package '{package_name}' to appear in the cart.")
        except NoSuchElementException: # Should be caught by WebDriverWait, but good practice
            self.fail(f"Package '{package_name}' was not found in the cart using XPath.")
        # --- End Cart Verification Phase ---

        print("test_add_package_to_cart PASSED")


if __name__ == "__main__":
    # IMPORTANT: Ensure you have a user 'admin' with password 'admin' in your DB
    unittest.main(verbosity=2)