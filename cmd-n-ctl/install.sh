#!/usr/bin/env bash
# Install script for cmd-n-ctl part of mySatComm github project
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
fi

# Install pip3
# ------------
echo
echo "Checking for pip3..."
dpkg -l python3-pip &>/dev/null
if [ $? ]; then
    echo "pip3 already installed, moving on"
else
    sudo apt install python3-pip
    if ! [ $? ]; then
        errmsg
        exit 2
    fi
fi

# Install pigpio daemon
# ---------------------
echo
echo "Checking for pigpio daemon..."
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

