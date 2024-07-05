#!/bin/bash

FILE_PATH="$HOME/.spotify_dl_settings"

CONTENT='{
  "output": "./audio",
  "verbose": "false",
  "skip_mp3": "true"
}'

echo "$CONTENT" > "$FILE_PATH"
