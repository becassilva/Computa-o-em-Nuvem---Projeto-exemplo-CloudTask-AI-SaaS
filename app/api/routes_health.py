"""Rotas de health-check da API CloudTask AI SaaS.

Endpoints leves usados por:

* ``HEALTHCHECK`` do Docker (definido no ``Dockerfile``).
* ``readinessProbe`` / ``livenessProbe`` do Kubernetes (Aulas 6 e 8).
* Load Balancers (ELB/ALB/NLB) na frente do EKS (Aula 8).

Não dependem de banco nem de serviços externos — manter assim. Em aulas
futuras (Aula 3+) introduziremos um ``/health/ready`` separado que
verifica conexão com PostgreSQL/RDS, S3, etc.
"""

from __future__ import annotations

from fastapi import APIRouter, status

from app.schemas import HealthResponse

router = APIRouter(tags=["health"])


HEALTH_DESCRIPTION = """\
Indica se o **processo da API está vivo**.

Endpoint leve e sem dependências externas, projetado para ser chamado por
orquestradores (Docker, Kubernetes, Load Balancers) **milhares de vezes
por dia** sem custo perceptível.

### Quando usar

| Consumidor | Configuração |
| --- | --- |
| Docker | `HEALTHCHECK` no `Dockerfile` |
| Kubernetes | `livenessProbe.httpGet.path: /health` |
| AWS ELB/ALB | Target Group Health Check Path = `/health` |

> <kbd>Importante</kbd> — esta rota **não** valida banco ou serviços
> externos. Para um check "está pronto para receber tráfego?", aguarde o
> endpoint `GET /health/ready` que será adicionado na Aula 3.

### Exemplos de uso

**curl**

```bash
curl -s http://localhost:8000/health
# {"status":"ok"}
```

**Python (httpx)**

```python
import httpx

resposta = httpx.get("http://localhost:8000/health")
assert resposta.status_code == 200
assert resposta.json() == {"status": "ok"}
```

**Manifest Kubernetes (trecho)**

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 15
  periodSeconds: 20
```
"""


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Liveness probe da aplicação",
    description=HEALTH_DESCRIPTION,
    response_description="Estado do processo da API.",
    responses={
        200: {
            "description": "Aplicação viva e respondendo.",
            "content": {
                "application/json": {
                    "example": {"status": "ok"},
                }
            },
        },
    },
)
def health() -> HealthResponse:
    """Indica se o processo da API está vivo.

    Returns:
        HealthResponse: Objeto contendo ``status == "ok"`` quando o
        processo Python responde corretamente a requisições HTTP.

    Example:
        >>> health().status
        'ok'
    """
    return HealthResponse(status="ok")
