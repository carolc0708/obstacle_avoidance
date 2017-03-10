import RPi.GPIO as GPIO
import time
import threading

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
class Thread_1(threading.Thread):
	
	# Create variables to be passed
	def __init__(self, threadID, name, counter, dist):
		# Decode variable into local variables
		threading.Thread.__init__(self)
		self.threadID = threadID
		self.name = name
		self.counter = counter
		self.dist = 0
	def run(self):
		# task
		GPIO.setup(TRIG_R, GPIO.OUT)
		GPIO.setup(ECHO_R, GPIO.IN)
		self.dist = distance(TRIG_R,ECHO_R)

class Thread_2(threading.Thread):
        # Create variables to be passed
        def __init__(self, threadID, name, counter, dist):
                # Decode variable into local variables
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter
		self.dist = 0
        def run(self):
                # task
                GPIO.setup(TRIG_L, GPIO.OUT)
                GPIO.setup(ECHO_L, GPIO.IN)
                self.dist = distance(TRIG_L,ECHO_L)

class Thread_3(threading.Thread):

        # Create variables to be passed
        def __init__(self, threadID, name, counter, dist):
                # Decode variable into local variables
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter
		self.dist = 0
        def run(self):
                # task
                GPIO.setup(TRIG_F, GPIO.OUT)
                GPIO.setup(ECHO_F, GPIO.IN)
                self.dist = distance(TRIG_F,ECHO_F)

class Thread_4(threading.Thread):

        # Create variables to be passed
        def __init__(self, threadID, name, counter, dist):
                # Decode variable into local variables
                threading.Thread.__init__(self)
                self.threadID = threadID
                self.name = name
                self.counter = counter
		self.dist = 0
        def run(self):
                # task
                GPIO.setup(TRIG_B, GPIO.OUT)
                GPIO.setup(ECHO_B, GPIO.IN)
                self.dist = distance(TRIG_B,ECHO_B)
#		print self.dist

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
			thread1 = Thread_1(1, "Thread-1", 1, 0)
			thread2 = Thread_2(2, "Thread-2", 1, 0)
			thread3 = Thread_3(3, "Thread-3", 1, 0)
			thread4 = Thread_4(4, "Thread-4", 1, 0)
			
			# Start new Threads
			thread1.start()
			thread2.start()
			thread3.start()
			thread4.start()
	
			print "-----------Exiting Main Thread---------"

			print ("Right = %.1f cm, Left = %.1f cm, Front = %.1f cm, Back = %.1f cm" % (thread1.dist,thread2.dist,thread3.dist,thread4.dist))
			time.sleep(1)
 
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
		print("Measurement stopped by User")
		GPIO.cleanup()	
	
