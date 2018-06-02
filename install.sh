#! /bin/bash
# Install script for cmd-n-ctl part of mySatComm github project
# Intended to be run on Raspberry Pi system
#
# You may want to run this in a virtual environment
# I may implement venvs in this repo at some point, but no promises

function errmsg() {
    echo -n "Something went wrong!"
    echo " Make sure your system is set up properly"
    exit 1
}

printf "Running mySatComm/install.sh...\n\n"

# pip for python3
echo "Checking for pip3..."
dpkg -l python3-pip &>/dev/null
if [ $? ]; then
    echo "pip3 installed, moving on..."
else
    echo "Installing pip3..."
    sudo apt install python3-pip
    if ! [ $? ]; then
        errmsg
    fi
fi

# pigpio
printf "\nChecking for pigpio..."
dpkg -l pigpio &>/dev/null
if [ $? ]; then
    echo "pigpio installed, moving on..."
else
    echo "Installing pigpio..."
    sudo apt install pigpio
    if ! [ $? ]; then
        errmsg
    fi
fi

# install SainSmart class and exception
printf "\nInstalling sainsmart...\n"
pip3 install -e cmd-n-ctl/sainsmart-lib
if ! [ $? ]; then
    errmsg
fi

printf "Installation Complete\n"
exit 0
