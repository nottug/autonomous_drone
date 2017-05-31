# utility functions for simplifying the calculations and deciding what actions to take

import cv2
from dict_digger import dig

img_center = (0,0)
ideal_area = 15000

median = 1680

# find the center of the bounding box and compare to the image center
def process_center(center):
	x0, y0 = center[0], center[1]
	x1, y1 = img_center[0], img_center[1]

	yaw = 1500
	throt = median

	# if person is left, move left, right, move right, center, don't move
	if x1 > x0:
		yaw = 1650
	elif x1 < x0:
		yaw = 1350
	else:
		yaw = 1500

	# if drone is high, move down, if low, move up, if center, don't move
	if y1 > y0:
		throt = 1560
	elif y1 < y0:
		throt = 1800
	else:
		throt = median

	return yaw, throt

# use the area to determine the distance from human
def process_area(area):
	pitch = 1500
	if area < ideal_area:
		pitch = 1400
	print(area)
	return pitch

# process the data from the network and convert into arrays
def process_data(out, width, height):
	conf = []
	labels = []
	bounds = []
	temp = True

	# sort through output dictionary and use relevant information
	for i in range(len(out)):
		label = dig(out[i], 'label')
		if label == 'person':
			conf.append(dig(out[i], 'confidence'))
			bounds.append(((dig(out[i], 'topleft', 'x'), dig(out[i], 'topleft', 'y')), 
				(dig(out[i], 'bottomright', 'x'), dig(out[i], 'bottomright', 'y'))))
			labels.append('person')
			temp = False
	
	# if no person is detected, stay at same position
	if temp:
		return median, 1500, 1500


	# calc centers/area of images/boxes
	box_center = (int((bounds[0][0][0]+bounds[0][1][0])/2), int((bounds[0][0][1]+bounds[0][1][1])/2))
	area = abs((bounds[0][0][0]-bounds[0][1][0]) *(bounds[0][0][1]-bounds[0][1][1]))
	img_center = (int(width/2), int(height/2))

	# calculate the necessary movements
	yaw, throt = process_center(box_center)
	pitch = process_area(area)
	
	conf = []
	bounds = []
	labels = []

	return throt, yaw, pitch
				

