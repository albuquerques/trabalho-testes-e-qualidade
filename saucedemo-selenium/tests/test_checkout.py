from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def test_fluxo_completo_de_compra():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        # 1. Acessar o site
        driver.get("https://www.saucedemo.com/")

        # 2. Fazer login
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()

        # 3. Validar se entrou na página de produtos
        assert "inventory" in driver.current_url

        # 4. Adicionar produto ao carrinho
        driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()

        # 5. Abrir carrinho
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()

        # 6. Validar se o produto está no carrinho
        produto = driver.find_element(By.CLASS_NAME, "inventory_item_name").text
        assert produto == "Sauce Labs Backpack"

        # 7. Ir para checkout
        driver.find_element(By.ID, "checkout").click()

        # 8. Preencher dados do cliente
        driver.find_element(By.ID, "first-name").send_keys("Ricardo")
        driver.find_element(By.ID, "last-name").send_keys("Albuquerque")
        driver.find_element(By.ID, "postal-code").send_keys("64000-000")

        driver.find_element(By.ID, "continue").click()

        # 9. Validar resumo da compra
        assert "checkout-step-two" in driver.current_url
        assert "Sauce Labs Backpack" in driver.page_source

        # 10. Finalizar compra
        driver.find_element(By.ID, "finish").click()

        # 11. Validar mensagem final
        mensagem = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert mensagem == "Thank you for your order!"

    finally:
        time.sleep(2)
        driver.quit()
