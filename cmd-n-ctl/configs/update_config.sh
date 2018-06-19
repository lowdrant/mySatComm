#! /usr/bin/env bash
#
# Provides interface to update rotator_config.json
# Literally copies it to ~/.satcomm/include
#
# author: Marion Anderson
# date:   2018-06-19
# file:   update_config.sh

set -o errexit -o nounset -o pipefail
cp rotator_config.json ~/.satcomm/include/
exit 0
