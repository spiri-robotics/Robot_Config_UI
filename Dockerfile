FROM ghcr.io/astral-sh/uv:debian

RUN apt-get update && apt-get install -y \
    docker.io \
    docker-compose && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./ /app
WORKDIR /app
RUN uv build
CMD uv run python -m spiriRobotUI.main