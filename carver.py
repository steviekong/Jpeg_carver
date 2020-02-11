import sys
import os
import random 
from PIL import Image

'''
Simple image carver. Right now it will assemble any and all JPEGS found including partial fragmented files.
You must have pillow installed. You can do that by `pip install pillow`.

YOU MUST HAVE PYTHON 3 NOT 2! THE Pillow version used is 3 and I can't guarantee any of this works on python 2.
'''
def main():
	if len(sys.argv) < 2:
		print("Invalid input, you must specify a file as the first argument.")
		exit(0)
	readFile(sys.argv[1])
# Reads file and creates the list of SOI AND EOI markers
def readFile(filename):
	startMarkerArr = []
	endMarkerArr = []
	sosArr = []
	counter = 0
	fileSize = os.stat(filename).st_size
	with open(filename, 'rb') as file:
		byte1 = file.read(1)
		byte2 = file.read(1)
		while counter <= fileSize:
			if findStart(byte1, byte2):
				startMarkerArr.append(counter)
			if findEnd(byte1, byte2):
				endMarkerArr.append(counter)
			counter += 2
			byte1 = file.read(1)
			byte2 = file.read(1)
	print("Found markers")
	pairs = findPairs(startMarkerArr, endMarkerArr, sosArr)
	validCount = buildFile(pairs)
	print("Total number of valid images found are " + str(validCount))

#Finds SOI
def findStart(byte1, byte2):
	if byte1 == b'\xFF' and byte2 == b'\xD8':
		return True
	return False
#Finds EOI
def findEnd(byte1, byte2):
	if byte1 == b'\xFF' and byte2 == b'\xD9':
		return True
	return False

#Creates the pairs of SOI and EOI markers 
def findPairs(startMarkerArr, endMarkerArr, sosArr):
	markerPairs = []
	for startI in range(0, len(startMarkerArr)):
		for endI in range(0, len(endMarkerArr)):
			if startMarkerArr[startI] < endMarkerArr[endI] + 2:
				markerPairs.append((startMarkerArr[startI], endMarkerArr[endI]))
	print("Found pairs list size is " + str(len(markerPairs)))
	return markerPairs

#Tests all pairs and tests/ deletes invalid images using Pillow/ PIL
def buildFile(markerPairs):
	file = open(sys.argv[1], 'rb')
	byteBuffer = file.read()
	validCount = 0
	counter = 0
	while counter < len(markerPairs):
		jpegBytes = bytearray()
		start = markerPairs[counter][1]
		jpegBytes.extend(byteBuffer[markerPairs[counter][0]:markerPairs[counter][1]+2])
		name = str(random.random())
		jpegFile = open(name + ".jpg", 'wb+')
		jpegFile.write(jpegBytes)
		try:
			Image.open(name + ".jpg")
		except IOError:
			os.remove(name + ".jpg")
			print("Invalid image removed")
		else:
			validCount += 1
			print("File saved, the size is " + str(len(jpegBytes)))
		counter += 1
	return validCount

if __name__ == '__main__':
	main()