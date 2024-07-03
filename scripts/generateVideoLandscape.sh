#!/bin/bash

# Use the first argument as the path to background image
bgImagePath=$1

# Check if bgImagePath is not empty
if [[ -z "$bgImagePath" ]]; then
    read -p "path to background image: " bgImagePath
fi

# To get the current time in the format Hour:Minute:Second
currentTime=$(date +"%H-%M-%S")

batemanVideoPath="./assets/bateman_original.mp4"
outputFileName="out_$currentTime.mp4"
outputFilePath="./outputs/$outputFileName"
# create directory if it doesn't exist already
[ -d "./outputs" ] || mkdir -p "./outputs"

callFFMPEG() {
    ffmpeg -i "$bgImagePath" -i "$batemanVideoPath" -filter_complex \
    "[0:v]scale=1920:1080[bg];[1:v]colorkey=0x00C04C:0.2:0.1[keyed];[bg][keyed]overlay" \
    $outputFilePath
}

callFFMPEG

# Print the path to the generated video file
echo "$outputFilePath"