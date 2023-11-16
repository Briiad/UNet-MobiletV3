import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

try:
    while True:
        data = str(input())
        arduino.write(data.encode())
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Close Serial Connection')
finally:
    arduino.close()