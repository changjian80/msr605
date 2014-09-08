#!/usr/bin/python
#!python
import msr605
import sys
import re
import binascii

def main():
    try:
		reader = msr605.MSR605("/dev/tty.usbserial", test=False)
		print 'swipe a card'
		while True:
			try:
				reader.reset()
				data = reader.read_raw()
				sdata = (data[0].rstrip('\x00'), data[1].rstrip('\x00'), data[2].rstrip('\x00'))
				print '------------------------------------------------------------'
				print 'track 1: ' + binascii.hexlify(sdata[0])
				print 'track 2: ' + binascii.hexlify(sdata[1])
				print 'track 3: ' + binascii.hexlify(sdata[2])
				print '------------------------------------------------------------'
			except msr605.ReadError:
				continue
			except msr605.ReadWriteError:
				print >> sys.stderr, 'ERROR: Could not read card'
    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    sys.exit(0)

if __name__ == "__main__":
    main()