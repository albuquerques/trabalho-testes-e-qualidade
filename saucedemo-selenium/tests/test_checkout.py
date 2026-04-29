import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def salvar_evidencia(driver, nome):
    os.makedirs("evidencias", exist_ok=True)

    driver.save_screenshot(f"evidencias/{nome}.png")

    with open(f"evidencias/{nome}.html", "w", encoding="utf-8") as arquivo:
        arquivo.write(driver.page_source)


def preencher_campo(wait, by, value, texto):
    campo = wait.until(EC.visibility_of_element_located((by, value)))
    campo.clear()
    campo.send_keys(texto)
    return campo


def test_fluxo_completo_de_compra():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        driver.get("https://www.saucedemo.com/")

        # Login
        preencher_campo(wait, By.ID, "user-name", "standard_user")
        preencher_campo(wait, By.ID, "password", "secret_sauce")

        wait.until(
            EC.element_to_be_clickable((By.ID, "login-button"))
        ).click()

        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_list"))
        )

        # Adicionar produto ao carrinho
        wait.until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
        ).click()

        wait.until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "shopping_cart_badge"), "1")
        )

        # Abrir carrinho
        cart_button = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "shopping_cart_link"))
        )

        driver.execute_script("arguments[0].click();", cart_button)

        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "cart_list"))
        )

        wait.until(
            EC.visibility_of_element_located((By.ID, "checkout"))
        )

        produto = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "inventory_item_name"))
        ).text

        assert produto == "Sauce Labs Backpack"

        # Ir para checkout
        checkout_button = wait.until(
            EC.element_to_be_clickable((By.ID, "checkout"))
        )

        driver.execute_script("arguments[0].click();", checkout_button)

        wait.until(
            EC.visibility_of_element_located((By.ID, "first-name"))
        )

        # Preencher informações do cliente
        preencher_campo(wait, By.ID, "first-name", "Ricardo")
        preencher_campo(wait, By.ID, "last-name", "Albuquerque")
        preencher_campo(wait, By.ID, "postal-code", "64000-000")

        continue_button = wait.until(
            EC.element_to_be_clickable((By.ID, "continue"))
        )

        continue_button.click()

        # Validar resumo da compra
        try:
            wait.until(
                EC.visibility_of_element_located((By.CLASS_NAME, "summary_info"))
            )
        except Exception:
            print("URL atual:", driver.current_url)

            erros = driver.find_elements(By.CSS_SELECTOR, "[data-test='error']")
            if erros:
                print("Erro exibido na tela:", erros[0].text)

            raise

        # Finalizar compra
        finish_button = wait.until(
            EC.element_to_be_clickable((By.ID, "finish"))
        )

        driver.execute_script("arguments[0].click();", finish_button)

        mensagem = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "complete-header"))
        ).text

        assert mensagem == "Thank you for your order!"

    except Exception:
        salvar_evidencia(driver, "erro_selenium")
        print("URL no momento do erro:", driver.current_url)
        raise

    finally:
        driver.quit()
