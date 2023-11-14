import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 115200)

try:
    while True:
        data = input()
        arduino.write(data.encode())
        print(data.decode('ascii'))
        time.sleep(0.1)
except KeyboardInterrupt:
    print('Close Serial Connection')
finally:
    arduino.close()