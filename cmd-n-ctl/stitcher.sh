#!/usr/bin/env bash
#
# This file "stitches" together the resources needed to interface with hamlib
# Intended only for experimentation/learning. There are things here that should
# not be hardcoded and it is not nearly robust enough to run on a given setup
# without heavy care
#
# author: Marion Anderson
# date:   2018-06-12
# file:   stitcher.sh

# run servo control daemon
sudo pigpiod

# stitch ttyS10 and ttyS11 together
sudo socat PTY,link=/dev/ttyS10 PTY,link=/dev/ttyS11 &

# rotator control
# use EasyCommm I protocol for simplicity
sudo rotctld -m 201 -T 10.0.0.117 -vvvvv -r /dev/ttyS10 &> rotlog.log &
