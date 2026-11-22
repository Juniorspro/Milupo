#!/bin/bash
# Arma el video de un idioma: imagen (montar.py) + audio (mezcla.py) → MP4 para TikTok (1080x1920, 30 fps, H.264 + AAC)
set -e
L=$1
cd "$(dirname "$0")"
venv/bin/python mezcla.py $L
venv/bin/python montar.py $L
mkdir -p /home/user/Milupo/trailers
MAYUS=$(echo $L | tr a-z A-Z)
ffmpeg -y -v error -i video_$L.mp4 -i mezcla_$L.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -ar 48000 -shortest -movflags +faststart \
  -metadata title="Dragon Rider - Trailer ($MAYUS)" /home/user/Milupo/trailers/DragonRider_Trailer_$MAYUS.mp4
echo "listo: /home/user/Milupo/trailers/DragonRider_Trailer_$MAYUS.mp4"
