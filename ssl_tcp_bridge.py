# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_TUPLE_INDEX_ADDR = 0
SOCKET_TUPLE_INDEX_PORT = 1
SOCKET_BUFFER_SIZE = 65536


# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 55195) #TODO: receive parameters from command line
LocalServer = ('localhost',30000)
MaxNumOfConnections = 7


# OBJECTS AND INTERNAL VARIABLES --------------------------------------------------------------------- #
LocalHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
VecConnFromInterestedClients = []
VecConnToTargetServer = []
VecSocketIsConnected = []

#TODO: work on IPv6

# ALGORITHM ------------------------------------------------------------------------------------------ #

#Arrays initialization
for Counter in range(MaxNumOfConnections):
	#Create sockets
	VecConnFromInterestedClients.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
	VecConnToTargetServer.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
	#Make them non-blocking
	VecConnFromInterestedClients[Counter].setblocking(0)
	VecConnToTargetServer[Counter].setblocking(0)
	#Initializes the control flag of connections
	VecSocketIsConnected.append(False)

# Make non-bloking
VecConnToTargetServer[0].setblocking(0)
#To target server
print('Connecting to ' + TargetServer[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(TargetServer[SOCKET_TUPLE_INDEX_PORT]))
while True:
	try:
		VecConnToTargetServer[0].connect(TargetServer)
		print('Connection successful')
		break
	except socket.error:
		pass
	
# Send data
message = 'Request!\r'
while True:
	try:
		print('Sent ' + str(VecConnToTargetServer[0].send(message)) + ' bytes: ' + message)
		break
	except socket.error:
		pass

# Look for the response
while True:
	try:
		data = VecConnToTargetServer[0].recv(SOCKET_BUFFER_SIZE)
		print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
		break
	except socket.error:
		pass

print('Closing socket')
VecConnToTargetServer[0].close()

#From interested client
LocalHost.bind(LocalServer) #TODO: Handle errors
LocalHost.listen(MaxNumOfConnections)
LocalHost.setblocking(0)
print('Waiting for a connection to the local sever')
while True:
	try:
		VecConnFromInterestedClients[0], InterestedClientAddress = LocalHost.accept()
		print ('Connection from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
		break
	except socket.error:
		pass

while True:
	try:
		data = VecConnFromInterestedClients[0].recv(SOCKET_BUFFER_SIZE)
		print('Received ' + str(len(data)) + ' bytes: ' + data.decode("utf-8"))
		break
	except socket.error:
		pass
print ('Sending data back to the client')
VecConnFromInterestedClients[0].send(data)
VecConnFromInterestedClients[0].close()
