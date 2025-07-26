#!/bin/bash

# Config
ESP32_IP="192.168.0.170"  # <-- Replace with the actual IP of your ESP32-CAM
OUTPUT_DIR="$HOME/devel/timelapse/outputs"
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
FILENAME="photo_${TIMESTAMP}.jpg"

# Ensure output directory exists
mkdir -p "$OUTPUT_DIR"

# Fetch the image
echo "Requesting image from ESP32-CAM at $ESP32_IP..."
curl -s "http://$ESP32_IP/capture" --output "$OUTPUT_DIR/$FILENAME"

# Check if the file was saved and is non-empty
if [ -s "$OUTPUT_DIR/$FILENAME" ]; then
    echo "Saved image as $OUTPUT_DIR/$FILENAME"
else
    echo "Failed to capture image. File is empty or download failed."
    rm -f "$OUTPUT_DIR/$FILENAME"
fi
