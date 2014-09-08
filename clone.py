#!/usr/bin/python
#!python
import msr605
import sys
import re
import binascii

# write_raw does not seem to work correctly.
# This was recorded from the windows app.
# 1B6E1B73
#    Tk  LN  DA
# 1B 01  01  48
# 1B 02  01  A2
# 1B 03  01  1E
# 3F1C
# Write T1:123 T2:456 T3:789

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
		print 'Reader firmware: '+ reader.get_firmware_version()
		reader.select_bpi(1,0,1)
		reader.set_hico()
		data = []
		print 'swipe card to read'
		try:
			reader.reset()
			data = reader.read_raw()
			sdata = (data[0].rstrip('\x00'), data[1].rstrip('\x00'), data[2].rstrip('\x00'))
			print '------------------------------------------------------------'
			print 'track 1: ' + binascii.hexlify(sdata[0])
			print 'track 2: ' + binascii.hexlify(sdata[1])
			print 'track 3: ' + binascii.hexlify(sdata[2])
			print '------------------------------------------------------------'
			print 'swipe a card to write'
			reader.reset()
			reader.write_raw(*sdata)
			print 'Done!'
		except msr605.ReadError:
			return
		except msr605.ReadWriteError:
			print >> sys.stderr, 'ERROR: Could not write card'
	except KeyboardInterrupt:
		print "Shutdown requested...exiting"
	sys.exit(0)

if __name__ == "__main__":
    main()