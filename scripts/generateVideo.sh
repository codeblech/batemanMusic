#!/bin/bash
echo "I have to return some videotapes..."

# Use the first argument as the path to background image
bgImagePath=$1

# Check if bgImagePath is not empty
if [[ -z "$bgImagePath" ]]; then
    read -p "path to background image: " bgImagePath
fi

# To get the current time in the format Hour:Minute:Second
currentTime=$(date +"%H-%M-%S")

batemanVideoPath="./assets/bateman_final.mp4"
currentTime=$(date +"%H-%M-%S")
outputFileName="out_$currentTime.mp4"

callFFMPEG() {
    ffmpeg -i "$bgImagePath" -i "$batemanVideoPath" -filter_complex \
    "[1:v]colorkey=0x00C04C:0.2:0.1[keyed];[0:v][keyed]overlay" \
    ./outputs/$outputFileName
}

callFFMPEG $bgImagePath "./assets/bateman_final.mp4"