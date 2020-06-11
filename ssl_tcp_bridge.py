# DEPENDENCIES --------------------------------------------------------------------------------------- #
import socket

# CONSTANT DEFINITIONS ------------------------------------------------------------------------------- #
SOCKET_TUPLE_INDEX_ADDR = 0
SOCKET_TUPLE_INDEX_PORT = 1
SOCKET_BUFFER_SIZE = 65536


# USER VARIABLES ------------------------------------------------------------------------------------- #
TargetServer = ('192.168.0.10', 50170) #TODO: receive parameters from command line
LocalServer = ('localhost',25000)
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
			VecSocketIsConnecting[FreeSocket] = True
			#Find the new next free socket
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

	#Active sockets sweeping
	if (1):
		for Counter in range(MaxNumOfConnections):
			if VecSocketIsConnected[Counter]:
				#Checks the target server
				try:
					data = VecConnToTargetServer[Counter].recv(SOCKET_BUFFER_SIZE)
					if len(data) == 0:
						#Disconnection
						VecConnFromInterestedClients[Counter].close()
						VecSocketIsConnected[Counter] = False
						#Find the new next free socket
						for Counter in range(MaxNumOfConnections + 1):
							FreeSocket = Counter
							if Counter == MaxNumOfConnections:
								#There are no more free sockets
								break
							if (not VecSocketIsConnected[Counter]) and (not VecSocketIsConnecting[Counter]):
								#Found a free socket
								break
					else:
						#Data
						print('Received ' + str(len(data)) + ' bytes from target server #' + str(Counter) + ': ' + data.decode("utf-8"))
				except socket.error:
					pass
				#Checks the target server
