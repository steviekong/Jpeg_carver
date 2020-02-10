import sys

def main():
	if len(sys.argv) < 2:
		print("Invalid input, you must specifiy a file as the first argument.")
		exit(0)
	readFile(sys.argv[1])

def readFile(filename):
	file = open(filename, 'rb')
	startMarker = 0
	endMarker = 0
	counter = 0
	while True:
		byteArray = file.read(4096)
		if findStart(byteArray):
			startMarker = counter
		if startMarker != 0:
			if findEnd(byteArray):
				endMarker = counter
		counter += 1
	print(startMarker, endMarker)
	buildFile(startMarker, endMarker, file)

def findStart(byteArray):
	print(bytearray.decode().length)
	if byteArray[0] == b'\xFF' and byteArray[1] == b'\xD8':
		return True
	return False

def findEnd(byteArray):
	if byteArray[4096] == b'\xFF' and byteArray[4097] == b'\xD9':
		return True
	return False

def buildFile(startMarker, endMarker, file):
	jpegBytes = bytes()
	file.seek(startMarker)
	while endMarker > 0:
		byte = file.read(1)
		jpegBytes.append(byte)
		endMarker -= 1
	jpegFile = open("outputfile.jpg", 'wb+')
	jpegFile.write(jpegBytes)
	


if __name__ == '__main__':
	main()