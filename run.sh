#!/usr/bin/env bash
#
# Run script for antenna rotation
#
# Author: Marion Anderson
# Date:   2018-07-06
# File:   run.sh


# leave out `set -o errexit` so C-c during interfacing
# leads directly to unstitcher
set -o nounset -o pipefail

# activate venv
source "$HOME/.satcomm/bin/activate"

# stitch resources
stitcher.sh

# begin interfacing
simple_interface.py

# cleanup
unstitcher.sh
