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
    wait = WebDriverWait(driver, 15)

    try:
        driver.get("https://www.saucedemo.com/")

        # Login
        wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys("standard_user")
        wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("secret_sauce")
        wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

        # Valida que entrou na página de produtos
        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url

        # Adiciona produto ao carrinho
        wait.until(EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))).click()

        # Aguarda o badge confirmar que o item foi adicionado
        wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1"))

        # Navega diretamente para o carrinho (mais confiável que clicar no ícone em headless)
        driver.get("https://www.saucedemo.com/cart.html")
        wait.until(EC.url_contains("cart"))

        # Valida produto no carrinho
        produto = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text

        assert produto == "Sauce Labs Backpack"

        # Checkout
        wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

        # Preenche formulário
        wait.until(EC.visibility_of_element_located((By.ID, "first-name"))).send_keys("Ricardo")
        wait.until(EC.visibility_of_element_located((By.ID, "last-name"))).send_keys("Albuquerque")
        wait.until(EC.visibility_of_element_located((By.ID, "postal-code"))).send_keys("64000-000")
        wait.until(EC.element_to_be_clickable((By.ID, "continue"))).click()

        # Finaliza compra
        wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()

        # Valida mensagem final
        mensagem = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert mensagem == "Thank you for your order!"

    finally:
        driver.quit()