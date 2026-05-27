"""
Endpoints de health-check da API.

`/health` é o endpoint padrão lido por:
  - Docker HEALTHCHECK (definido no Dockerfile)
  - readinessProbe / livenessProbe do Kubernetes (Aulas 6 e 8)
  - Load Balancers (ELB/ALB) na frente do EKS (Aula 8)

Mantenha esta rota leve e SEM dependências externas (banco, rede, etc.).
Em aulas futuras (Aula 3+), criaremos um `/health/ready` separado que
verifica banco/serviços.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Liveness probe")
def health() -> dict[str, str]:
    """Responde 200 OK se o processo da API está vivo."""
    return {"status": "ok"}
