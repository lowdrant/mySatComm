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

# stitch resources
stitcher.sh

# begin interfacing
interface.py

# cleanup
unstitcher.sh
