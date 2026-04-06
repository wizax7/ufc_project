FROM python:3.12-slim 

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app 

ENV UV_SYSTEM_PYTHON=1

COPY pyproject.toml uv.lock ./  
RUN uv sync --frozen --no-install-project 

COPY . .

ENTRYPOINT [ "uv", "run", "python", "-m", "main" ]