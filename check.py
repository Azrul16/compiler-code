# import requests
# import time
# import random

# # Function to simulate views on a Reel
# def simulate_views(reel_link, num_requests=10):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

#     for _ in range(num_requests):
#         try:
#             response = requests.get(reel_link, headers=headers)
#             if response.status_code == 200:
#                 print(f"Successfully simulated a view. Status code: {response.status_code}")
#             else:
#                 print(f"Failed to simulate a view. Status code: {response.status_code}")
#         except Exception as e:
#             print(f"Error simulating a view: {e}")
#         time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

# # Main function to take a Reel link as input and simulate views
# def main():
#     reel_link = "https://www.instagram.com/p/DP6rYLAkQM0/"
#     simulate_views(reel_link)

# if __name__ == "__main__":
#     main()


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import random

# Function to simulate views on a Reel
def simulate_views(reel_link, num_requests=10):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    for _ in range(num_requests):
        try:
            # Open the Reel link
            driver.get(reel_link)
            time.sleep(5)  # Wait for the page to load

            # Handle pop-ups (example: closing a cookie consent pop-up)
            try:
                close_button = driver.find_element(By.XPATH, '//button[contains(text(), "Close")]')
                close_button.click()
            except:
                pass

            # Simulate scrolling to trigger more views
            for _ in range(100):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(1, 3))  # Random delay between 1 and 3 seconds

            # Keep the browser open for a while to simulate longer view time
            time.sleep(random.uniform(5, 15))  # Random delay between 5 and 15 seconds

        except Exception as e:
            print(f"Error simulating a view: {e}")
        finally:
            driver.quit()
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

# Main function to take a Reel link as input and simulate views
def main():
    reel_link = "https://www.instagram.com/p/DP6rYLAkQM0/"
    simulate_views(reel_link)

if __name__ == "__main__":
    main()