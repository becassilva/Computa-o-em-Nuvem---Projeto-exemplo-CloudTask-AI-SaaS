<!-- Área do Banner -->
<div align="center" style="background-color: white; max-width: 70%;">
  <img alt="BANNER do repositório CloudTask AI SaaS — disciplina Computação em Nuvem" title="Banner_CloudTask_AI_SaaS" src=".readme_docs/Banner_Github_NCPU.png" width="100%" />
</div>

<!-- Título e breve descrição do repositório -->
<div align="center">
  <h1>CloudTask AI SaaS — Aula 1</h1>
  <p><b>Branch <code>semana-01-fastapi-docker</code> — estado pós Aula 1.</b></p>
  <p>API FastAPI mínima (<code>/health</code> e <code>/</code>) + Dockerfile multi-target + devcontainer do VS Code.</p>
</div>

<p align="center">
  <a href="https://www.python.org/" title="Python"><img src="https://github.com/get-icon/geticon/raw/master/icons/python.svg" alt="Python" height="21px"></a>
  +
  <a href="https://fastapi.tiangolo.com/" title="FastAPI"><img src="https://github.com/get-icon/geticon/raw/master/icons/fastapi.svg" alt="FastAPI" height="21px"></a>
  +
  <a href="https://www.docker.com/" title="Docker"><img src="https://github.com/get-icon/geticon/raw/master/icons/docker-icon.svg" alt="Docker" height="21px"></a>
</p>

## O que foi entregue nesta aula

- Estrutura inicial do pacote `app/`:
  - `app/main.py` — instância do FastAPI.
  - `app/api/routes_health.py` — endpoint `GET /health`.
- Endpoints:
  - `GET /` — metadados (nome, versão, link para `/docs`).
  - `GET /health` — `{"status": "ok"}`.
  - `GET /docs` — Swagger gerado pela FastAPI.
- `requirements.txt` (produção) e `requirements-dev.txt` (debug, lint, hot-reload).
- `Dockerfile` **multi-target** com estágios `dev` e `prod` (a base para todas as próximas aulas).
- `.dockerignore` evitando levar `.git`, `.venv`, segredos e pastas auxiliares para a imagem.
- `.devcontainer/devcontainer.json` que abre a aplicação no VS Code dentro do container `dev` — desenvolvimento **cloud-native desde o primeiro dia**.
- `.vscode/launch.json` com configurações de debug (launch direto + attach na porta 5678).

## Pré-requisitos

| Ferramenta              | Versão mínima | Para quê                                         |
| ----------------------- | ------------- | ------------------------------------------------ |
| Git                     | 2.40          | Clonar e trocar de branches.                     |
| Docker Desktop          | 4.30          | Construir e rodar a imagem.                      |
| VS Code                 | 1.90          | Editor de código.                                |
| Extensão Dev Containers | 0.380         | Abrir o projeto dentro do container.             |
| Python *(opcional)*     | 3.11          | Rodar fora do container, se preferir.            |

> No Windows, use **WSL2** com integração ao Docker Desktop. No macOS/Linux funciona nativo.

## Como rodar — três caminhos

### 1) Devcontainer no VS Code (recomendado)

```text
1. Abra a pasta deste repositório no VS Code.
2. F1 → "Dev Containers: Reopen in Container".
3. Aguarde o build (só na primeira vez).
4. No terminal integrado:  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
5. Abra http://localhost:8000/docs no navegador do host.
```

Para depurar, use `Run and Debug` (`Ctrl+Shift+D`) → escolha **"FastAPI (uvicorn debug)"** e coloque breakpoints em `app/*.py`.

### 2) Docker puro (sem VS Code)

```bash
# Build da imagem de desenvolvimento
docker build --target dev -t cloudtask-api:dev .

# Subir a API com hot-reload e código montado por volume
docker run --rm -it -p 8000:8000 -v "${PWD}:/app" cloudtask-api:dev

# Testar
curl http://localhost:8000/health
# resposta esperada: {"status":"ok"}
```

A imagem de produção (sem ferramentas de dev) é construída com:

```bash
docker build --target prod -t cloudtask-api:prod .
```

### 3) Python local (sem Docker)

```bash
python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# macOS / Linux:         source .venv/bin/activate

pip install -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Endpoints

| Método | Caminho           | Descrição                                    |
| ------ | ----------------- | -------------------------------------------- |
| GET    | `/`               | Metadados da aplicação.                      |
| GET    | `/health`         | Liveness probe (`{"status": "ok"}`).         |
| GET    | `/docs`           | Swagger UI interativo (gerado pela FastAPI). |
| GET    | `/openapi.json`   | Especificação OpenAPI.                       |

## O que vem na próxima aula

- **Aula 2 (mesma branch `semana-01-fastapi-docker`):** Docker Compose para a API. Devcontainer continua usando o mesmo Dockerfile, sem mudanças.
- **Semana 2 (branch `semana-02-rds-vpc-seguranca`):**
  - Aula 3: PostgreSQL 16 (**compatível com Amazon RDS for PostgreSQL**) via Compose, CRUD de tarefas.
  - O devcontainer migrará de `"build"` para `"dockerComposeFile"` apontando para o `docker-compose.yml` com serviço `db`.

## Referências

- Issue da aula: [#1 — Aula 1](https://github.com/N-CPUninter/Computa-o-em-Nuvem---Projeto-exemplo-CloudTask-AI-SaaS/issues/1)
- Lista completa de tarefas: [`docs/TAREFAS.md`](docs/TAREFAS.md)
- Guia geral: [`docs/HOW_TO_USE.md`](docs/HOW_TO_USE.md)
- Roadmap: [`docs/ROADMAP.md`](docs/ROADMAP.md)
- Exemplos didáticos de Dockerfile: [`exemplos/dockerfile/`](exemplos/dockerfile/)

## Licença

[GNU General Public License v3.0](LICENSE).
