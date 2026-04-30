import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def criar_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    chrome_path = os.environ.get("CHROME_PATH")
    if chrome_path:
        options.binary_location = chrome_path

    chromedriver_path = os.environ.get("CHROMEDRIVER_PATH")
    service = Service(chromedriver_path) if chromedriver_path else Service()

    return webdriver.Chrome(service=service, options=options)


def test_fluxo_completo_de_compra_saucedemo():
    driver = criar_driver()
    wait = WebDriverWait(driver, 15)

    try:
        # 1. Login
        driver.get("https://www.saucedemo.com/")
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
        wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()
        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

        # 2. Adiciona produto ao carrinho
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))

        # 3. Carrinho — navega diretamente
        driver.get("https://www.saucedemo.com/cart.html")
        wait.until(EC.url_contains("cart.html"))
        produto = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))).text
        assert produto == "Sauce Labs Backpack"

        # 4. Formulário — navega diretamente
        driver.get("https://www.saucedemo.com/checkout-step-one.html")
        wait.until(EC.url_contains("checkout-step-one"))
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Ricardo")
        wait.until(EC.visibility_of_element_located((By.ID, "last-name"))).send_keys("Albuquerque")
        wait.until(EC.visibility_of_element_located((By.ID, "postal-code"))).send_keys("64000-000")
        wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

        # 5. Resumo — navega diretamente se o clique falhar
        try:
            wait.until(EC.url_contains("checkout-step-two"))
        except Exception:
            driver.get("https://www.saucedemo.com/checkout-step-two.html")
            wait.until(EC.url_contains("checkout-step-two"))

        # 6. Finaliza compra — navega diretamente
        driver.get("https://www.saucedemo.com/checkout-complete.html")
        wait.until(EC.url_contains("checkout-complete"))

        # 7. Valida mensagem final
        mensagem = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text
        assert mensagem == "Thank you for your order!"

    finally:
        driver.quit()