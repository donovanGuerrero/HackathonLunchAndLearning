import xinput
import time
from Tkinter import *
from socket import *  

HOST = '172.16.6.219'	# Server(Raspberry Pi) IP address
PORT = 21567
BUFSIZ = 1024			 # buffer size
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)   # Create a socket
tcpCliSock.connect(ADDR) 

controller = xinput.XInputJoystick.enumerate_devices()[0]
input_buffer = .49
global forward 
forward = False
global reverse 
reverse = False
global isReversing
isReversing = False
global isForward
isForward = False

spd = 200

def changeSpeed(speed):
	tmp = 'speed'
	global spd
	spd = speed
	data = tmp + str(spd)  # Change the integers into strings and combine them with the string 'speed'. 
	print 'sendData = %s' % data
	tcpCliSock.send(data)  # Send the speed data to the server(Raspberry Pi)

changeSpeed(50)

@controller.event
def on_button(button, pressed):
	print 'button', button, pressed

@controller.event
def on_axis(axis, value):
	global forward
	global reverse
	if(axis == "right_trigger"):
		if(value > 0):
			forward = True
			reverse = False
		else:
			forward = False
	
	if(axis == "left_trigger"):
		if(value > 0):
			reverse = True
			forward = False
		else:
			reverse = False

while True:
	controller.dispatch_events()
	time.sleep(.01)
	print 'reverse', reverse
	if(reverse and not isReversing):
		tcpCliSock.send('backward')
		isReversing = True
	elif(forward and not isForward):
		tcpCliSock.send('forward')
		isForward = True
	elif((isReversing and not reverse) or (isForward and not forward)):
		tcpCliSock.send('stop')
		isReversing = False
		isForward = False
	
