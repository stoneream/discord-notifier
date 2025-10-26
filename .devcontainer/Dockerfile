FROM mcr.microsoft.com/devcontainers/python:3.13

# Install direnv
RUN curl -sfL https://direnv.net/install.sh | bash

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:/root/.cargo/bin:${PATH}"
