#!/bin/bash

tmux kill-server

cd /root/portfolio-site
git fetch && git reset origin/main --hard

source python3-virtualenv/bin/activate
pip install -r requirements.txt

tmux_cmd="
cd /root/portfolio-site
source python3-virtualenv/bin/activate
flask run --host=0.0.0.0 --port 80
"
tmux new-session -d -s portfolio-site "$tmux_cmd"

