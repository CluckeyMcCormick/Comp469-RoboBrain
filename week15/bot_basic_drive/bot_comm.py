import serial
import time

ser = None

CODE_FORWARD  = b'f'
CODE_BACKWARD = b'b'
CODE_LEFT     = b'l'
CODE_RIGHT    = b'r'

def initialize_comms(exit_on_fail=False):
	global ser

	try:
		ser = serial.Serial('/dev/ttyACM1', 9600)
	except:
		try:
			ser = serial.Serial('/dev/ttyACM0', 9600)
		except:
			print("Could not connect to arduino!")
			ser = None

			if exit_on_fail:
				exit()


def do_action(bot_dir, action):
	if ser is None:
		return None

	#If bot_dir and the action are
	#the same 
	if bot_dir == action:
		#go forward
		forward()

	#If the parities are the same,
	#we are axially the same
	elif bot_dir % 2 == action % 2:
		#backward
		backward()

	#Else, if the action is just one
	#less than our direction,
	elif bot_dir - 1 == action or (bot_dir == 0 and action == 3): 
		#turn right
		right()
		#go forward
		forward()

	#Otherwise, if the action is just
	#one greater than our direction
	elif (bot_dir + 1) % 4 == action:
		#turn left
		left()
		#go forward
		forward()

def forward():
	action_to_bot(CODE_FORWARD)

def backward():
	action_to_bot(CODE_BACKWARD)

def left():
	action_to_bot(CODE_LEFT)

def right():
	action_to_bot(CODE_RIGHT)

def action_to_bot(action_code):
	ser.write( action_code )
	time.sleep(.25)
	ser.readline()

if __name__ == '__main__':
	print("clear the field!")
	initialize_comms(True)
	print("Robo-drive in: ")
	for i in range(4, -1, -1):
		time.sleep(1)
		print("\t" + str(i))

	for i in range(4):
		print()
		print("Side " + str(i))

		print("\tForward!")
		forward()
		print("\tForward!")
		forward()

		if i % 2 == 0:
			print("\tForward!")
			forward()
		print("\tRight!")
		right()

	print("All done!")

