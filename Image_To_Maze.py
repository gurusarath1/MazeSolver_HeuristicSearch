from PIL import Image
import numpy as np

fileImg = input('Image File name ? ')

if fileImg:
	im = Image.open( fileImg, 'r')
else:
	im = Image.open( 'Maze.jpg', 'r')

width, height = im.size
print(height, width)
pix_val = list(im.getdata())

RowOptimize = True

def distance_from_black_white(pxl):
	distance_from_black = ((0 - pxl[0])**2 + (0 - pxl[1])**2 + (0 - pxl[2])**2)**0.5
	distance_from_white = ((255 - pxl[0])**2 + (255 - pxl[1])**2 + (255 - pxl[2])**2)**0.5
	return (distance_from_black, distance_from_white)

k = 0
pic_2D_List =[]
imageMapString = ""
prevRow = [2]
for i in range(height):
	rowX = []
	rowXString = ""
	for j in range(width):
		rowX.append(pix_val[k])
		BW = distance_from_black_white(pix_val[k])

		if BW[0] > BW[1]:
			rowXString = rowXString + " "
		else:
			rowXString = rowXString + "X"
		k += 1

	if rowX != prevRow:
		imageMapString += rowXString + "\n"
		pic_2D_List.append(rowX)
	elif not RowOptimize:
		imageMapString += rowXString + "\n"
		pic_2D_List.append(rowX)
	else:
		pass


	prevRow = rowX
	


fileX = open('Maze.txt','w')
fileX.write(imageMapString)
fileX.close()