# 🛒 SauceDemo — Testes de UI com Selenium

Suíte de testes automatizados para o site de e-commerce de demonstração [SauceDemo](https://www.saucedemo.com), cobrindo o **fluxo completo de compra**. Os testes são executados via **Pytest + Selenium** com Chrome headless, prontos para integração em pipelines de CI/CD com **GitHub Actions**.

---

## 📁 Estrutura do Projeto

```
saucedemo-selenium/
├── tests/
│   └── test_checkout.py    # Teste do fluxo completo de compra
└── requirements.txt        # Dependências do projeto
```

---

## ✅ Cobertura de Testes

### 🛍️ Fluxo Completo de Compra (1 teste / ~7 asserções)

| Etapa | Ação | Validação |
|-------|------|-----------|
| Login | Preenche usuário e senha e clica em entrar | URL contém `inventory` |
| Carrinho | Adiciona "Sauce Labs Backpack" ao carrinho | Badge do carrinho exibe `1` |
| Carrinho | Navega para o carrinho | Produto presente (`"Sauce Labs Backpack"`) |
| Checkout — Dados | Preenche nome, sobrenome e CEP e clica em continuar | — |
| Checkout — Resumo | Aguarda página de revisão do pedido | URL contém `checkout-step-two` |
| Checkout — Confirmação | Finaliza a compra | — |
| Confirmação | Valida mensagem de sucesso | Texto `"Thank you for your order!"` |

**Total: 1 teste / ~7 asserções**

---

## 🔧 Dependências

O arquivo `requirements.txt` define as seguintes dependências:

| Pacote | Versão | Descrição |
|--------|--------|-----------| 
| `selenium` | 4.21.0 | Automação de navegador web |
| `pytest` | 8.2.2 | Framework de execução de testes |

> O ChromeDriver é gerenciado automaticamente pelo Selenium Manager a partir da versão 4.6+, sem necessidade de instalação manual em ambiente local.

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- [Python](https://www.python.org/) 3.8 ou superior
- [Google Chrome](https://www.google.com/chrome/) instalado

### Instalação das dependências

```bash
pip install -r requirements.txt
```

### Executando os testes

```bash
pytest -v
```

### Executando com relatório HTML (opcional)

```bash
pip install pytest-html

pytest -v --html=results/report.html --self-contained-html
```

---

## ⚙️ CI/CD com GitHub Actions

O pipeline está configurado no arquivo `.github/workflows/ci-web.yml`:

```yaml
name: Testes Web - SauceDemo

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  selenium-tests:
    runs-on: ubuntu-latest

    defaults:
      run:
        working-directory: saucedemo-selenium

    steps:
      - name: Baixar código do repositório
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar Google Chrome e ChromeDriver pareados
        uses: browser-actions/setup-chrome@v2
        id: setup-chrome
        with:
          chrome-version: "147"
          install-chromedriver: true

      - name: Exportar caminhos do Chrome e ChromeDriver
        run: |
          echo "CHROME_PATH=${{ steps.setup-chrome.outputs.chrome-path }}" >> $GITHUB_ENV
          echo "CHROMEDRIVER_PATH=${{ steps.setup-chrome.outputs.chromedriver-path }}" >> $GITHUB_ENV

      - name: Verificar versões
        run: |
          ${{ steps.setup-chrome.outputs.chrome-path }} --version
          ${{ steps.setup-chrome.outputs.chromedriver-path }} --version

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Executar testes Selenium
        run: pytest -v
```

### Pipeline

```
Checkout → Configurar Python → Instalar Chrome + ChromeDriver → Exportar caminhos → Verificar versões → Instalar dependências → Rodar testes
```

> O Chrome e o ChromeDriver são instalados na versão **147** via `browser-actions/setup-chrome@v2`, garantindo compatibilidade entre os dois. Os caminhos são exportados como variáveis de ambiente (`CHROME_PATH` e `CHROMEDRIVER_PATH`) e lidos automaticamente pelo código do teste.

Para visualizar os resultados, acesse a aba **Actions** no repositório do GitHub.

---

## 🧪 Estratégia de Testes

O teste segue um **fluxo de ponta a ponta** que simula um usuário real realizando uma compra completa no SauceDemo:

- **Login → Catálogo → Adicionar ao carrinho → Checkout → Confirmação**
- O Chrome é iniciado em modo **headless** (`--headless=new`), garantindo compatibilidade com ambientes de CI sem interface gráfica
- O `WebDriverWait` é utilizado em todas as interações para aguardar elementos dinamicamente, tornando os testes resilientes a variações de carregamento
- Em etapas críticas, o teste navega diretamente para a URL caso o clique não acione a transição esperada, evitando falhas intermitentes de CI
- O bloco `finally` garante que o driver seja encerrado corretamente mesmo em caso de falha

---

## 🌐 Sobre a Aplicação

O [SauceDemo](https://www.saucedemo.com) é um e-commerce de demonstração mantido pela Sauce Labs, amplamente utilizado para prática de automação de testes. A aplicação oferece diferentes tipos de usuário para simular cenários variados.

| Usuário | Comportamento |
|---------|--------------|
| `standard_user` | Fluxo normal de compra |
| `locked_out_user` | Bloqueado no login |
| `problem_user` | Imagens com defeito |
| `performance_glitch_user` | Lentidão simulada |

> Senha padrão para todos os usuários: `secret_sauce`

- Site: https://www.saucedemo.com
- Documentação Sauce Labs: https://docs.saucelabs.com
