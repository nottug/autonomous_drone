# main program, runs through basic algorith

from drone import Drone
import time

middle = 1680

if __name__ == "__main__":
	# create drone object
	d = Drone()
	try:
		# arming sequence
		d.move([900, 1500, 1500])
		d.arm(2)
		d.move([middle - 250, 1500, 1500])
		time.sleep(1.5)

		# loop through pictures and move based off of outputs
		while True:
			throt, yaw, pit = d.process()
			print(throt, yaw, pit)
			d.move([throt, yaw, pit])
	except:
		# stop the drone if program shut off
		d.move([900, 1500, 1500])
