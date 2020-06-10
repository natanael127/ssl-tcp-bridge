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
LocalClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #TODO: Stablish many connections
LocalHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
VecConnInterestedClients = [];
for Counter in range(MAX_CONNECTIONS):
	VecConnInterestedClients.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

#TODO: work on IPv6

# ALGORITHM ------------------------------------------------------------------------------------------ #

#To target server
print('Connecting to ' + TargetServer[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(TargetServer[SOCKET_TUPLE_INDEX_PORT]))
if LocalClient.connect_ex(TargetServer) != 0:
	print('Connection error')
else:
	print('Connection successful')
	# Make non-bloking
	LocalClient.setblocking(0)
	# Send data
	message = 'Request!\r'
	print('Sending: ' + message)
	print('Sent ' + str(LocalClient.send(message)) + ' bytes!')
	# Look for the response
	while True:
		try:
			data = LocalClient.recv(SOCKET_BUFFER_SIZE)
			print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
			break
		except socket.error:
			pass

	print('Closing socket')
	LocalClient.close()

#From interested client
LocalHost.bind(LocalServer)
LocalHost.listen(MAX_CONNECTIONS)
LocalHost.setblocking(0)
print('Waiting for a connection to the local sever')
while True:
	try:
		VecConnInterestedClients[0], InterestedClientAddress = LocalHost.accept()
		print ('Connection from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
		break
	except socket.error:
		pass

VecConnInterestedClients[0].setblocking(0)

while True:
	try:
		data = VecConnInterestedClients[0].recv(SOCKET_BUFFER_SIZE)
		print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
		break
	except socket.error:
		pass
print ('Sending data back to the client')
VecConnInterestedClients[0].send(data)
VecConnInterestedClients[0].close()
