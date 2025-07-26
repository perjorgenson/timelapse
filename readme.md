# ESP32 Cam Timelapse
To set up the environment for this repo, run `./bootstrap.sh` and then `source .venv/bin/activate`.
## USB-Serial Port For Programming
Dev environment is WSL(2), along with a Sparkfun FTDI Basic USB-Serial adapter.
This uses 3.3V for logic levels, and the 3v3 output does not provide enough 
current for the ESP32 and would have to bypass the voltage regulator if it was
used which might cause issues. I'm providing 5V to the ESP32 with a different 
source. 

To use a USB-Serial adapter with WSL, you need to follow the instructions here:

https://devblogs.microsoft.com/commandline/connecting-usb-devices-to-wsl/

Some things in the above instructions might be old, e.g. the command `usbipd wsl list` is old

Relevant commands to run in Windows Command Prompt (must run as admin): 


List out USB devices:

```
usbipd list
```

Share the USB serial converter for the first time:
```
usbipd bind --busid <busid>
```

Attach the serial converter to WSL:
```
usbipd attach --wsl --busid <busid>
```


Detach the serial converter from WSL (I didn't really use this):

```
usbipd detach --wsl --busid <busid>
```

> Occasionally the `usbipd attach` command will fail with the error  `usbipd: error: Loading vhci_hcd failed.`. I've been able to fix this by running `sudo modprobe vhci_hcd` from WSL first, and then retrying `attach`.

in WSL it shows up as `/dev/ttyUSB0` for me

## Flashing MicroPython
This will flash it with `firmware.bin`, which is a fork of MicroPython that supports 
the OV2640 camera sensor on the ESP32 Cam. 

https://github.com/Lennyz1988/micropython

specifically this release: https://github.com/Lennyz1988/micropython/releases/tag/v1
(I think)


### Hardware Configuration:
```
Programmer/Power Supply      ESP32 CAM Board
_____________________________________
Power Supply 5V--------------5V Input
Power Supply GND------------ GND

USB Serial Adapter GND-------GND
USB Serial Adapter Tx--------Rx
USB Serial Adapter Rx--------Tx
                             GPIO0---| (Jump to GND for programming)
                             GND-----|
```

### Steps
1. Connect up the ESP 32 CAM to a 5V power supply and the USB serial programmer
2. Connect GPIO0 to ground (labeled IO0 on my board)
3. Run  `./flash_esp32.sh` from the terminal
4. Press the "Reset" button on the ESP32 CAM board
5. Once flashing is complete, remove the jumper from GPIO0 and GND
6. Power cycle the board

Once this is complete, confirm that MicroPython is usable by getting a REPL prompt by
running the command `mpremote` from the terminal. You should be able to interact with
the MicroPython interpreter like below, where I print out "Hello" to the terminal.
```
(.venv) per@Per-XPS:~/devel/timelapse$ mpremote
Connected to MicroPython at /dev/ttyUSB0
Use Ctrl-] or Ctrl-x to exit this shell
print("HELLO")
HELLO
```

use ctrl+x to exit.

## Testing Main Program
The main file can be run on the ESP32 without saving it to the file system by running
```
mpremote run main.py
```
You should get an output like
```
I (116240) phy: phy_version: 4007, 9c6b43b, Jan 11 2019, 16:45:07, 0, 2
Connecting to WiFi...
Connected! IP: 192.168.0.170
HTTP server running at http://192.168.0.170/capture
```

This shows that the ESP32 camera has sucessfully connected to your WiFi. Go to the 
url that is printed out, and the ESP32 will take a picture and send it to your
browser window. 

The server will need to manually restarted every time with this method.


## Uploading Main Program
To make the main program run permanently, run the script

```
./upload_main.sh
```
This will make the main program run on boot.

At this point, the programming cable is no longer needed. It just needs to be powered.

## Network Configuration
To prevent the IP address of the ESP32 from changing, go into your local router
management page and assign it a static IP. The menu for mine was under
Network/DHCP Server/Address Reservation, where I was able to see the IP adress
of the "espressif" device. I then set a reserved IP address for it.

## Timelapse Photo Capture
To turn this boring old camera into a remote timelapse camera, a client device will
periodically connect to it and download an image. In my case, I have a mini computer
sitting in a closet that runs a cronjob every hour. This conjob runs the `fetch_photo.sh`
script, which saves a jpg file with a timestamp to a specified folder. 


To do this:
1. Put the `fetch_photo.sh` script onto the client machine (in my case the minicomputer). A simple way to do this is to just clone this repo to that machine.
2. Edit the crontab file with `crontab -e`
3. Add a line that points to the path of the `fetch_photos` script, and specifies the frequency that you want it to be run. In this case I'm running it on the first minute of every hour
```
0 * * * * /home/per/devel/timelapse/fetch_photo.sh
```
The `fetch_photos.sh` script should have the following lines edited to match your desired
setup:
```bash
ESP32_IP="192.168.0.140"  # <-- Replace with the actual IP of your ESP32-CAM
OUTPUT_DIR="$HOME/esp32_photos"
``` 

You may want to temporarily increase the frequency of the timelapse photos
being take to make sure that it's working correctly. Replace the first `0` with `*` to make it take a photo every minute.

## Timelapse Video Construction
Assuming that the the cronjob is working away and periodically saving .jpg photos
to a folder, you can stitch the photos together into a timelapse video with the `make_timelapse.py` python script.

The last line in the file should be changed to point to the path of your input
and output files.

```# create_timelapse("/path/to/images", "my_timelapse.mp4", fps=30)```



# Troubleshooting
### Software
- Are you in the virtual environment?
- Are you in WSL?
- Are you on the correct machine for the step of the tutorial?
- Have you run bootstrap?


### Hardware
In the REPL with mpremote, 
```python
>>> import camera
>>> camera.init()
```
this should give you some output about the GPIO configuration like 
```
I (30320) gpio: GPIO[32]| InputEn: 0| OutputEn: 1| OpenDrain: 0| Pullup: 0| Pulldown: 0| Intr:0 
I (30400) gpio: GPIO[35]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30400) gpio: GPIO[34]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30410) gpio: GPIO[39]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30420) gpio: GPIO[36]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30430) gpio: GPIO[21]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30430) gpio: GPIO[19]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30440) gpio: GPIO[18]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30450) gpio: GPIO[5]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30460) gpio: GPIO[25]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30470) gpio: GPIO[23]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30480) gpio: GPIO[22]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:0 
I (30490) camera: Allocating 1 frame buffers (234 KB total)
I (30530) camera: Allocating 234 KB frame buffer in OnBoard RAM
E (30560) gpio: gpio_install_isr_service(394): GPIO isr service already installed
True
```
Ignore the GPIO isr error, it didn't seem to cause any issues. This might hang, for
a little bit, which is a sign of an issue. 

Then run 
```python
img = camera.capture()
```
If this hangs forever, then there is definitely a problem. I was able to fix this by
1. Remove power from the ESP32 board
1. Carefully flip open the camera ribbon cable connector on the ESP32 board
2. Pull out, and then firmly reseat the cable
3. Close the clamp-connector for the ribbon cable
4. Repower the board, and run the above trouble shooting steps in the REPL again

If the camera is running, you should be able to get this output:
```
>>> img = camera.capture()
>>> img
b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01......(and a whole lot more binary data)'
```

# 