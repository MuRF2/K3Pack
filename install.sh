#!/bin/bash

git clone https://github.com/MuRF2/K3Pack
cd ./K3Pack
python3 -m venv K3Pack-env
source ./K3Pack-env/bin/activate
pip install -r requirements.txt
pyinstaller --onefile main.py
mv ./dist/main ./K3Pack
deactivate

