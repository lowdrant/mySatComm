#!/usr/bin/env bash
#
# This file "stitches" together the resources needed to interface with hamlib
# Intended only for experimentation/learning. There are are a number of
# hardcoded and bad code practices here that are not nearly robust enough to
# run on a given setup without some assembly and sudo access
#
# author: Marion Anderson
# date:   2018-06-12
# file:   stitcher.sh

set -o errexit
set -o pipefail
echo "Running stitcher.sh"

# servo control daemon
if [ $(ps aux | grep pigpiod | wc --lines) -gt 1 ]
then
  echo "  pigpiod daemon already running"
else
  sudo pigpiod
  echo "  pigpiod activated"
fi

# stitch custom serial ports together
if [ $(ps aux | grep socat | wc --lines) -gt 1 ]
then
  echo "  socat already running"
else
  sudo socat PTY,link="$HOME/.satcomm/ttySatT",user="$USER"\
             PTY,link="$HOME/.satcomm/ttySatR",user="$USER" &
  echo "  socat started"
fi

# rotator control
# use EasyComm I protocol
if [ $(ps aux | grep rotctld | wc --lines) -gt 1 ]
then
  echo "  rotctld already running"
else
  sudo rotctld -m 201 -T "raspberrypi.local" -vvvvv -r "$HOME/.satcomm/ttySatT" &> rotlog.log &
  echo "  rotctld activated using EasyComm I protocol"
fi

echo "Resources successfully stitched"
exit 0
