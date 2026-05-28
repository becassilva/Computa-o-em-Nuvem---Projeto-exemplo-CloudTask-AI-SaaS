"""Ponto de entrada da aplicação CloudTask AI SaaS.

Este módulo instancia o objeto :class:`fastapi.FastAPI` que será servido
pelo ``uvicorn`` e registra os routers HTTP. Em aulas futuras este arquivo
crescerá com configuração via ``.env`` (Aula 4), conexão com banco
(Aula 3), middlewares de logging/CORS, etc.

Formas de execução:
    Local (com venv)::

        $ uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

    Docker (target dev)::

        $ docker build --target dev -t cloudtask-api:dev .
        $ docker run --rm -p 8000:8000 cloudtask-api:dev

    Devcontainer (VS Code)::

        F1 → "Dev Containers: Reopen in Container"

URLs úteis após subir:
    * Swagger UI:    http://localhost:8000/docs
    * ReDoc:         http://localhost:8000/redoc
    * OpenAPI JSON:  http://localhost:8000/openapi.json
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI, status

from app import __version__
from app.api import routes_health, routes_tasks
from app.db.database import Base, engine
from app.schemas import RootResponse

# ---------------------------------------------------------------------------
# Texto rico em Markdown exibido na home do Swagger UI.
# CommonMark + GFM (tabelas) + HTML inline são suportados.
# ---------------------------------------------------------------------------
APP_DESCRIPTION = """\
Mini **SaaS de gerenciamento de tarefas** construído ao longo da disciplina
**Computação em Nuvem** (N-CPU / UNINTER).

Esta é a versão da **Semana 2** (versão `0.2.0`): além da base da Semana 1
(FastAPI + Docker + devcontainer), adicionamos **PostgreSQL** e o **CRUD de
tarefas** (`/tasks`).

### Status do projeto

> A coluna **Semana atual** está marcada com `← você está aqui`. A versão
> da API é incrementada para `0.N.0` no início de cada semana.

| Semana | Branch                          | Tema                                                          |
| -----: | :------------------------------ | :------------------------------------------------------------ |
|      1 | `semana-01-fastapi-docker`      | FastAPI mínimo, Docker e Docker Compose, devcontainer         |
| <kbd>2</kbd> ← *você está aqui* | `semana-02-rds-vpc-seguranca`   | PostgreSQL + CRUD, config `.env`, HTTPS, docs de VPC/IAM      |
|      3 | `semana-03-s3-kubernetes`       | Upload S3 (com fallback local), Kubernetes local (Kind)       |
|      4 | `semana-04-eks-aws`             | Build/push para ECR, deploy no EKS                            |
|      5 | `semana-05-custos-nosql-logs`   | HPA + teste de carga + Cost Explorer, eventos com DynamoDB    |
|      6 | `semana-06-cdk-final`           | AWS CDK (S3, ECR, VPC), docs finais e checklist LGPD          |

### Tags

- <span style="color:#0ea5e9">**meta**</span> — metadados da aplicação.
- <span style="color:#16a34a">**health**</span> — endpoints de saúde para orquestradores.
- <span style="color:#f59e0b">**tasks**</span> — CRUD de tarefas (PostgreSQL).

### Links úteis

- [Issue mais recente (Aula 3)](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/3)
- [Roadmap completo](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/blob/main/docs/ROADMAP.md)
- [Lista de tarefas (`docs/TAREFAS.md`)](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/blob/main/docs/TAREFAS.md)

<details>
<summary><b>Como rodar localmente</b></summary>

```bash
# 1. Subir API + PostgreSQL via Docker Compose
docker compose up --build

# 2. Testar
curl http://localhost:8000/health
curl http://localhost:8000/tasks
```

Ou abra o projeto no VS Code e use `F1 → "Dev Containers: Reopen in Container"`.
</details>
"""


ROOT_DESCRIPTION = """\
Devolve **identificação básica** do serviço.

Usado por humanos para descobrir rapidamente onde acessar a documentação
interativa e por monitores externos para confirmar qual versão está
implantada.

### Campos retornados

| Campo | Tipo | Descrição |
| --- | --- | --- |
| `name` | `string` | Nome legível do serviço. |
| `version` | `string` | Versão semântica corrente. |
| `docs` | `string` | Caminho relativo do Swagger UI. |

### Exemplos de uso

**curl**

```bash
curl -s http://localhost:8000/
# {"name":"CloudTask AI SaaS","version":"0.1.0","docs":"/docs"}
```

**Python (httpx)**

```python
import httpx

resposta = httpx.get("http://localhost:8000/")
assert resposta.status_code == 200
print(resposta.json()["docs"])  # /docs
```

> <kbd>Dica</kbd> — use este endpoint como **canary check** após cada
> deploy: se ele responder com a nova `version`, o pod novo já está
> servindo tráfego.
"""


# ---------------------------------------------------------------------------
# Ciclo de vida da aplicação (startup / shutdown).
#
# No startup, criamos as tabelas no banco caso ainda não existam.
#
# POR QUÊ `create_all` aqui (e não uma ferramenta de migração como Alembic):
#   é o jeito mais simples e didático para a Aula 3. `create_all` apenas CRIA
#   tabelas que faltam — não altera tabelas já existentes.
# RISCO/LIMITAÇÃO: se um dia você mudar uma coluna, `create_all` NÃO migra o
#   schema. Em projeto real usa-se Alembic. Mencionamos isso para o aluno saber
#   que esta é uma simplificação consciente de ensino.
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncGenerator[None, None]:
    """Cria as tabelas no startup e cede o controle à aplicação."""
    Base.metadata.create_all(bind=engine)
    yield
    # (Nada a desfazer no shutdown nesta aula.)


# ---------------------------------------------------------------------------
# Instância principal do FastAPI.
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloudTask AI SaaS",
    description=APP_DESCRIPTION,
    version=__version__,
    lifespan=lifespan,
    contact={
        "name": "Prof. Guilherme Patriota",
        "url": "https://github.com/guipatriota",
    },
    license_info={
        "name": "GNU GPL v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.html",
    },
    openapi_tags=[
        {"name": "meta", "description": "Metadados gerais da aplicação."},
        {
            "name": "health",
            "description": "Endpoints de saúde usados por Docker, Kubernetes e Load Balancers.",
        },
        {
            "name": "tasks",
            "description": "CRUD de tarefas, persistidas em PostgreSQL.",
        },
    ],
)

# Registra os routers na aplicação.
app.include_router(routes_health.router)
app.include_router(routes_tasks.router)


@app.get(
    "/",
    response_model=RootResponse,
    status_code=status.HTTP_200_OK,
    summary="Metadados da aplicação",
    description=ROOT_DESCRIPTION,
    tags=["meta"],
    response_description="Identificação básica do serviço.",
    responses={
        200: {
            "description": "Metadados retornados com sucesso.",
            "content": {
                "application/json": {
                    "example": {
                        "name": "CloudTask AI SaaS",
                        "version": "0.1.0",
                        "docs": "/docs",
                    }
                }
            },
        }
    },
)
def root() -> RootResponse:
    """Devolve identificação básica do serviço.

    Returns:
        RootResponse: Nome, versão e caminho do Swagger.

    Example:
        >>> r = root()
        >>> r.name, r.docs
        ('CloudTask AI SaaS', '/docs')
    """
    return RootResponse(
        name="CloudTask AI SaaS",
        version=__version__,
        docs="/docs",
    )
