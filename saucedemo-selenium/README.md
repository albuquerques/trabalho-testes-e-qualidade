# saucedemo-selenium

Projeto de testes automatizados end-to-end para o site [SauceDemo](https://www.saucedemo.com), desenvolvido com **Selenium WebDriver** e **pytest**.

O teste cobre o fluxo completo de compra: login → adição de produto ao carrinho → checkout → confirmação do pedido.

---

## Pré-requisitos

- Python 3.12+
- Google Chrome instalado
- ChromeDriver compatível com a versão do Chrome (gerenciado automaticamente pelo Selenium 4+)

---

## Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seu-usuario/saucedemo-selenium.git
cd saucedemo-selenium
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Como executar

```bash
pytest
```

Para rodar com saída detalhada:

```bash
pytest -v
```

Para rodar em modo headless (sem abrir o navegador):

O modo headless já está ativado por padrão no teste. Para desativá-lo durante o desenvolvimento, remova ou comente a linha `options.add_argument("--headless")` no arquivo `tests/test_checkout.py`.

---

## Estrutura do projeto

```
saucedemo-selenium/
├── tests/
│   └── test_checkout.py       # Teste principal do fluxo de compra
├── .github/
│   └── workflows/
│       └── ci.yml             # Pipeline de CI com GitHub Actions
├── requirements.txt           # Dependências do projeto
└── README.md
```

---

## Cenário de teste

O arquivo `tests/test_checkout.py` cobre o seguinte fluxo:

1. Acessa `https://www.saucedemo.com`
2. Realiza login com o usuário `standard_user`
3. Valida o redirecionamento para a página de produtos
4. Adiciona o produto *Sauce Labs Backpack* ao carrinho
5. Abre o carrinho e valida se o produto está presente
6. Inicia o checkout e preenche os dados do cliente
7. Valida o resumo da compra
8. Finaliza o pedido e valida a mensagem de confirmação

---

## CI/CD

O projeto utiliza **GitHub Actions** para rodar os testes automaticamente a cada `push` ou `pull request` na branch `main`.

O workflow instala o Chrome, configura o Python 3.12, instala as dependências e executa o pytest. Veja a configuração completa em `.github/workflows/ci.yml`.

---

## Dependências

| Pacote | Versão mínima | Descrição |
|--------|---------------|-----------|
| selenium | 4.0.0 | Automação do navegador |
| pytest | 9.0.0 | Framework de testes |

---

## Credenciais de teste

O SauceDemo é um site público criado para fins de automação de testes. As credenciais usadas no projeto são oficialmente disponibilizadas pelo próprio site:

| Usuário | Senha |
|---------|-------|
| `standard_user` | `secret_sauce` |

Outros usuários disponíveis no site incluem `locked_out_user`, `problem_user` e `performance_glitch_user`, úteis para expandir a cobertura de testes.

---

## Licença

Este projeto é de uso livre para fins educacionais e de estudo.
