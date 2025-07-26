import network
import socket
import camera
import time
import gc

SSID = 'your_ssid'
PASSWORD = 'your_password'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to WiFi...")
        wlan.connect(SSID, PASSWORD)
        retry = 0
        while not wlan.isconnected() and retry < 20:
            time.sleep(1)
            retry += 1
    if wlan.isconnected():
        print("Connected! IP:", wlan.ifconfig()[0])
        return wlan.ifconfig()[0]
    else:
        print("Failed to connect to WiFi.")
        return None

def take_photo(filename):
    try:
        camera.init()
        img = camera.capture()
        if img:
            f = open(filename, 'wb')
            f.write(img)
            f.close()
            print("Image saved as:", filename)
        else:
            print("Failed to capture image.")
        camera.deinit()
        gc.collect()
    except Exception as e:
        print("Camera error:", e)

def start_server(ip):
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print("HTTP server running at http://{}/capture".format(ip))

    while True:
        try:
            cl, addr = s.accept()
            print("Client:", addr)
            req = cl.recv(1024)
            if b"GET /capture" in req:
                filename = "photo.jpg"
                take_photo(filename)
                try:
                    f = open(filename, 'rb')
                    img = f.read()
                    f.close()
                    cl.send(b"HTTP/1.1 200 OK\r\n")
                    cl.send(b"Content-Type: image/jpeg\r\n")
                    cl.send(b"Content-Length: %d\r\n" % len(img))
                    cl.send(b"Connection: close\r\n\r\n")
                    cl.send(img)
                    print("Photo sent.")
                except Exception as e:
                    cl.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nCould not read image.")
                    print("File send error:", e)
            else:
                cl.send(b"HTTP/1.1 404 Not Found\r\n\r\nEndpoint not found.")
            cl.close()
        except Exception as e:
            print("Request error:", e)
            try:
                cl.close()
            except:
                pass
            gc.collect()

def main():
    ip = connect_wifi()
    if ip:
        start_server(ip)
    else:
        print("Network unavailable. Halting.")

main()
