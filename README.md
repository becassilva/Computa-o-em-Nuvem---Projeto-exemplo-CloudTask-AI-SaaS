<!-- Área do Banner -->
<div align="center" style="background-color: white; max-width: 70%;">
  <img alt="BANNER do repositório CloudTask AI SaaS — disciplina Computação em Nuvem" title="Banner_CloudTask_AI_SaaS" src=".readme_docs/Banner_Github_NCPU.png" width="100%" />
</div>

<!-- Título e breve descrição do repositório -->
<div align="center">
  <h1>CloudTask AI SaaS — Aula 3</h1>
  <p><b>Branch <code>semana-02-rds-vpc-seguranca</code> — estado pós Aula 3.</b></p>
  <p>API FastAPI + <b>PostgreSQL</b> + CRUD de tarefas, em Docker Compose e devcontainer.</p>
</div>

<p align="center">
  <a href="https://www.python.org/" title="Python"><img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" height="21px"></a>
  +
  <a href="https://fastapi.tiangolo.com/" title="FastAPI"><img src="https://github.com/get-icon/geticon/raw/master/icons/fastapi.svg" alt="FastAPI" height="21px"></a>
  +
  <a href="https://www.docker.com/" title="Docker"><img src="https://github.com/get-icon/geticon/raw/master/icons/docker-icon.svg" alt="Docker" height="21px"></a>
  +
  <a href="https://www.postgresql.org/" title="PostgreSQL"><img src="https://github.com/get-icon/geticon/raw/master/icons/postgresql.svg" alt="PostgreSQL" height="21px"></a>
  +
  <a href="https://www.sqlalchemy.org/" title="SQLAlchemy">SQLAlchemy</a>
</p>

## O que foi entregue nesta aula

- Serviço **`db` (PostgreSQL 16-alpine)** no `docker-compose.yml` — mesma engine do Amazon RDS, com healthcheck e `depends_on`.
- Camada de dados em `app/db/`:
  - `database.py` — engine, `SessionLocal`, `Base`, dependência `get_db`.
  - `models.py` — modelo `Task` + enums `TaskStatus` / `TaskPriority`.
  - `schemas.py` — `TaskCreate`, `TaskUpdate`, `TaskRead` (Pydantic, com exemplos no Swagger).
- `app/api/routes_tasks.py` — **CRUD completo** de tarefas.
- Criação automática das tabelas no startup (via `lifespan`).
- Versão da API: **`0.2.0`** (início da Semana 2).

> Tudo com **comentários didáticos** explicando motivo, impacto e risco de cada decisão.

## Endpoints

| Método | Caminho            | Descrição                              |
| ------ | ------------------ | -------------------------------------- |
| GET    | `/`                | Metadados da aplicação.                |
| GET    | `/health`          | Liveness probe.                        |
| POST   | `/tasks`           | Criar tarefa (201).                    |
| GET    | `/tasks`           | Listar tarefas (paginação `skip`/`limit`). |
| GET    | `/tasks/{task_id}` | Obter tarefa por id (404 se não existe). |
| PUT    | `/tasks/{task_id}` | Atualizar tarefa (parcial).            |
| DELETE | `/tasks/{task_id}` | Remover tarefa (204).                  |
| GET    | `/docs`            | Swagger UI.                            |

### Modelo `Task`

```text
id           int        (gerado pelo banco)
title        str        (obrigatório, 1–200 chars)
description  str | null  (até 2000 chars)
status       enum        pending | in_progress | done   (default pending)
priority     enum        low | medium | high            (default medium)
created_at   datetime    (carimbado pelo banco)
updated_at   datetime    (atualizado pelo banco a cada PUT)
```

## Pré-requisitos

| Ferramenta              | Versão mínima | Para quê                       |
| ----------------------- | ------------- | ------------------------------ |
| Docker Desktop          | 4.30          | API + PostgreSQL em containers |
| VS Code + Dev Containers| 1.90 / 0.380  | Abrir o projeto no container   |

> Nunca usou terminal/Docker? Veja [`docs/aws-academy-setup.md`](docs/aws-academy-setup.md).

## Como rodar

### 1) Devcontainer no VS Code (recomendado)

```text
1. F1 → "Dev Containers: Rebuild and Reopen in Container".
   (Rebuild porque o compose agora tem o serviço `db`.)
2. O VS Code sobe API + PostgreSQL juntos.
3. Terminal integrado:  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
4. Abra http://localhost:8000/docs
```

### 2) Docker Compose direto

```bash
docker compose up --build           # sobe API + PostgreSQL
curl http://localhost:8000/tasks    # deve responder []
docker compose down                 # para (mantém os dados)
docker compose down -v              # para e ZERA o banco
```

> ⚠️ Se a porta **5432** já estiver ocupada na sua máquina, defina
> `POSTGRES_PORT=5433` (ou outra livre) no seu `.env` antes de subir.

### Testando o CRUD pelo terminal

```bash
# criar
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Minha primeira tarefa","priority":"high"}'

# listar
curl http://localhost:8000/tasks

# atualizar (id 1)
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" -d '{"status":"done"}'

# remover (id 1)
curl -X DELETE http://localhost:8000/tasks/1
```

## Conexão com o banco

`DATABASE_URL` (lida do ambiente; default no compose):

```text
postgresql+psycopg2://cloudtask:cloudtask@db:5432/cloudtask
```

O host `db` é o nome do serviço no Compose. Esta **mesma URL** servirá para o
Amazon RDS na nuvem — só muda o host/usuário/senha (via Secret). Por isso
usamos PostgreSQL 16 local, igual ao RDS.

## O que vem na próxima aula

- **Aula 4 (mesma branch):** `app/core/config.py` (`.env` via pydantic-settings),
  `GET /health/ready` (checa o PostgreSQL), **HTTPS** (FORCE_HTTPS, proxy-headers,
  HSTS, mkcert local) e docs de VPC/IAM/segurança. Ver [issue #4](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/4).

## Referências

- Issue da aula: [#3 — Aula 3](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/3)
- Lista de tarefas: [`docs/TAREFAS.md`](docs/TAREFAS.md)
- Guia geral: [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md)
- Setup do zero: [`docs/aws-academy-setup.md`](docs/aws-academy-setup.md)
- SQLAlchemy 2.0: <https://docs.sqlalchemy.org/en/20/>

## Licença

[GNU General Public License v3.0](LICENSE).
