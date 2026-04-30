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

### 🛍️ Fluxo Completo de Compra (1 teste / ~6 asserções)

| Etapa | Ação | Validação |
|-------|------|-----------|
| Login | Preenche usuário e senha e clica em entrar | URL contém `inventory` |
| Catálogo | Página de produtos carregada | — |
| Carrinho | Adiciona "Sauce Labs Backpack" ao carrinho | Produto presente no carrinho |
| Checkout | Preenche nome, sobrenome e CEP | — |
| Confirmação | Finaliza a compra | Mensagem `"Thank you for your order!"` |

**Total: 1 teste / ~6 asserções**

---

## 🔧 Dependências

O arquivo `requirements.txt` define as seguintes dependências:

| Pacote | Versão | Descrição |
|--------|--------|-----------|
| `selenium` | 4.21.0 | Automação de navegador web |
| `pytest` | 8.2.2 | Framework de execução de testes |

> O ChromeDriver é gerenciado automaticamente pelo Selenium Manager a partir da versão 4.6+, sem necessidade de instalação manual.

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
pytest tests/test_checkout.py -v
```

### Executando com relatório HTML (opcional)

```bash
pip install pytest-html

pytest tests/test_checkout.py -v --html=results/report.html --self-contained-html
```

---

## ⚙️ CI/CD com GitHub Actions

Para integrar ao GitHub Actions, crie o arquivo `.github/workflows/ui-tests.yml`:

```yaml
name: UI Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Instalar dependências
        run: pip install -r requirements.txt

      - name: Instalar Google Chrome
        uses: browser-actions/setup-chrome@v1

      - name: Rodar testes
        run: pytest tests/ -v
```

### Pipeline

```
Checkout → Configurar Python → Instalar dependências → Instalar Chrome → Rodar testes
```

Para visualizar os resultados, acesse a aba **Actions** no repositório do GitHub.

---

## 🧪 Estratégia de Testes

O teste segue um **fluxo de ponta a ponta** que simula um usuário real realizando uma compra completa no SauceDemo:

- **Login → Catálogo → Adicionar ao carrinho → Checkout → Confirmação**
- O Chrome é iniciado em modo **headless** (`--headless=new`), garantindo compatibilidade com ambientes de CI sem interface gráfica
- O `WebDriverWait` é utilizado em todas as interações para aguardar elementos dinamicamente, tornando os testes resilientes a variações de carregamento
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
