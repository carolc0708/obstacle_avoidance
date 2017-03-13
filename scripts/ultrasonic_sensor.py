import RPi.GPIO as GPIO
import time
from CustomFilter import CustomFilter

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
WARNING_DISTANCE = 400 # 4m 
SAMPLING_FREQUENCY = None

# settings
GPIO.setwarnings(False)
GPIO.setup(TRIG_R, GPIO.OUT)
GPIO.setup(ECHO_R, GPIO.IN)
GPIO.setup(TRIG_L, GPIO.OUT)
GPIO.setup(ECHO_L, GPIO.IN)
GPIO.setup(TRIG_F, GPIO.OUT)
GPIO.setup(ECHO_F, GPIO.IN)
GPIO.setup(TRIG_B, GPIO.OUT)
GPIO.setup(ECHO_B, GPIO.IN)

# functions

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
		custom_filter_r = CustomFilter()
		custom_filter_l = CustomFilter()
		custom_filter_f = CustomFilter()
		custom_filter_b = CustomFilter()
			
		dist_r = distance(TRIG_R,ECHO_R)
		dist_l = distance(TRIG_L,ECHO_L)
		dist_f = distance(TRIG_F,ECHO_F)
		dist_b = distance(TRIG_B,ECHO_B)
		#	print ("Right = %.1f cm, Left = %.1f cm, Front = %.1f cm, Back = %.1f cm" % (dist_r,dist_l,dist_f,dist_b))
		fdist_r = custom_filter_r.observe(dist_r)
		fdist_l = custom_filter_l.observe(dist_l)
		fdist_f = custom_filter_f.observe(dist_f)
		fdist_b = custom_filter_b.observe(dist_b)
		#	print ("[Filtered] Right = %.1f cm, Left = %.1f cm, Front = %.1f cm, Back = %.1f cm" % (fdist_r,fdist_l,fdist_f,fdist_b))
		#	print('---------------------------')
		alert_str = ""
		if fdist_r < WARNING_DISTANCE :
			alert_str += '1'
		else:
			alert_str += '0'
		if fdist_l < WARNING_DISTANCE:
			alert_str += '1'
		else:
			alert_str += '0'
		if fdist_f < WARNING_DISTANCE:
			alert_str += '1'
		else:
			alert_str += '0'
		if fdist_b < WARNING_DISTANCE:
			alert_str += '1'
		else:
			alert_str += '0'
		print alert_str
				  
	#	time.sleep(1)
 
	# Reset by pressing CTRL + C
	except KeyboardInterrupt:
	#	print("Measurement stopped by User")
		GPIO.cleanup()	
	
