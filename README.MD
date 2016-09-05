# Mission Pinball Video Backgrounds

M. Betz, 9/16

An experiment in including hardware accelerated video backgrounds
in Mission Pinball on the Raspberry Pi 2 and 3. A dirty but effective hack.

## Installation

  1. Add `KivyWindow.clearcolor = (0, 0, 0, 0)` to `mpfmc/uix/window.py`
     This will make your MPF slide window have a transparent background,
     so videos can be played below it.

  2. Copy the `scriptlets` folder to your mpf machine folder.

  3. Include the scriptlet in your config.yaml like so:

     ```yaml
     scriptlets: video_background.VideoBackground
     ```

## Usage

The player listens to the MPF event `video_background_change`.
To play a video you can do this for example:
     
    ```yaml
    event_player:
      mode_attract_started:
        video_background_change:
          fName: "<path+filename>.h264"
          z: -1             # sets z index to -1 (below MPF slides)
          #stop: True       # stops playing
    ```
    
Also make sure that your slide has a transparent background:

    ```yaml
        slides:
          intro_slide:
            background_color: 00000000
    ```
    
## How it works    
    
  1. `./scriptlets/video_background.py` and `hello_video.py` are 
     imported during init of mpf.
  2. When the user wants to play a video, `hello_video.py` calls 
     the `hello_video.bin` application. It can __seamlesslys__
     loop .h264 video files on the Raspi grapical background layer
  3. We have to configure MPF-MC to have a transparent background window.
     So add `KivyWindow.clearcolor = (0, 0, 0, 0)` to mpfmc/uix/window.py
     Also use `background_color: 00000000` in the slide config (last 00 is alpha)
  4. The python library `hello_video` communicates with the player `hello_video.bin`
     via stdout. So it's possible to change the playing video seamlessly and without
     blackouts or glitches. This is the advantage over omxplayer.
  5. We listen to the MPF event `video_background_change`. See below for examples.
  6. .h264 files can be easily created with ffmpeg. See attached `convert_h264.sh`
     file for details
     
## Results

1280x800 video in h264 format. RPI3. MPF v0.30.

  * With the kivy based slide player I get 100% CPU load on one core. Video stutters a lot.
    MPF becomes unresponsive.
  * With hello_video alone I get 4 % CPU load, together with MPF it's ~ 25 %. Video plays
    perfectly smooth.
 
## TODO
   * Support the MPF asset manger to get the .h264 file names.
   * add `dimension` parameter, so video can be played within a specified rectangle
     __on top_ of the MPF slide player
   * Make sure `hello_video.bin` provides a black background when no video is playing.
     Else the terminal might shine through :o
