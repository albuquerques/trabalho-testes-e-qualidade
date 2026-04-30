from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def criar_driver():
    options = Options()

    # Necessário para rodar no GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")

    return webdriver.Chrome(options=options)


def test_fluxo_completo_de_compra_saucedemo():
    driver = criar_driver()
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://www.saucedemo.com/")

        # Login
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # Valida que entrou na página de produtos
        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

        # Adiciona produto ao carrinho
        wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        ).click()

        # Acessa o carrinho
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # Valida produto no carrinho
        produto = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text

        assert produto == "Sauce Labs Backpack"

        # Checkout
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Ricardo")
        driver.find_element(By.ID, "last-name").send_keys("Albuquerque")
        driver.find_element(By.ID, "postal-code").send_keys("64000-000")

        driver.find_element(By.ID, "continue").click()

        # Finaliza compra
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

        # Valida mensagem final
        mensagem = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert mensagem == "Thank you for your order!"

    finally:
        driver.quit()
