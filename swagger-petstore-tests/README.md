# 🐾 Swagger Petstore — Testes de API

![CI](https://github.com/albuquerques/trabalho-testes-e-qualidade/actions/workflows/api-tests.yml/badge.svg)

Suíte de testes automatizados para a API pública [Swagger Petstore](https://petstore.swagger.io), cobrindo os módulos de **Pet**, **Store** e **User**. Os testes são executados via **Postman/Newman** e integrados ao **GitHub Actions** para rodar automaticamente a cada push ou pull request.

---

## 📁 Estrutura do Projeto

```
trabalho-testes-e-qualidade/
├── .github/
│   └── workflows/
│       └── api-tests.yml        # Pipeline de CI/CD (raiz do repositório)
└── swagger-petstore-tests/
    └── postman/
        ├── collection.json      # Coleção com todos os testes
        └── environment.json     # Variáveis de ambiente
```

---

## ✅ Cobertura de Testes

### 👤 User (10 requests)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/user` | Cria um usuário com dados dinâmicos |
| GET | `/user/{username}` | Busca o usuário criado |
| PUT | `/user/{username}` | Atualiza dados do usuário |
| GET | `/user/{username}` | Valida que a atualização foi aplicada |
| GET | `/user/login` | Realiza login e valida a resposta |
| GET | `/user/logout` | Realiza logout |
| POST | `/user/createWithArray` | Cria múltiplos usuários via array |
| POST | `/user/createWithList` | Cria múltiplos usuários via lista |
| DELETE | `/user/{username}` | Remove o usuário |
| GET | `/user/{username}` | Valida que o usuário foi deletado (404) |

### 🐶 Pet (8 requests)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/pet` | Cria um pet e salva o ID no ambiente |
| GET | `/pet/{petId}` | Busca o pet pelo ID |
| PUT | `/pet` | Atualiza nome e status do pet |
| GET | `/pet/{petId}` | Valida que a atualização foi aplicada |
| GET | `/pet/findByStatus` | Lista pets por status (`sold`) |
| POST | `/pet/{petId}` | Atualiza pet via form data |
| DELETE | `/pet/{petId}` | Remove o pet |
| GET | `/pet/{petId}` | Valida que o pet foi deletado (404) |

### 🏪 Store (5 requests)

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/store/inventory` | Consulta o inventário da loja |
| POST | `/store/order` | Cria um pedido e salva o ID |
| GET | `/store/order/{orderId}` | Busca o pedido pelo ID |
| DELETE | `/store/order/{orderId}` | Remove o pedido |
| GET | `/store/order/{orderId}` | Valida que o pedido foi deletado (404) |

**Total: 23 requests / ~85 asserções**

---

## 🔧 Variáveis de Ambiente

O arquivo `postman/environment.json` define as seguintes variáveis:

| Variável | Descrição | Valor padrão |
|----------|-----------|-------------|
| `base_url` | URL base da API | `https://petstore.swagger.io/v2` |
| `pet_id` | ID do pet criado (preenchido em runtime) | — |
| `pet_name` | Nome do pet criado (preenchido em runtime) | — |
| `order_id` | ID do pedido criado (preenchido em runtime) | — |
| `username` | Username do usuário criado (preenchido em runtime) | — |
| `user_id` | ID do usuário criado (preenchido em runtime) | — |
| `password` | Senha padrão usada nos testes | `123456` |

> As variáveis preenchidas em runtime são salvas via `pm.environment.set()` durante a execução dos testes e reutilizadas nas requisições seguintes.

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- [Node.js](https://nodejs.org/) v20 ou superior
- [Newman](https://www.npmjs.com/package/newman) (CLI do Postman)
- _(Opcional)_ [newman-reporter-htmlextra](https://www.npmjs.com/package/newman-reporter-htmlextra) para relatórios HTML

### Instalação do Newman

```bash
npm install -g newman
```

### Executando os testes

```bash
newman run postman/collection.json -e postman/environment.json
```

### Executando com relatório HTML (opcional)

```bash
npm install -g newman-reporter-htmlextra

newman run postman/collection.json \
  -e postman/environment.json \
  -r htmlextra \
  --reporter-htmlextra-export results/report.html
```

---

## ⚙️ CI/CD com GitHub Actions

O pipeline está configurado no arquivo `.github/workflows/api-tests.yml` na **raiz do repositório** e é disparado nos seguintes eventos:

- **Push** na branch `main`
- **Pull Request** com destino à branch `main`
- **Execução manual** via `workflow_dispatch`

### Pipeline

```
Checkout → Instalar Node.js 20 → Instalar Newman → Rodar testes
```

### Configuração (`api-tests.yml`)

```yaml
name: API Tests

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

jobs:
  test:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: swagger-petstore-tests
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g newman
      - run: newman run postman/collection.json -e postman/environment.json
```

Para visualizar os resultados, acesse a aba **Actions** no repositório do GitHub.

---

## 🧪 Estratégia de Testes

Os testes seguem um **fluxo encadeado**: o resultado de uma requisição alimenta as seguintes por meio de variáveis de ambiente, simulando um cenário real de uso da API.

- **Criação → Leitura → Atualização → Validação → Exclusão → Validação**
- Dados dinâmicos gerados com `{{$randomInt}}` e `{{$timestamp}}` evitam conflitos entre execuções
- Cada request valida o **status HTTP** e, quando aplicável, **campos específicos do corpo da resposta**

---

## 🌐 Sobre a API

A [Swagger Petstore](https://petstore.swagger.io) é uma API pública de demonstração mantida pela Swagger/OpenAPI. Por ser um ambiente compartilhado, dados criados por outros usuários podem interferir em buscas por status — isso é esperado e não representa falha nos testes.

- Documentação: https://petstore.swagger.io
- Especificação OpenAPI: https://petstore.swagger.io/v2/swagger.json
