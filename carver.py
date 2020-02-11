import sys
import os
import random 
from PIL import Image

def main():
	if len(sys.argv) < 2:
		print("Invalid input, you must specifiy a file as the first argument.")
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
			if findSOS(byte1, byte2):
				sosArr.append(counter)
			counter += 2
			byte1 = file.read(1)
			byte2 = file.read(1)
	print("Found markers")
	pairs = findPairs(startMarkerArr, endMarkerArr, sosArr)
	buildFile(pairs)
#Finds EIO
def findStart(byte1, byte2):
	if byte1 == b'\xFF' and byte2 == b'\xD8':
		return True
	return False
#Finds SOI
def findEnd(byte1, byte2):
	if byte1 == b'\xFF' and byte2 == b'\xD9':
		return True
	return False

def findSOS(byte1, byte2):
	if byte1 == b'\xFF' and byte2 == b'\xDA':
		return True
	return False
#Creates the pairs of SOI and EOI markers 
def findPairs(startMarkerArr, endMarkerArr, sosArr):
	markerPairs = []
	for startI in range(0, len(startMarkerArr)):
		for endI in range(0, len(endMarkerArr)):
			if startMarkerArr[startI] < endMarkerArr[endI] + 2:
				markerPairs.append((startMarkerArr[startI], endMarkerArr[endI]))
				#for sosI in range(0, len(sosArr)):
					#if sosArr[sosI] > startMarkerArr[startI] and sosArr[sosI] < endMarkerArr[endI]:
						#markerPairs.append((startMarkerArr[startI], endMarkerArr[endI]))
	print("Found pairs size is " + str(len(markerPairs)))
	return markerPairs

#Tests all pairs and deletes invalid images using Pillow/ PIL
def buildFile(markerPairs):
	file = open(sys.argv[1], 'rb')
	byteBuffer = file.read()
	counter = 0
	while counter < len(markerPairs):
		jpegBytes = bytearray()
		start = markerPairs[counter][1]
		jpegBytes.extend(byteBuffer[markerPairs[counter][0]:markerPairs[counter][1]+2])
		print("Image size is " + str(len(jpegBytes)))
		name = str(random.random())
		jpegFile = open(name + ".jpg", 'wb+')
		jpegFile.write(jpegBytes)
		try:
			Image.open(name + ".jpg")
		except IOError:
			os.remove(name + ".jpg")
			print("Invalid image removed")
		counter += 1


if __name__ == '__main__':
	main()