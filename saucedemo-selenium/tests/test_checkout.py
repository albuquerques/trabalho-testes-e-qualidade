from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_fluxo_completo_de_compra():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.saucedemo.com/")

        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        wait.until(EC.url_contains("inventory"))

        wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        ).click()

        wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        ).click()

        wait.until(EC.url_contains("cart"))

        produto = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text

        assert produto == "Sauce Labs Backpack"

        checkout_button = wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )

        driver.execute_script("arguments[0].click();", checkout_button)

        wait.until(EC.url_contains("checkout-step-one"))

        wait.until(
            EC.visibility_of_element_located((By.ID, "first-name"))
        ).send_keys("Ricardo")

        driver.find_element(By.ID, "last-name").send_keys("Albuquerque")
        driver.find_element(By.ID, "postal-code").send_keys("64000-000")

        wait.until(
            EC.element_to_be_clickable((By.ID, "continue"))
        ).click()

        wait.until(EC.url_contains("checkout-step-two"))

        wait.until(
            EC.element_to_be_clickable((By.ID, "finish"))
        ).click()

        mensagem = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert mensagem == "Thank you for your order!"

    finally:
        driver.quit()
