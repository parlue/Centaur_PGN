#!/usr/bin/env python
"""
This script opens two serial ports, specified with arguments 1 and 2
on the command line.  It forwards data between the two serial ports as if it's
just a wire. So the CEntaurboard and picohess could communicate internal

Usage: ./serial-loopback.py /dev/ttyUSB0 /dev/ttyUSB1
"""

import sys
import os
import serial
import select

class SerialProxy(serial.Serial):

    def __init__(self, device, baudrate, quiet = 0):

        self.device = device
        self.dest = None
        timeout = 0.1
        self.quiet = quiet

        super(SerialProxy, self).__init__(port=device, baudrate=baudrate, timeout=timeout)

    def handle_read(self):
        data = os.read(self.fileno(), 1024)

        if not self.dest:
                return

        if not self.quiet:
            print '{0}->{1}: [{2:02}] {3} "{4}"'.format(self.port, self.dest.port, len(data), type(data), data)

        os.write(self.dest.fileno(), data)

    def handle_write(self):
        print "Handle write called for ", self

    def handle_error(self):
        print "Handle ERROR called for ", self

    def set_dest(self, dest):
        self.dest = dest
#
# Script starts execution here
#
if __name__ == '__main__':

    daemonize = False

    if "-d" in sys.argv:
        daemonize = True
        sys.argv.pop(sys.argv.index("-d"))

    if (len(sys.argv) < 3):
        print "FAIL:\tNeed 2 serial devices for arguments, optional 3rd argument is baudrate"
        print "FAIL:\tUsage:", sys.argv[0], "[-d] DEV1 DEV2 [BAUDRATE1 [BAUDRATE2]]"
        sys.exit(1)

    baud = 9600
    baud1 = baud
    baud2 = baud

    if (len(sys.argv) >= 4):
        try:
            baud1 = int(sys.argv[3])
        except:
            print "WARN:\tfailed to parse baudrate"
            pass

    if (len(sys.argv) == 5):
        try:
            baud2 = int(sys.argv[4])
        except:
            print "WARN:\tfailed to parse baudrate"
            pass

    dev1 = SerialProxy(device=sys.argv[1], baudrate=baud1, quiet=daemonize)
    dev2 = SerialProxy(device=sys.argv[2], baudrate=baud2, quiet=daemonize)

    dev1.set_dest(dev2)
    dev2.set_dest(dev1)

    read_map = {}
    write_map = {}
    error_map = {}

    read_map[dev1] = dev1.handle_read
    read_map[dev2] = dev2.handle_read

    # Mostly unused
    #write_map[dev1] = dev1.handle_write
    #write_map[dev2] = dev2.handle_write
    error_map[dev1] = dev1.handle_error
    error_map[dev2] = dev2.handle_error

    # Fork
    try:
        if daemonize:
            pid = os.fork()
            if pid > 0:
                f = open('/var/run/serial-proxy.pid', 'w')
                f.write(str(pid))
                f.close()
                sys.exit(0) # Exit parent.
    except OSError, e:
        sys.stderr.write("fork failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)

    run = True
    while run:
        try:
            #readers, writers, errors = select.select(read_map.keys(), write_map.keys(), error_map.keys(), 5)
            readers, writers, errors = select.select(read_map.keys(), [], error_map.keys(), 5)
        except select.error, err:
            if err[0] != EINTR:
                raise

        for reader in readers:
            read_map[reader]()
        for writer in writers:
            write_map[writer]()
        for error in errors:
            error_map[error]()