import serial
import time


VALID = {"forward" : b'f', "backward" : b'b', "stop" : b's'}
try:
	ser = serial.Serial('/dev/ttyACM1', 9600)
except:
	ser = serial.Serial('/dev/ttyACM0', 9600)

print("VALID COMMANDS: ")

for k in VALID.keys():
	print("\t" + k)
print()

while True:
	resp = str( input() ).lower()
	if resp in VALID:
		ser.write( VALID[resp] )
		time.sleep(.25)

		print( ser.readline() )

	else:
		print("VALID COMMANDS: ")
		for k in VALID.keys():
			print("\t" + k + "  \t" + str(VALID[k]) )
		print()
