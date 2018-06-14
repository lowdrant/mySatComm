#!/usr/bin/env bash
# Install script for cmd-n-ctl part of mySatComm github project
# Creates and installs directly into a virtual environment
# Intended to be run on Raspberry Pi system

# Script Setup
# ============
set -o errexit
set -o pipefail

function errmsg() {
    echo -n "Something went wrong!"
    echo " Make sure your system is set up properly"
}

function helpmsg() {
    echo "usage: install.sh [--venv]"
    echo "Installs antenna controller libraries and scripts"
    printf "\n  --venv       Install python libraries"
    echo " in a virtual environment"
}

function errcheck() {
  if ! [ $? ]; then
    errmsg
    exit 1
  fi
}

# Script Execution
# ================
echo "Running cmd-n-ctl install.sh"

# Install python3
# ---------------
echo
echo "Checking for python3"
dpkg -l python3 &> /dev/null
if [ $? ]; then
  echo "python3 already installed, moving on"
else
  sudo apt install python3 &> /dev/null
  errcheck; echo "python3 installed!"
fi

# Install pip3
# ------------
echo
echo "Checking for pip3..."
dpkg -l python3-pip &> /dev/null
if [ $? ]; then
  echo "pip3 already installed, moving on"
else
  sudo apt install python3-pip &> /dev/null
  errcheck; echo "pip3 installed!"
fi

# Install  hamlib
# ---------------
echo
echo "Checking for hamlib"
dpkg -l libhamlib-doc libhamlib-dev libhamlib-utils &> /dev/null
if [ $? ]; then
  echo "hamlib alreading installed, moving on"
else
  sudo apt install libhamlib-doc libhamlib-dev libhamlib-utils &> /dev/null
  errcheck; echo "hamlib installed!"
fi

# Install pigpio daemon
# ---------------------
echo
echo "Checking for pigpio daemon..."
dpkg -l pigpio &> /dev/null
if [ $? ]; then
  echo "pigpio already installed, moving on"
else
  sudo apt install pigpio &> /dev/null
  errcheck
  echo "pigpio installed!"
fi

# Install & activate virtualenv
# -----------------------------
echo
echo "Checking for virtualenv..."
dpkg -l python3-virtualenv &> /dev/null
if [ $? ]; then
  echo "virtualenv already installed, moving on"
else
  sudo apt install python3-virtualenv
  errcheck; echo "virtualenv installed!"
fi
# activating virtualenv
echo "Creating virtual environment..."
python3 -m venv satcomm
source satcomm/bin/activate
errcheck
echo "Virtual environment activated!"
echo "Installing python packages..."

# Install python packages
# -----------------------
echo "Installing sainsmart-lib..."
pip3 install -e sainsmart-lib/; errcheck
echo "Installing pyserial..."
pip3 install pyserial; errcheck

# Cleanup
# -------
deactivate
echo
echo "Installation Complete!"
echo "Virtual environment stored in cmd-n-ctl/satcomm/bin/activate"

exit 0
