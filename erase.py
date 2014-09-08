#!/usr/bin/python
#!python
import msr605
import sys
import re
import binascii

def _reverse_bits(value, nbits):
    return sum(
        1 << (nbits - 1 - i)
        for i in xrange(nbits)
        if (value >> i) & 1
    )

def main():
	try:
		reader = msr605.MSR605("/dev/tty.usbserial", test=False)
		reader.reset()
		reader.select_bpi(1,0,1)
		reader.set_hico()
		print 'swipe card to erase'
		while True:
			try:
				reader.reset()
				data = reader.erase_card()
				print 'card erased'
			except msr605.ReadError:
				print 'failed to erase'
			except msr605.ReadWriteError:
				print >> sys.stderr, 'ERROR: Could not erase card'
	except KeyboardInterrupt:
		print "Shutdown requested...exiting"
	sys.exit(0)

if __name__ == "__main__":
    main()