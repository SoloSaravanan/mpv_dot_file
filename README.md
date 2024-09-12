# mpv_dot_file
mpv with realtime frame interpolation

```
git clone https://github.com/SoloSaravanan/mpv_dot_file ~/.config/mpv
```

# Encoding video to a higher framerate

Run this:
```
vspipe --arg in_filename=input.mkv --arg display_fps=60 --y4m ~/.config/mpv/motioninterpolation.vpy -|ffmpeg -i - -crf 18 output.mkv
```

Refs: <br>
https://gist.github.com/phiresky/4bfcfbbd05b3c2ed8645 <br>
https://github.com/cyl0/ModernX/ <br>
https://github.com/dubhater/vapoursynth-mvtools
