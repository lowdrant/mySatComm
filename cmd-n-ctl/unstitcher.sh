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

# find & kill pigpiod daemon
sudo kill $(ps aux | grep pigpiod | cut -d' ' -f7)

# kill off concat'd terminals
sudo kill $(ps aux | grep "sudo socat" | cut -d' ' -f7)

# kill rotator control
sudo kill $(ps aux | grep "sudo rotctld" | cut -d' ' -f6)
