#!/usr/bin/env python

"""A simple python script template.
"""

import serial
import TinyFrame as TF
import os
import sys
import time

TYPE_DEFAULT = 0x0000
TYPE_UART = 0x0001
TYPE_PERIPHERAL = 0x0002
TYPE_CENTRAL = 0x0003

def fallback_listener(frame):
    print("Fallback listener")
    print(frame)

def main(arguments):
    print("TinyFrame test sender")

    with serial.Serial('/dev/ttyUSB0', 115200, timeout=1) as ser:
        tf = TF.TinyFrame()
        tf.TYPE_BYTES = 0x02
        tf.CKSUM_TYPE = 'crc16'
        tf.SOF_BYTE = 0x55
        tf.write = ser.write
        # Add listeners
        tf.add_fallback_listener(fallback_listener)

        # send a frame
        tf.send(TYPE_CENTRAL, b"Hi Central")
        time.sleep(1)
        tf.send(TYPE_PERIPHERAL, b"Hi Peripheral")
        time.sleep(1)
        tf.send(TYPE_UART, b"Hi UART\n")
        time.sleep(1)

        #line = ser.readline()   # read a '\n' terminated line
        #tf.accept(line)
    

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))