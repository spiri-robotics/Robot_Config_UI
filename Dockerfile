FROM ghcr.io/astral-sh/uv:debian

RUN apt-get update && apt-get install -y \
    curl && \
    curl -fsSL https://get.docker.com | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./ /app
WORKDIR /app
RUN uv build
CMD uv run python -m spiriRobotUI.main