# obstacle_avoidance

STEP 1: Raspberry pi should be set up with static IP address for pietty to connect.  
STEP 2: Open a terminal, execute `$ roscore`.  
STEP 3: Open the second terminal, and do the following.  
```
$ cd catkin_ws
$ source ./devel/setup.bash # every time after file content is revised 
$ rosrun obstacle_avoidance ultrasonic_publisher.py
```
You will see the following if message is published.
```
[INFO] [1489379901.960451]: Publish Alert:1111
```
STEP 4: Open the third terminal, and do the following.
```
$ cd catkin_ws
$ source ./devel/setup.bash # every time after file content is revised 
$ rosrun obstacle_avoidance ultrasonic_subscrer.py
```
You will receive message as following immediately in the second terminal.
```
[INFO] [1489379911.056675]: Receive Alert: Publish Alert:1111
```
