import socket
import time

# Create a TCP/IP socket
ConnFromClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
TargetServer = ('192.168.0.10', 49823)

print('Connecting to ' + TargetServer[0] + ':' + str(TargetServer[1]));

if ConnFromClient.connect_ex(TargetServer) != 0:
	print('Connection error')
else:
	print('Connection successful')
	# Make non-bloking
	ConnFromClient.setblocking(0)
	# Send data
	message = 'Request!\r'
	print('Sending: ' + message)
	print('Sent ' + str(ConnFromClient.send(message)) + ' bytes!')
	# Look for the response
	while True:
		try:
			data = ConnFromClient.recv(1024)
			print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
			break
		except socket.error:
			pass

	print('Closing socket')
	ConnFromClient.close()
