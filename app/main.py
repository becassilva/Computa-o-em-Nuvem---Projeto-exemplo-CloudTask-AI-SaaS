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

from fastapi import FastAPI, status

from app import __version__
from app.api import routes_health
from app.schemas import RootResponse

# ---------------------------------------------------------------------------
# Texto rico em Markdown exibido na home do Swagger UI.
# CommonMark + GFM (tabelas) + HTML inline são suportados.
# ---------------------------------------------------------------------------
APP_DESCRIPTION = """\
Mini **SaaS de gerenciamento de tarefas** construído ao longo da disciplina
**Computação em Nuvem** (N-CPU / UNINTER).

Esta é a versão da **Aula 1**: apenas endpoints básicos para validar a
estrutura do projeto, do Docker e do devcontainer.

### Status do projeto

| Aula | Branch | Tema |
| ---: | :--- | :--- |
| <kbd>1</kbd> ← *você está aqui* | `semana-01-fastapi-docker` | FastAPI mínimo + Docker + devcontainer |
| 2 | `semana-01-fastapi-docker` | Docker Compose |
| 3 | `semana-02-rds-vpc-seguranca` | PostgreSQL + CRUD de tarefas |
| 4 | `semana-02-rds-vpc-seguranca` | Config `.env` + docs VPC/IAM |

### Tags

- <span style="color:#0ea5e9">**meta**</span> — metadados da aplicação.
- <span style="color:#16a34a">**health**</span> — endpoints de saúde para orquestradores.

### Links úteis

- [Issue da Aula 1](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/1)
- [Roadmap completo](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/blob/main/docs/ROADMAP.md)
- [Lista de tarefas (`docs/TAREFAS.md`)](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/blob/main/docs/TAREFAS.md)

<details>
<summary><b>Como rodar localmente</b></summary>

```bash
# 1. Build da imagem de desenvolvimento
docker build --target dev -t cloudtask-api:dev .

# 2. Subir com hot-reload
docker run --rm -p 8000:8000 -v "$(pwd):/app" cloudtask-api:dev

# 3. Testar
curl http://localhost:8000/health
```
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
# Instância principal do FastAPI.
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloudTask AI SaaS",
    description=APP_DESCRIPTION,
    version=__version__,
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
    ],
)

# Registra os endpoints do módulo `routes_health` na aplicação.
app.include_router(routes_health.router)


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
