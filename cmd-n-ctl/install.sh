#!/usr/bin/env bash
# Install script for cmd-n-ctl part of mySatComm github project
<<<<<<< HEAD
# Creates and installs directly into a virtual environment
=======
>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
# Intended to be run on Raspberry Pi system

# Script Setup
# ============
<<<<<<< HEAD
set -o errexit
set -o pipefail

=======
set -o errexit 
set -o pipefail
>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
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

<<<<<<< HEAD
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
=======
# Script Execution
# ================
# Notify user script is running
# -----------------------------
if [ $# -gt 1 ]; then
    echo "Error: too many arguments"
    helpmsg
    exit 1
fi
execstr="Running cmd-n-ctl install.sh"
if [ $# -eq 1 ] && [ $1 = "--venv" ]; then
    execstr+=" with python virtualenv"
    echo "tmp file as installer flag" >> env_install
elif [ $# -eq 1 ] && [ $1 = "-h" ]; then
    helpmsg
    exit 0
elif [ $# -ne 0 ]; then
    echo "Error: bad arguments"
    helpmsg
    exit 1
fi
echo "$execstr..."
echo

# Install  hamlib
# ---------------
echo
echo "Checking for hamlib"
dpkg -l libhamlib-doc libhamlib-dev libhamlib-utils &>/dev/null
if [ $? ]; then
    echo "hamlib alreading installed, moving on"
else
    sudo apt install libhamlib-doc libhamlib-dev libhamlib-utils
>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
fi

# Install pip3
# ------------
echo
echo "Checking for pip3..."
<<<<<<< HEAD
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
=======
dpkg -l python3-pip &>/dev/null
if [ $? ]; then
    echo "pip3 already installed, moving on"
else
    sudo apt install python3-pip
    if ! [ $? ]; then
        errmsg
        exit 2
    fi
>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
fi

# Install pigpio daemon
# ---------------------
echo
echo "Checking for pigpio daemon..."
<<<<<<< HEAD
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
=======
dpkg -l pigpio &>/dev/null
if [ $? ]; then
    echo "pigpio already installed, moving on"
else
    sudo apt install pigpio
    if ! [ $? ]; then
        errmsg
        exit 3
    fi
fi

if  [ -e env_install ]; then
    echo
    echo "Installing virtualenv"
    sudo apt install python3-venv
    if ! [ $? ]; then
        errmsg
        exit 4
    fi

    # activating virtualenv
    python3 -m venv env
    source env/bin/activate
    echo
    echo "Virtual environment activated"
fi

# install SainSmart class and exception
echo
echo "Installing sainsmart-lib..."
pip3 install -e sainsmart-lib/
if ! [ $? ]; then
    errmsg
    exit 5
fi

echo "Installation Complete!"
if [ -e env_install ]; then
    rm env_install  # remove file flag
    deactivate
    echo
    echo "Virtual environment stored in cmd-n-ctl/env/bin/activate"
fi
exit 0

>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
