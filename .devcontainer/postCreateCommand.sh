#!/bin/sh
# postCreateCommand.sh

direnv hook bash >> ~/.bashrc
direnv allow

pipenv install --dev
source $(pipenv --venv)/bin/activate
