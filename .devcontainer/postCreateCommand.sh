#!/bin/sh
# postCreateCommand.sh

set -e

direnv hook bash >> ~/.bashrc
direnv allow

uv sync --group dev
if ! grep -q ". .venv/bin/activate" ~/.bashrc 2>/dev/null; then
  echo ". .venv/bin/activate" >> ~/.bashrc
fi
