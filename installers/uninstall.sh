#!/usr/bin/env bash
# Uninstall script for cmd-n-ctl part of mySatComm github project
# Intended to be run on a Raspberry Pi system

# Script Setup
# ============
set -o pipefail -o errexit
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
}

# Script Execution
# ================
# Notify user script is running
# -----------------------------
echo "Running cmd-n-ctl/uninstall.sh"
if [ $# -gt 1 ]; then
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
source /home/py/mySatComm/cmd-n-ctl/satcomm/bin/activate
echo; echo "Virtual environment activated!"
echo "Removing sainsmart-lib..."
pip3 uninstall sainsmart; errcheck; echo "sainsmart-lib uninstalled!"
echo; echo "Removing pyserial..."
pip3 uninstall pyserial; errcheck; echo "pyserial uninstalled!"
echo; echo "Removing click..."
pip3 uninstall click; errcheck; echo "click uninstalled!"

# Remove other packages as well
# -----------------------------
if [ "$1" = "--all" ]; then
  echo "--all flag selected. This WILL uninstall python3 & pip."
  echo -n "Continue? (y/n):"
  read -n 1 goflag
  if [goflag = 'y' ]; then
    sudo apt remove libhamlib-doc libhamlib-dev libhamlib-utils pigpio pip3 python3-venv python3 socat --purge
    echo 'All dependencies at system-level removed'
  fi
  echo 'Aborting...'
  exit 0
fi

echo; echo "Removal Complete!"
exit 0
