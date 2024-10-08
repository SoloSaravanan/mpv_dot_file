# vim: set ft=python:

# see the README at https://gist.github.com/phiresky/4bfcfbbd05b3c2ed8645
# source: https://github.com/mpv-player/mpv/issues/2149
# source: https://github.com/mpv-player/mpv/issues/566
# source: https://github.com/haasn/gentoo-conf/blob/nanodesu/home/nand/.mpv/filters/mvtools.vpy

import vapoursynth
import os

core = vapoursynth.core

#Load mvtools plugin
core.std.LoadPlugin(os.path.expanduser("~/.config/mpv/libmvtools.so"))
#Load FFMS2 plugins
core.std.LoadPlugin(os.path.expanduser("~/.config/mpv/libffms2.so.4"))

# ref: http://avisynth.org.ru/mvtools/mvtools2.html#functions
# default is 400, less means interpolation will only happen when it will work well
ignore_threshold=140
# if n% of blocks change more than threshold then don't interpolate at all (default is 51%)
scene_change_percentage=15

dst_fps = 72
# Interpolating to fps higher than 60 is too CPU-expensive, smoothmotion can handle the rest.
# while (dst_fps > 60):
#    dst_fps /= 2

if "video_in" in globals():
    # realtime
    clip = video_in
    # Needed because clip FPS is missing
    src_fps_num = int(container_fps * 1e8)
    src_fps_den = int(1e8)
    clip = core.std.AssumeFPS(clip, fpsnum = src_fps_num, fpsden = src_fps_den)
else:
    # run with vspipe
    clip = core.ffms2.Source(source=in_filename)
    dst_fps=float(dst_fps)

# Downscale to 1080p if the video is larger
if clip.width > 1920 or clip.height > 1080:
    clip = core.resize.Bicubic(clip, width=1920, height=1080)

# resolution in megapixels. 1080p ≈ 2MP, 720p ≈ 1MP
mpix = clip.width * clip.height / 1000000

# Skip interpolation for >1080p or 60 Hz content due to performance
if not (mpix > 2.5 or clip.fps_num/clip.fps_den > 59):
    analParams = {
        'overlap': 2,
        'search': 3,
        'truemotion': True,
        #'chrome': True,
        'blksize':16,
        #'searchparam':1
    }

    quality = 'high'
    dst_fps_num = int(dst_fps * 1e4)
    dst_fps_den = int(1e4)
    print("Reflowing from {} fps to {} fps (quality={})".format(clip.fps_num/clip.fps_den,dst_fps_num/dst_fps_den,quality))
    
    sup  = core.mv.Super(clip, pel=2)
    bvec = core.mv.Analyse(sup, isb=True, **analParams)
    fvec = core.mv.Analyse(sup, isb=False, **analParams)
    clip = core.mv.FlowFPS(clip, sup, bvec, fvec,
            num=dst_fps_num, den=dst_fps_den)

clip.set_output()
