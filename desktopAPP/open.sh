#!/bin/bash

# Open the first terminal and run the Python script
gnome-terminal -- bash -c "
cd /home/orangepi/NIKKEAutoScript;
source VENV/bin/activate;
python gui.py;
exec bash"

# Open the second terminal and run the npm command
gnome-terminal -- bash -c "
cd /home/orangepi/NIKKEAutoScript/webapp;
npm run watch;
exec bash"
