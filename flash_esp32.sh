#!/bin/bash

PORT="/dev/ttyUSB0"
BIN="firmware.bin"
ADDRESS="0x1000"

if [ ! -f "$BIN" ]; then
  echo "Error: Firmware file '$BIN' not found!"
  exit 1
fi

echo "Erasing flash on $PORT..."
esptool --chip esp32 --port "$PORT" erase-flash || { echo "Erase failed"; exit 1; }

echo "Flashing $BIN to $PORT at $ADDRESS..."
esptool --chip esp32 --port "$PORT" write-flash -z "$ADDRESS" "$BIN" || { echo "Flash failed"; exit 1; }

echo "Flash completed successfully."
