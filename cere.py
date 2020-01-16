import serial 
port="/dev/ttyACM10"
rate=9600
s1=serial.Serial(port,rate)
s1.flushInput()
col=['Blinked\r\n','H\r\n']
while True:
	if s1.inWaiting()>0:
		input1=s1.readline()
		print(input1)
		
		try:
			n=input("enter digit now ")
			s1.write(n.encode())	
		except:
			print("Error")
			s1.write('0')		
