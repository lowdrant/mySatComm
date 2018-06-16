#!/usr/bin/env bash
#
# Test script for interface.py
# runs interface.py, but not to the full intended autonomy
#
# MUST be run in same directory as interface.py
#
# author: Marion Anderson
# date:   2018-06-15
# file:   test_interface.sh

set -o pipefail -o errexit

if ! [ -e "interface.py" ]; then
    echo "Must be run in same directory as interface.py!"
    exit 1
fi

# activate venv
source ../satcomm/bin/activate
echo "Activated virtual environment!"

# stitch resouces
exec stitcher.sh

# create file flag for interface.py
touch "~/satcomm_runflag_delete2stop"

# run interface.py
./interface.py
