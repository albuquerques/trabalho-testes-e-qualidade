# 🧪 Desafio Técnico — Automação de Testes

Repositório com a entrega do desafio técnico de automação de testes, cobrindo dois projetos independentes: automação de **API REST** e automação **Web E2E**. Cada projeto possui seu próprio diretório, dependências e documentação.

---

## 📁 Estrutura do Repositório

```
/
├── saucedemo-selenium/        # Automação Web E2E (Selenium + Python)
│   └── README.md              # Instruções detalhadas do projeto
│
└── swagger-petstore-tests/    # Automação de API REST (Postman + Newman)
    └── README.md              # Instruções detalhadas do projeto
```

---

## 🗂️ Projetos

### 🌐 Automação Web — SauceDemo

Testes end-to-end para o site [SauceDemo](https://www.saucedemo.com), simulando o fluxo completo de compra de um usuário real.

| | |
|---|---|
| **Ferramenta** | Selenium WebDriver + pytest |
| **Linguagem** | Python 3.12 |
| **Escopo** | Login → Carrinho → Checkout → Confirmação |
| **CI/CD** | GitHub Actions |

📄 [Ver documentação completa →](./saucedemo-selenium/README.md)

---

### 🔌 Automação de API — Swagger Petstore

Testes automatizados para a API pública [Swagger Petstore](https://petstore.swagger.io), cobrindo os módulos de Pet, Store e User.

| | |
|---|---|
| **Ferramenta** | Postman + Newman |
| **Linguagem** | JavaScript (scripts Postman) |
| **Escopo** | Endpoints de Pet, Store e User (23 requests) |
| **CI/CD** | GitHub Actions |

📄 [Ver documentação completa →](./swagger-petstore-tests/README.md)

---

## ⚙️ CI/CD

Ambos os projetos possuem pipelines independentes configuradas no **GitHub Actions**, disparadas automaticamente a cada `push` ou `pull request` na branch `main`.

| Projeto | Workflow |
|---------|----------|
| SauceDemo (Web) | `.github/workflows/ci.yml` |
| Swagger Petstore (API) | `.github/workflows/api-tests.yml` |

Para acompanhar as execuções, acesse a aba **Actions** no repositório.

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Finalidade |
|------------|------------|
| Python 3.12 | Linguagem base dos testes web |
| Selenium WebDriver | Automação do navegador |
| pytest | Framework de testes web |
| Postman / Newman | Criação e execução dos testes de API |
| GitHub Actions | Integração e entrega contínua |

---

## 📖 Documentação por Projeto

Cada projeto contém um `README.md` próprio com instruções detalhadas de instalação, configuração e execução. Consulte-os para mais informações:

- [SauceDemo — Testes E2E com Selenium](./saucedemo-selenium/README.md)
- [Swagger Petstore — Testes de API](./swagger-petstore-tests/README.md)
