# Copyright 2015 Adafruit Industries.
# Author: Tony DiCola
# Modified: M. Betz
# License: GNU GPLv2, see LICENSE.txt
import os
import logging
import subprocess
import time

HF_NAME = os.path.join( os.path.dirname(__file__), './hello_video.bin' )

class HelloVideoPlayer(object):

    def __init__(self):
        """Create an instance of a video player that runs hello_video.bin in the
        background.
        """
        self.log = logging.getLogger("HelloVideoPlayer")
        self._process = None

    def play(self, fName, loop=False, layer=0, dimensions=None, **kwargs):
        """Play the provided .h264 movie file, optionally looping it repeatedly."""
        if self._process is not None:
            if self._process.poll() is not None:  #Process has terminated :(
                self._process = None
        if self._process is None:
            # Startup the player process. Assemble list of arguments.
            args = [HF_NAME, str(int(loop)), str(int(layer)) ]
            if dimensions is not None:
                if len(dimensions)==4:
                    for dim in dimensions:
                        args.append( int(dim) )
                else:
                    raise ValueError("dimensions must be [x, y, w, h]")
            args.append(fName)                # Add fName file path.
            # Run hello_video process and direct standard output to /dev/null.
            self.log.info("Playing: {0}".format(args) )
            #self._process = subprocess.Popen( args, stdin=subprocess.PIPE, stdout=open(os.devnull, 'wb'), stderr=subprocess.STDOUT, universal_newlines=True, close_fds=True )
            self._process = subprocess.Popen( args, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, close_fds=True )

        # Semaless switch of video
        st = self._process.stdin
        st.write( fName )
        st.flush()

    def stop(self):
        proc = self._process
        proc.kill()
        #if proc is not None and proc.poll() is None:
            #subprocess.call(['kill', '-9', str(proc.pid)])
        self._process = None

    def __delete__( self ):
        self.stop()
