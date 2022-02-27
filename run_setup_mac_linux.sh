#!bin/bash

chmod 775 run_game_mac_linux.sh &&
apt install python3.9-venv &&
python3 -m venv battle &&
source battle/bin/activate &&
pip install -r requirements.txt &&
python3 -m initiate &&
deactivate
