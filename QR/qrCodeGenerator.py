import pyqrcode
import getopt
from pyqrcode import QRCode
import sys

def main(argv):
	color = None
	try:
		opts, args = getopt.getopt(argv,"c:",["color="])
	except getopt.GetoptError:
		sys.exit(2)
	for opt, arg in opts:
		if opt in ('-c', '-color'):
         		color = arg

	url = pyqrcode.create(color)
	url.png(color + '.png', scale = 6)

if __name__ == "__main__":
   main(sys.argv[1:])
