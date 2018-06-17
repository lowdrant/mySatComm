#!/usr/bin/env bash
# Uninstall script for cmd-n-ctl part of mySatComm github project
# Intended to be run on a Raspberry Pi system

# Script Setup
# ============
set -o pipefail -o errexit

function helpmsg() {
  echo "usage: uninstall.sh [--all]"
  echo "Uninstalls antenna controller python libraries and scripts"
  echo "  --all       Remove all packages, not just sainsmart-lib"
}

# Script Execution
# ================
# Notify user script is running
# -----------------------------
echo "Running cmd-n-ctl/uninstall.sh"
goflag="n"

if [ $# -gt 1 ]; then
  echo "Error: too many arguments"
  helpmsg
  exit 1
elif [ $# -eq 1 ] && [ $1 = "-h" ]; then
  helpmsg
  exit 0
elif [ $# -eq 1 ] && [ $1 = '--all' ]; then
  echo
  echo -n "--all flag selected. This WILL uninstall ALL system dependencies,"
  echo " including pip."
  read -p "Continue? (y/n): " goflag
  if ! [ "$goflag" = "y" ]; then
    echo "Exiting"
    exit 0
  fi
elif [ $# -ne 0 ]; then
  echo "Error: bad argument"
  helpmsg
  exit 1
fi

# Removing python packages
# ------------------------
source /home/$USER/.satcomm/bin/activate
echo; echo "Virtual environment activated"
pip3 uninstall "sainsmart" --yes
pip3 uninstall "pyserial" --yes
pip3 uninstall "click" --yes
deactivate
rm -rf /home/$USER/.satcomm

# Remove other packages as well
# -----------------------------
if [ "$goflag" = 'y' ]; then
  sudo apt remove libhamlib-doc libhamlib-dev libhamlib-utils pigpio python3-pip python3-venv socat --purge
  echo 'All dependencies at system-level removed'
fi

echo; echo "Removal Complete!"
exit 0
