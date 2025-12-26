from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

PNR = "4430098831"
URL = f"https://www.railyatri.in/pnr-status/{PNR}"

def get_current_status():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    wait = WebDriverWait(driver, 20)
    driver.get(URL)

    try:
        wait.until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "pnr-search-result-title")
            )
        )

        status_blocks = driver.find_elements(
            By.CSS_SELECTOR, "#status .statusType"
        )

        booking_status = status_blocks[0].text
        current_status = status_blocks[1].text

        return booking_status, current_status

    finally:
        driver.quit()


# Run standalone (optional)
if __name__ == "__main__":
    booking, current = get_current_status()
    print("Booking Status :", booking)
    print("Current Status :", current)
