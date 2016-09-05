""" 
    video_background.py
    M. Betz, 5.9.16

    An experiment in including hardware accelerated video backgrounds
    in Mission Pinball on the Raspberry Pi 2 and 3. It is a dirty but effective hack.
    
      1. This file is imported during init of mpf. Here we import hello_video.
      2. When the user wants to play a video, `hello_video` calls 
         the `hello_video.bin` application. It can __seamlesslys__
         loop .h264 video files on the Raspi grapical background layer
      3. We have to configure MPF-MC to have a transparent background window.
         So add `KivyWindow.clearcolor = (0, 0, 0, 0)` to mpfmc/uix/window.py
         Also use `background_color: 00000000` in the slide config (last 00 is alpha)
      4. The python library hello_video communicates with the player `hello_video.bin`
         via stdout. So it's possible to change the playing video on-the-fly.
      5. We listen to the MPF event `video_background_change`. See below for examples.
      6. .h264 files can be easily created with ffmpeg. See attached `convert_h264.sh`
         file for details
     
    ## Results
    
    1280x800 video in h264 format. RPI3. MPF v0.30.

          * With the kivy based slide player I get 100% CPU load on one core. Video stutters a lot.
            MPF becomes unresponsive.
          * With hello_video alone I get 4 % CPU load, together with MPF it's ~ 25 %. Video plays
            perfectly smooth.
     
     TODO: 
       * add `dimension` parameter, so video can be played within a specified rectangle
         __on top_ of the MPF slide player
       * Make sure `hello_video.bin` provides a black background when no video is playing.
         Else the terminal might shine through :o
"""

import sys, os, logging
sys.path.append( os.path.dirname(__file__) )
from mpf.core.scriptlet import Scriptlet
import hello_video

#from kivy.core.window import Window as KivyWindow


class VideoBackground(Scriptlet):
    """
        A video background can be triggered like this anywhere in the .yaml files:

            event_player:
              mode_attract_started:
                video_background_change:
                  fName: "/home/pi/mpf_machine/videos/AmazonSwamp.h264"

        Make sure that your slide has a transparent background:

            slides:
              intro_slide:
                background_color: 00000000
    """

    def on_load(self):
        self.log.info("Adding `helloVideoPlayer`")
        self.helloVideoPlayer = hello_video.HelloVideoPlayer()
        self.machine.events.add_handler('video_background_change', self.videoChangeCallback )

    def videoChangeCallback( self, *args, **kwargs ):
        """
        z: -1             sets z index to -1 (below MPF slides)
        fname: bla.h264   starts playing a h264 file
        stop:             stops playing (dominant)
        """
        if "stop" in kwargs:
            #KivyWindow.clearcolor = [0,0,0,1]
            self.helloVideoPlayer.stop()
            return
        if "fname" in kwargs:
            try:
                z = kwargs["z"]
            except:
                z = -1
            self.helloVideoPlayer.play( kwargs["fname"], True, z )
            #KivyWindow.clearcolor = [0,0,0,0]
