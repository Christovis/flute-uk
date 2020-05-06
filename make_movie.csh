

#  needs some tricks to find a format that MacOS can understand...

ffmpeg -framerate 5 -i ew_day%d_map.png -c:v libx264 -vf: scale=-2:720 -pix_fmt yuv420p  output.mp4
