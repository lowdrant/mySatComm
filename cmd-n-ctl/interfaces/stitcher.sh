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

set -o errexit -o pipefail
echo "Running stitcher.sh"; echo

# servo control daemon
if [ $(ps aux | grep pigpiod | wc --lines) -gt 1 ]
then
  echo "pigpiod daemon already running!"
else
  sudo pigpiod
  echo "pigpiod activated!"
fi

# stitch ttyS10 and ttyS11 together
if [ $(ps aux | grep socat | wc --lines) -gt 1 ]
then
  echo "socat already running!"
else
  sudo socat PTY,link=/dev/ttyS10 PTY,link=/dev/ttyS11 &
  echo "socat started on ttyS10 & ttyS11!"
fi

# rotator control
# use EasyComm I protocol
if [ $(ps aux | grep rotctld | wc --lines) -gt 1 ]
then
  echo "rotctld already running!"
else
  sudo rotctld -m 201 -T 10.0.0.117 -vvvvv -r /dev/ttyS10 &> rotlog.log &
  echo "rotctld activated on ttyS10 with EasyComm I protocol!"
fi

echo
echo "Resources successfully stitched!"
exit 0