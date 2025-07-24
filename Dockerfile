FROM ghcr.io/astral-sh/uv:debian

RUN apt-get update && apt-get install -y \
    curl && \
    curl -fsSL https://get.docker.com | sh && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./ /app
WORKDIR /app

# Install uv dependencies
RUN uv run true
CMD uv run python -m spiriRobotUI.main