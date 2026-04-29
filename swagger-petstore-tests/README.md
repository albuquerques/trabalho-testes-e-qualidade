# 🛒 SauceDemo — Testes E2E com Selenium

Suíte de testes automatizados end-to-end para o site público [SauceDemo](https://www.saucedemo.com), cobrindo o fluxo completo de compra. Os testes são executados via **pytest + Selenium WebDriver** e integrados ao **GitHub Actions** para rodar automaticamente a cada push ou pull request.

---

## 📁 Estrutura do Projeto

```
saucedemo-selenium/
├── tests/
│   └── test_checkout.py       # Teste principal do fluxo de compra
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de CI/CD
├── requirements.txt           # Dependências do projeto
└── README.md
```

---

## ✅ Cobertura de Testes

### 🛍️ Fluxo de Compra (1 teste / 7 asserções)

| Etapa | Ação | Validação |
|-------|------|-----------|
| Login | Autentica com `standard_user` | URL contém `inventory` |
| Carrinho | Adiciona *Sauce Labs Backpack* | Nome do produto no carrinho |
| Checkout | Preenche nome, sobrenome e CEP | — |
| Resumo | Avança para a etapa de revisão | URL contém `checkout-step-two` e produto listado |
| Confirmação | Finaliza o pedido | Mensagem `"Thank you for your order!"` |

**Total: 1 teste / 7 asserções**

---

## 🔧 Pré-requisitos

- Python 3.12+
- Google Chrome instalado
- ChromeDriver compatível (gerenciado automaticamente pelo Selenium 4+)

---

## 🚀 Como Executar Localmente

### Instalação

```bash
git clone https://github.com/seu-usuario/saucedemo-selenium.git
cd saucedemo-selenium
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Executando os testes

```bash
pytest
```

### Executando com saída detalhada

```bash
pytest -v
```

> O modo headless já está ativado por padrão. Para desativá-lo durante o desenvolvimento, remova ou comente a linha `options.add_argument("--headless")` em `tests/test_checkout.py`.

---

## ⚙️ CI/CD com GitHub Actions

Os testes são executados automaticamente pelo workflow `.github/workflows/ci.yml` nos seguintes eventos:

- **Push** na branch `main`
- **Pull Request** com destino à branch `main`

### Pipeline

```
Checkout → Configurar Python 3.12 → Instalar Chrome → Instalar dependências → Rodar testes
```

Para visualizar os resultados, acesse a aba **Actions** no repositório do GitHub.

---

## 🧪 Estratégia de Testes

O teste segue um **fluxo encadeado e linear**, simulando um usuário real navegando pela loja do início ao fim:

- **Login → Navegação → Adição ao carrinho → Checkout → Confirmação**
- Cada etapa valida o **estado da página** antes de prosseguir (URL, texto e presença de elementos)
- O navegador é encerrado via `finally`, garantindo limpeza mesmo em caso de falha

---

## 🔐 Credenciais de Teste

O SauceDemo é um site público criado para fins de automação. As credenciais abaixo são disponibilizadas oficialmente pelo próprio site:

| Usuário | Senha | Comportamento |
|---------|-------|---------------|
| `standard_user` | `secret_sauce` | Fluxo normal ✅ |
| `locked_out_user` | `secret_sauce` | Login bloqueado 🔒 |
| `problem_user` | `secret_sauce` | Elementos com defeito ⚠️ |
| `performance_glitch_user` | `secret_sauce` | Respostas lentas 🐢 |

> Os demais usuários são úteis para expandir a cobertura de testes com cenários negativos e de degradação.

---

## 📦 Dependências

| Pacote | Versão mínima | Descrição |
|--------|---------------|-----------|
| `selenium` | 4.0.0 | Automação do navegador |
| `pytest` | 9.0.0 | Framework de testes |

---

## 🌐 Sobre o SauceDemo

O [SauceDemo](https://www.saucedemo.com) é uma aplicação de e-commerce fictícia mantida pela Sauce Labs, criada especificamente para prática de automação de testes. Por ser um ambiente público e compartilhado, o estado da aplicação pode variar entre sessões — isso é esperado e não representa falha nos testes.

- Site: https://www.saucedemo.com
