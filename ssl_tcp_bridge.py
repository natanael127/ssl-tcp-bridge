# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_TUPLE_INDEX_ADDR = 0
SOCKET_TUPLE_INDEX_PORT = 1
SOCKET_BUFFER_SIZE = 65536
MAX_CONNECTIONS = 7

# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 50010) #TODO: receive parameters from command line
LocalServer = ('localhost',30000)

# OBJECTS -------------------------------------------------------------------------------------------- #
ConnToServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TODO: Stablish many connections
LocalHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#TODO: work on IPv6

# ALGORITHM ------------------------------------------------------------------------------------------ #

#To target server
print('Connecting to ' + TargetServer[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(TargetServer[SOCKET_TUPLE_INDEX_PORT]))
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

#From interested client
LocalHost.bind(LocalServer)
LocalHost.listen(MAX_CONNECTIONS)
print('Waiting for a connection to the local sever')
ConnInterestedClient, InterestedClientAddress = LocalHost.accept()
ConnInterestedClient.setblocking(0)
print ('Connection from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
while True:
	try:
		data = ConnInterestedClient.recv(SOCKET_BUFFER_SIZE)
		print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
		break
	except socket.error:
		pass
print ('Sending data back to the client')
ConnInterestedClient.send(data)
ConnInterestedClient.close()
