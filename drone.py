# define a class to condense all functions necessary for the testing

# PWM i2c driver library
import Adafruit_PCA9685 as pca
import RPi.GPIO as GPIO
import time
# modified CNN library
from darkflow.net.build import TFNet
# image processing library
import cv2
# utils for processing
from utils import *

# define vars/declare objects
pwm = pca.PCA9685()

weight = '/home/pi/git/darkflow/bin/tiny-yolo-voc.weights'
cfg = '/home/pi/git/darkflow/cfg/tiny-yolo-voc.cfg'

threshold = 0.15
gpu = 0

options = {'model': cfg, 'load': weight, 'gpu': gpu, 'threshold': threshold}

vals = [1, 2, 0]
slope = 1.16

trig = 18
echo = 24
GPIO.setmode(GPIO.BCM)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

# make drone process input and fly
class Drone(object):
	def __init__(self):
		# build network and create camera
		self.net = TFNet(options)
		self.camera = cv2.VideoCapture(0)

	# ultrasonic
	def distance(self):
		GPIO.output(trig, True)
		time.sleep(0.00001)
		GPIO.output(trig, False)
		initial = time.time()
		final = time.time()

		while GPIO.input(echo) == 0:
			inital = time.time()
		while GPIO.input(echo) == 1:
			final = time.time()

		return ((final - initial) * 34300) / 2

	# arm the drone (also need killswitch)
	def arm(self, wait_time):
		time.sleep(wait_time)
		pwm.set_pwm(vals[0], 0, dig_to_pwm(900))
		time.sleep(3)
	
	# send pwm signals based off array of values [throttle, yaw, pitch] (roll is unnecessary)
	def move(self, direc):
		x = 0
		for i in direc:
			# set pwm values for each axis
			pwm.set_pwm(vals[x], 0, dig_to_pwm(i))
			x+=1

	# take picture and run through net
	def process(self):
		_, frame = self.camera.read()
		w, h = frame.shape[:2]
		out = self.net.return_predict(frame)
		return process_data(out, w, h)

# convert digital signals to pwm (and vice versa) based off linear relationship
def dig_to_pwm(dig):
	return int(dig / slope)

def pwm_to_dig(pwm):
	return int(pwm * slope)
