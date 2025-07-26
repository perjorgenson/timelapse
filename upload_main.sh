#!/bin/bash

PORT="/dev/ttyUSB0"
FILE="main.py"

if [ ! -f "$FILE" ]; then
  echo "Error: File '$FILE' not found!"
  exit 1
fi

echo "Uploading $FILE to ESP32 on $PORT..."
mpremote connect "$PORT" fs cp "$FILE" : || { echo "Upload failed"; exit 1; }

echo "Upload completed successfully."
