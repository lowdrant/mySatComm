#!/usr/bin/env bash
#
# This file "unstitches" the resources needed to interface with hamlib
# Intended only for experimentation/learning. There are things here that should
# not be hardcoded and it is not nearly robust enough to run on a given setup
# without heavy care
#
# author: Marion Anderson
# date:   2018-06-12
# file:   unstitcher.sh

# Helper function to get pid of satcomm BASH commands
# takes one arg, the input string
# usage: `get_pid "input str"``
get_pid() {
  str=$(ps aux | grep "$1" | head --lines=1)
  str=$(tr --squeeze-repeats " " <<< "$str")
  pid=$(cut --delimiter=' ' --fields=2 <<< "$str")
}

# find & kill pigpiod daemon
sudo kill $(get_pid "pigpiod")
if ! [ $? ]
then
  echo 'Failed to kill pigpiod!'
fi

# kill off concat'd terminals
sudo kill $(get_pid "socat")
if ! [ $? ]
then
  echo 'Failed to kill socat!'
fi

# kill rotator control
sudo kill $(get_pid "rotctld")
if ! [ $? ]
then
  echo 'Failed to kill rotctld!'
fi
