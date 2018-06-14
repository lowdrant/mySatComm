#!/usr/bin/env bash
# Uninstall script for cmd-n-ctl part of mySatComm github project
<<<<<<< HEAD
# Intended to be run on a Raspberry Pi system

# Script Setup
# ============
set -o errexit
set -o pipefail
function errmsg() {
  echo -n "Something went wrong!"
  echo " Make sure your system is set up properly"
}

function helpmsg() {
  echo "usage: uninstall.sh [--all]"
  echo "Uninstalls antenna controller python libraries and scripts"
  echo "  --all       Remove all packages, not just sainsmart-lib"
}

function errcheck() {
  if ! [ $? ]; then
    errmsg
    exit 1
  fi
=======
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
    echo "usage: uninstall.sh [--all]"
    echo "Uninstalls antenna controller python libraries and scripts"
    echo "  --all       Remove all packages, not just sainsmart-lib"
>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
}

# Script Execution
# ================
# Notify user script is running
# -----------------------------
if [ $# -gt 1 ]; then
<<<<<<< HEAD
  echo "Error: too many arguments"
  helpmsg
  exit 1
elif [ $# -eq 1 ] && [ $1 = "-h" ]; then
  helpmsg
  exit 0
elif [ $# -ne 0 ]; then
  echo "Error: bad argument"
  helpmsg
  exit 1
fi

# Removing python packages
# ------------------------
# activate virtualenv
source satcomm/bin/activate
echo "Virtual environment activated..."
echo "Removing sainsmart-lib..."
pip3 uninstall sainsmart; errcheck; echo "sainsmart-lib uninstalled!"
echo "Removing pyserial..."
pip3 uninstall pyserial; errcheck; echo "pyserial uninstalled!"

# Remove other packages as well
# -----------------------------
if [ $1 -eq "--all" ]; then
  echo "--all flag selected. Waiting 5 seconds in case of error"
  sleep 5
  sudo apt remove libhamlib-doc libhamlib-dev libhamlib-utils pigpio pip3 python3-venv
fi

=======
    echo "Error: too many arguments"
    helpmsg
    exit 1
elif [ $# -eq 1 ] && [ $1 = "-h" ]; then
    helpmsg
    exit 0
elif [ $# -ne 0 ]; then
    echo "Error: bad argument"
    helpmsg
    exit 1
fi

# remove SainSmart
echo "Removing sainsmart-lib..."
if [ -e env/bin/activate ]; then
    echo "qwer"
    source env/bin/activate
fi
pip3 uninstall sainsmart

# remove else
if [ $# -eq 1 ] && [ $1 -eq "--all" ]; then
    sudo apt remove libhamlib-doc libhamlib-dev libhamlib-utils pigpio pip3 python3-venv
fi


>>>>>>> b57b9002a7d3ecd1ac8005d6ba4111375a266296
echo "Removal Complete!"
exit 0
