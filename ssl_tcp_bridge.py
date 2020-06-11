# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_TUPLE_INDEX_ADDR = 0
SOCKET_TUPLE_INDEX_PORT = 1
SOCKET_BUFFER_SIZE = 65536


# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 50170) #TODO: receive parameters from command line
LocalServer = ('localhost',20000)
MaxNumOfConnections = 3


# OBJECTS AND INTERNAL VARIABLES --------------------------------------------------------------------- #
VecConnFromInterestedClients = []
VecConnToTargetServer = []
VecSocketIsConnected = []
VecSocketIsConnecting = []

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
	VecSocketIsConnecting.append(False)

#Local host initialization
LocalHost = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
LocalHost.setblocking(0)
try:
	LocalHost.bind(LocalServer)
except socket.error:
	print('Failed to bind localhost socket. Exiting...')
	exit()
try:
	LocalHost.listen(MaxNumOfConnections)
except socket.error:
	print('Failed to listen localhost socket. Exiting...')
	exit()

#Control to next connection
FreeSocket = 0
#Main infinity loop
while True:
	#Verify for a pending incoming connection to accept (FreeSocket == MaxNumOfConnections means all are busy)
	if FreeSocket < MaxNumOfConnections:
		#Accepts connections
		try:
			VecConnFromInterestedClients[FreeSocket], InterestedClientAddress = LocalHost.accept()
			print ('Connection #' + str(FreeSocket) + ' from ' + InterestedClientAddress[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(InterestedClientAddress[SOCKET_TUPLE_INDEX_PORT]))
			#Schedules the respective connection to server
			print('Connecting to ' + TargetServer[SOCKET_TUPLE_INDEX_ADDR] + ':' + str(TargetServer[SOCKET_TUPLE_INDEX_PORT]))
			VecSocketIsConnecting[FreeSocket] = True
			#Finds the new next free socket
			for Counter in range(MaxNumOfConnections + 1):
				FreeSocket = Counter
				if Counter == MaxNumOfConnections:
					#There are no more free sockets
					break
				if (not VecSocketIsConnected[Counter]) and (not VecSocketIsConnecting[Counter]):
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

	#Connecting sockets sweeping
	for Counter in range(MaxNumOfConnections):
		if VecSocketIsConnecting[Counter]:
			try:
				VecConnToTargetServer[Counter].connect(TargetServer)
				VecSocketIsConnected[Counter] = True
				VecSocketIsConnecting[Counter] = False
				print('Mirror connection #' + str(Counter) + ' done!')
				break
			except socket.error:
				pass

	if (0):
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
