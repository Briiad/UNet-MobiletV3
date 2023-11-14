import serial
import time

arduino = serial.Serial('/dev/ttyACM0', 115200)

while True:
  # keyboard input
  key = input()

  # send the character to the device
  arduino.write(key.encode())

  # wait for the device to send the character back
  time.sleep(0.1)

  # read the character from the device
  # note that I'm reading for only 1 byte, adjust as needed
  data = arduino.read(1)

  # display the received data in terminal
  print(data.decode('ascii'))

arduino.close()