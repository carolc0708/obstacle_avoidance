import RPi.GPIO as GPIO
import time
import threading
from CustomFilter import CustomFilter

exitFlag = 0 # Fail safe exit - nothing not used

# GPIO pin number mode
GPIO.setmode(GPIO.BCM)

# pin number assignment
# right side
TRIG_R = 10
ECHO_R = 9

# left side
TRIG_L = 15 
ECHO_L = 18 

# front side
TRIG_F = 23
ECHO_F = 24

# back side
TRIG_B = 17
ECHO_B = 27


# threshold assignment
#WARNING_DISTANCE = None 
#SAMPLING_FREQUENCY = None

# settings
GPIO.setwarnings(False)

# thread handling
class Thread(threading.Thread):
	# Create variables to be passed
	def __init__(self, threadID, name, counter, trig, echo):
		# Decode variable into local variables
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.trig = trig
		self.echo = echo
		self.dist = 0
		self.filter = CustomFilter()
		self.f_dist = 0
	def run(self):
		# task
		GPIO.setup(self.trig, GPIO.OUT)
		GPIO.setup(self.echo, GPIO.IN)
		self.dist = distance(self.trig,self.echo)
		self.f_dist = self.filter.observe(self.dist)
		

# functions
# to check if distance d is legal
#def isLegalDistance(d):

#	return d < 400 # 4 m

def distance(TRIG,ECHO):
	# set Trigger to HIGH
	GPIO.output(TRIG, True)
	
	# set Trigger to LOW after 0.01ms
	time.sleep(0.00001)
	GPIO.output(TRIG, False) 

	pulse_start = time.time()		
	# record start time
	while GPIO.input(ECHO) == 0:
		pulse_start = time.time()
#		print 'start'

	pulse_end = time.time()
	# record stop time
	while GPIO.input(ECHO) == 1:
		pulse_end = time.time()
#		print 'end'
		
	# measure the pulse duration
	pulse_duration = pulse_end - pulse_start
	
	# calculate the distance
	distance = pulse_duration * 17150
	
	return distance - 0.5 # for calibration

if __name__ == '__main__':
	try:
        	while True:
			# Create new threads
			thread1 = Thread(1, "Thread-1", 1, TRIG_R, ECHO_R)
			thread2 = Thread(2, "Thread-2", 1, TRIG_L, ECHO_L)
			thread3 = Thread(3, "Thread-3", 1, TRIG_F, ECHO_F)
			thread4 = Thread(4, "Thread-4", 1, TRIG_B, ECHO_B)			
			# Start new Threads
			thread1.start()
			thread2.start()
			thread3.start()
			thread4.start()
			print "-----------Exiting Main Thread---------"

			print ("Right = %.1f cm, Left = %.1f cm, Front = %.1f cm, Back = %.1f cm" % (thread1.dist,thread2.dist,thread3.dist,thread4.dist))
			print ("[Filtered] Right = %.1f cm, Left = %.1f cm, Front = %.1f cm, Back = %.1f cm" % (thread1.f_dist,thread2.f_dist,thread3.f_dist,thread4.f_dist))
			time.sleep(1)
 
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()	
	
