#!/usr/bin/env bash
# Uninstall script for cmd-n-ctl part of mySatComm github project
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
}

# Script Execution
# ================
# Notify user script is running
# -----------------------------
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


echo "Removal Complete!"
exit 0
