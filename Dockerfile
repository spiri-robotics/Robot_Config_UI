FROM ghcr.io/astral-sh/uv:debian

COPY ./ /app
WORKDIR /app
RUN uv build
CMD uv run python -m spiriRobotUI.main