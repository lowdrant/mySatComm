#! /bin/bash
# Install script for cmd-n-ctl part of mySatComm github project
# Intended to be run on Raspberry Pi system

printf "Running mySatComm/install.sh...\n\n"

# pip for python3
printf "Checking for pip3...\n"
dpkg -l python3-pip
if [ $? ]; then
    printf "pip3 installed, moving on..."
else
    printf "Installing pip3..."
    sudo apt install python3-pip
fi

# pigpio
printf "Checking for pigpio...\n"
dpkg -l pigpio
if [ $? ]; then
    printf "pigpio installed, moving on..."
else
    printf "Installing pigpio..."
    sudo apt install pigpio
fi

# pigpio for python
printf "Checking for python3-pigpio...\n"
dpkg -l pigpio
if [ $? ]; then
    printf "python3-pigpio installed, moving on..."
else
    printf "Installing python3-pigpio..."
    sudo apt install python3-pigpio
fi

printf "Installation Complete\n"
