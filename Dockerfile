FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh
ENV PATH="/root/.local/bin/:$PATH"

RUN useradd -m appuser
WORKDIR /app
COPY pyproject.toml uv.lock /app/
COPY valgem/ /app/valgem/
RUN uv sync --locked --compile-bytecode


CMD ["uv", "run", "valgem"]