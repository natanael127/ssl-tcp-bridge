# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_BUFFER_SIZE = 65536

# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 49823) #TODO: receive parameters from command line

# OBJECTS -------------------------------------------------------------------------------------------- #
ConnToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ALGORITHM ------------------------------------------------------------------------------------------ #
print('Connecting to ' + TargetServer[0] + ':' + str(TargetServer[1]));
if ConnToServer.connect_ex(TargetServer) != 0:
	print('Connection error')
else:
	print('Connection successful')
	# Make non-bloking
	ConnToServer.setblocking(0)
	# Send data
	message = 'Request!\r'
	print('Sending: ' + message)
	print('Sent ' + str(ConnToServer.send(message)) + ' bytes!')
	# Look for the response
	while True:
		try:
			data = ConnToServer.recv(SOCKET_BUFFER_SIZE)
			print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
			break
		except socket.error:
			pass

	print('Closing socket')
	ConnToServer.close()
