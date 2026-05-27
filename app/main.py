"""
Ponto de entrada da aplicação CloudTask AI SaaS.

Aula 1 — versão mínima:
  * Cria a instância FastAPI.
  * Registra o router de health-check.
  * Expõe a rota raiz `/` com metadados básicos.

Como rodar localmente:
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

Como rodar via Docker:
  docker build --target dev -t cloudtask-api:dev .
  docker run --rm -p 8000:8000 cloudtask-api:dev

Como rodar via devcontainer (VS Code):
  Abra a pasta → F1 → "Dev Containers: Reopen in Container".
"""

from fastapi import FastAPI

from app import __version__
from app.api import routes_health

# ---------------------------------------------------------------------------
# Instância principal do FastAPI.
# `title` e `version` aparecem no Swagger (http://localhost:8000/docs).
# ---------------------------------------------------------------------------
app = FastAPI(
    title="CloudTask AI SaaS",
    description=(
        "Mini SaaS de gerenciamento de tarefas construído ao longo da "
        "disciplina Computação em Nuvem (N-CPU / UNINTER)."
    ),
    version=__version__,
)

# Registra os endpoints do módulo `routes_health` na aplicação.
app.include_router(routes_health.router)


@app.get("/", summary="Metadados da aplicação")
def root() -> dict[str, str]:
    """Endpoint raiz — devolve identificação básica do serviço."""
    return {
        "name": "CloudTask AI SaaS",
        "version": __version__,
        "docs": "/docs",
    }
