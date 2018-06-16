"""
Class definition for running rotator interface.
Utilizing class to limit scope of state variables

author: Marion Anderson
date:   2018-06-15
file:   controller.py
"""
from __future__ import absolute_import, print_function

import os
import time


class ControllerClassException(Exception):
    """Provide exceptions for Controller class."""
    pass


class Controller(object):
    """Object that handles running of mySatComm/cmd-n-ctl"""

    def __init__(self):
        self.stitched = False
        self.running = False

    def stitch(self):
        """Stitch system resources together"""
        # make sure this hasn't been run before
        if self.stitched:
            raise ControllerClassException('Resources already stitched!')

        # stitch resources
        ret = os.system('./stitcher.sh')
        if ret >> 8 != 0:
            raise ControllerClassException('Failed to stitch resources!')
        self.stitched = True

    def unstitch(self):
        """Unstitch system resources."""
        # make sure system is stitched first
        if not self.stitched:
            raise ControllerClassException('Resources not stitched!')

        # unstitch resources
        ret = os.system('./unstitcher.sh')
        if ret >> 8 != 0:
            raise ControllerClassException('Failed to stitch resources!')
        self.stitched = False

    def run(self):
        """Run controller interface."""
        # stitch system if it isn't already
        if not self.stitched:
            self.stitch()

        # create "go" flag file for rotator interface
        with open('~/.satcomm_runflag_delete2stop', 'w') as f:
            f.write('')
        # start interface
        ret = os.system('./interface.py &')
        if ret >> 8 != 0:
            raise ControllerClassException('Failed to run interface!')
        self.running = True

    def stop(self):
        """Stops controller interface."""
        # remove "go" flag file to stop
        os.remove('~/.satcomm_runflag_delete2stop')
        self.running = False
        time.sleep(0.55)
        self.unstitch()
