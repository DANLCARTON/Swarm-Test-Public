#!/bin/bash
#
#

# Start script to begin scenario

sleep 1

# puredata /home/pi/Wavematrix-scenario/main.pd

# cd /home/pi/c-climate/claim_monitor
cd claim_monitor

#lxterminal -e python3 cl_monitor.py &
py cl_monitor.py &

sleep 120

#cd /home/pi/c-climate
cd ..

#lxterminal -e python3 scenario.py &
py scenario.py &