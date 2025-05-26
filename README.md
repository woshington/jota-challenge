
# 📰 JOTA - Sistema de Publicação de Notícias

## 🛠️ Instalação e Execução

Este projeto utiliza **Docker Compose** para orquestrar os seguintes serviços:

- PostgreSQL
- RabbitMQ
- Django (App)
- Celery (Worker)
- Celery Beat (Agendador)

---


### ✅ Pré-requisitos

- [Docker](https://docs.docker.com/get-docker/) instalado
- Arquivo `.env` configurado com as variáveis necessárias (veja exemplo abaixo)

---

### ⚙️ Passos para execução

1. Configure o arquivo `.env` conforme o exemplo abaixo.
### 📄 Exemplo de `.env`

```env
SECRET_KEY=super-secret-key
DEBUG=True
DJANGO_SETTINGS_MODULE=JOTA.settings
DB_NAME=jota
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_HOST=rabbitmq_jota
```

---

2. Execute o comando:

```bash
docker compose up
```

> Este comando irá subir todos os serviços necessários: banco de dados, mensageria, aplicação, worker e agendador.

3. Após o container da aplicação estar rodando, acesse o shell dentro do container Django e crie um superusuário com o comando:

```bash
docker compose exec app python manage.py createsuperuser
```

> Este usuário admin será necessário para acessar o painel administrativo e gerenciar o sistema.

---

# 📖 Documentação da API JOTA

A **JOTA API** oferece endpoints RESTful para autenticação, gerenciamento de usuários, planos, verticais e notícias. A API utiliza autenticação JWT para segurança.

- **Base URL:** `http://127.0.0.1:8000/api/v1/`
- **Versão:** v1
- **Licença:** BSD License

---

## ✅ Funcionalidades

### Autenticação
- Registro de usuários
- Obtenção de tokens JWT (access e refresh)
- Refresh e verificação de tokens

### Usuário
- Consulta e atualização do próprio perfil

### Plano
- Listagem e consulta de planos

### Vertical
- Listagem de verticais

### Notícias
- CRUD completo
- Publicação de notícias

---

## 🚀 Endpoints Principais

### Autenticação JWT

| Método | Endpoint                 | Descrição                            |
|--------|--------------------------|------------------------------------|
| POST   | `/accounts/token/`        | Gera access e refresh tokens        |
| POST   | `/accounts/token/refresh/`| Atualiza access token               |
| POST   | `/accounts/token/verify/` | Verifica validade do token          |
| POST   | `/accounts/register/`     | Registra um novo usuário            |

---

### Usuário

| Método | Endpoint          | Descrição                        |
|--------|-------------------|--------------------------------|
| GET    | `/accounts/me/`    | Consulta dados do usuário atual |
| PUT    | `/accounts/me/`    | Atualiza dados do usuário       |
| PATCH  | `/accounts/me/`    | Atualização parcial             |

---

### Plano

| Método | Endpoint        | Descrição              |
|--------|-----------------|------------------------|
| GET    | `/core/plan/`    | Lista todos os planos  |
| GET    | `/core/plan/{id}`| Consulta plano por ID  |

---

### Vertical

| Método | Endpoint        | Descrição                |
|--------|-----------------|--------------------------|
| GET    | `/core/vertical/`| Lista todas as verticais |

---

### Notícias

| Método | Endpoint                 | Descrição                  |
|--------|--------------------------|----------------------------|
| GET    | `/news/`                 | Lista todas as notícias    |
| POST   | `/news/`                 | Cria uma notícia           |
| GET    | `/news/{id}/`            | Consulta notícia específica|
| PUT    | `/news/{id}/`            | Atualiza notícia           |
| PATCH  | `/news/{id}/`            | Atualização parcial        |
| POST   | `/news/{id}/publish/`    | Publica a notícia          |

---

## 📡 Exemplos de Requisições cURL

### Autenticação

#### Obter tokens JWT (access e refresh)

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/token/ -H "Content-Type: application/json" -d '{"username": "usuario", "password": "senha"}'
```

---

#### Atualizar access token com refresh token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/token/refresh/ -H "Content-Type: application/json" -d '{"refresh": "<refresh_token>"}'
```

---

#### Verificar validade do token

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/token/verify/ -H "Content-Type: application/json" -d '{"token": "<access_token>"}'
```

---

#### Registrar novo usuário

```bash
curl -X POST http://127.0.0.1:8000/api/v1/accounts/register/ -H "Content-Type: application/json" -d '{"username": "novo_usuario", "password": "senha123", "email": "email@exemplo.com", "plan": 1, "vertical": 1}'
```

---

### Usuário

#### Consultar perfil do usuário (requer token)

```bash
curl -X GET http://127.0.0.1:8000/api/v1/accounts/me/ -H "Authorization: Bearer <access_token>"
```

---

#### Atualizar perfil do usuário (exemplo com PATCH)

```bash
curl -X PATCH http://127.0.0.1:8000/api/v1/accounts/me/ -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"email": "novoemail@exemplo.com"}'
```

---

### Planos

#### Listar planos

```bash
curl -X GET http://127.0.0.1:8000/api/v1/core/plan/
```

---

### Verticais

#### Listar verticais

```bash
curl -X GET http://127.0.0.1:8000/api/v1/core/vertical/
```

---

### Notícias

#### Listar notícias

```bash
curl -X GET http://127.0.0.1:8000/api/v1/news/
```

---

#### Criar notícia

```bash
curl -X POST http://127.0.0.1:8000/api/v1/news/ -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"title": "Nova notícia", "content": "Conteúdo da notícia", "vertical": 1}'
```

---

#### Publicar notícia

```bash
curl -X POST http://127.0.0.1:8000/api/v1/news/{id}/publish/ -H "Authorization: Bearer <access_token>"
```

---

## 🔗 Documentação Interativa

- [Swagger UI](http://127.0.0.1:8000/swagger/)
- [Redoc](http://127.0.0.1:8000/redoc/)

---

## 🔐 Segurança

A API utiliza autenticação via **JWT Bearer Token**. Envie o token no header da requisição:

```
Authorization: Bearer <access_token>
```

---

## 🛠️ Tecnologias Utilizadas

- Python 3.x  
- Django & Django REST Framework  
- PostgreSQL  
- RabbitMQ  
- Celery & Celery Beat  
- Docker & Docker Compose  

---

## 📩 Contato

Em caso de dúvidas ou sugestões:

- Email: [woshingtonvaldeci@gmail.com](mailto:woshingtonvaldeci@gmail.com)

---

## 📝 Licença

BSD License
