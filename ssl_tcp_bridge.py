# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_TUPLE_INDEX_ADDR = 0
SOCKET_TUPLE_INDEX_PORT = 1
SOCKET_BUFFER_SIZE = 65536


# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 49988) #TODO: receive parameters from command line
LocalServer = ('localhost',20000)
MaxNumOfConnections = 3


# OBJECTS AND INTERNAL VARIABLES --------------------------------------------------------------------- #
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

#Local host initialization
LocalHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LocalHost.bind(LocalServer) #TODO: Handle errors
LocalHost.listen(MaxNumOfConnections)
LocalHost.setblocking(0)

#Control to next connection
FreeSocket = 0
#Main infinity loop
while True:
	#Verify for a pending incoming connection to accept (FreeSocket == MaxNumOfConnections means all are busy)
	if FreeSocket < MaxNumOfConnections:
		#Accepts connections
		try:
			VecConnFromInterestedClients[FreeSocket], InterestedClientAddress = LocalHost.accept()
			print ('Connection ' + str(FreeSocket) + ' from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
			#Make the respective connection to server
			print('Connecting to ' + TargetServer[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(TargetServer[SOCKET_TUPLE_INDEX_PORT]))
			while True:    #TODO: Unblock it
				try:
					VecConnToTargetServer[FreeSocket].connect(TargetServer)
					print('Connection to server successful')
					break
				except socket.error:
					pass
			#Finds the new next free socket and assign the connection flag
			VecSocketIsConnected[FreeSocket] = True
			for Counter in range(MaxNumOfConnections + 1):
				FreeSocket = Counter
				if Counter == MaxNumOfConnections:
					#There are no more free sockets
					break
				if not VecSocketIsConnected[Counter]:
					#Found a free socket
					break
		except socket.error:
			pass
	else:
		#Refuse connections
		try:
			ConnRejectedClient, InterestedClientAddress = LocalHost.accept()
			ConnRejectedClient.close()
			print ('Rejecting from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
		except socket.error:
			pass

	#Active sockets sweeping
	for Counter in range(MaxNumOfConnections):
		if VecSocketIsConnected[Counter]:
			#Check for messages or disconnection from target server
			data = bytearray(0)
			try:
				data = VecConnToTargetServer[Counter].recv(SOCKET_BUFFER_SIZE)
				if len(data) == 0:	#Disconnection
					VecConnToTargetServer[Counter].close()
					VecConnFromInterestedClients[Counter].close()
					VecSocketIsConnected[Counter] = False
				else:			#Message
					while True: #TODO: Unblock it
						try:
							VecConnFromInterestedClients[Counter].send(data)
							break
						except socket.error:
							pass
			except socket.error:
				pass
			#Check for messages or disconnection from interested clients
			data = bytearray(0)
			try:
				data = VecConnFromInterestedClients[Counter].recv(SOCKET_BUFFER_SIZE)
				if len(data) == 0:	#Disconnection
					VecConnToTargetServer[Counter].close()
					VecConnFromInterestedClients[Counter].close()
					VecSocketIsConnected[Counter] = False
				else:			#Message
					while True: #TODO: Unblock it
						try:
							VecConnToTargetServer[Counter].send(data)
							break
						except socket.error:
							pass
			except socket.error:
				pass

	
#The program must never reach below here

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
