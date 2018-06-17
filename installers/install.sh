#!/usr/bin/env bash
# Install script for cmd-n-ctl part of mySatComm github project
# Creates and installs directly into a virtual environment
# Intended to be run on Raspberry Pi system

# Script Setup
# ============
set -o errexit -o pipefail

# Script Execution
# ================
echo "Running cmd-n-ctl install.sh"

# Install python3
# ---------------
echo
echo "Checking for python3..."
sudo apt install python3

# Install pip3
# ------------
echo
echo "Checking for pip3..."
sudo apt install python3-pip

# Install  hamlib
# ---------------
echo
echo "Checking for hamlib..."
sudo apt install libhamlib-doc libhamlib-dev libhamlib-utils

# Install socat
# -------------
echo
echo "Checking for socat..."
sudo apt install socat

# Install pigpio daemon
# ---------------------
echo
echo "Checking for pigpio daemon..."
sudo apt install pigpio

# Install & activate virtualenv
# -----------------------------
echo
echo "Checking for virtualenv..."
sudo pip3 install virtualenv

# activating virtualenv
if ! [ -e /home/$USER/.satcomm/bin/activate ]; then
  echo; echo "Creating virtual environment..."
  python3 -m venv /home/$USER/.satcomm
fi
source /home/$USER/.satcomm/bin/activate
echo "Virtual environment activated!"
echo; echo "Installing python packages..."

# Install python packages
# -----------------------
echo "Installing sainsmart-lib..."
pip3 install -e ../cmd-n-ctl/sainsmart-lib/ --no-cache-dir
echo; echo "Installing pyserial..."
pip3 install pyserial --no-cache-dir
echo; echo "Installing click..."
pip3 install click --no-cache-dir

# Cleanup
# -------
deactivate
echo
echo "Installation Complete!"
echo "Virtual environment stored in /home/pi/.satcomm/bin/activate"

exit 0
