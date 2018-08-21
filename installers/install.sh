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
script_path=$(dirname "$0")  # for copying files

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
if ! [ -e "$HOME/.satcomm/bin/activate" ]; then
  echo; echo "Creating virtual environment..."
  python3 -m venv "$HOME/.satcomm/"
fi
source "$HOME/.satcomm/bin/activate"
echo "Virtual environment activated!"
echo; echo "Installing python packages..."

# Install python packages
# -----------------------
echo "Installing rotator-lib..."
pip3 install -e "$script_path/../cmd-n-ctl/rotator-lib/" --no-cache-dir
echo; echo "Installing pyserial..."
pip3 install pyserial --no-cache-dir
echo; echo "Installing click..."
pip3 install click --no-cache-dir

# Copy utils
# ----------
# for loop is necessary because the dynamic path interferes with globbing
# yes, it is hacky. If you have a more robust solution please let me know
for i in $(ls "$script_path/../cmd-n-ctl/utils/"); do
    cp -r "$script_path/../cmd-n-ctl/utils/$i" "$HOME/.satcomm/bin/"
done
cp "../run.sh" "$HOME/.satcomm/bin/"

# Cleanup
# -------
deactivate
echo
echo "Installation Complete!"
echo "Virtual environment stored in $HOME/.satcomm/bin/activate"

exit 0
