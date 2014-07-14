from spock.utils import pl_announce
from spock.mcp import mcdata

class ClientInfo:
	def __init__(self):
		self.uuid = 0
		self.game_info = {
			'level_type': 0,
			'gamemode': None,
			'dimension': 0,
			'difficulty': 0,
			'max_players': 0,
		}
		self.spawn_position = {
			'x': 0,
			'y': 0,
			'z': 0,
		}
		self.health = {
			'health': 20,
			'food': 20,
			'saturation': 5,
		}
		self.position = {
			'x': 0,
			'y': 0,
			'z': 0,
			'stance': 0,
			'yaw': 0,
			'pitch': 0,
			'on_ground': False,
		}
		self.player_list = {}

	def reset(self):
		self.__init__()


@pl_announce('ClientInfo')
class ClientInfoPlugin:
	def __init__(self, ploader, settings):	
		self.emit = ploader.requires('Event').emit
		packets = (0x01, 0x05, 0x06, 0x08, 0x38, 0x40)
		handlers = (self.handle01, self.handle05, self.handle06, self.handle08, self.handle38, self.handle40)
		for i in range(len(packets)):
			ploader.reg_event_handler((mcdata.PLAY_STATE, mcdata.SERVER_TO_CLIENT, packets[i]), handlers[i])

		self.client_info = ClientInfo()
		ploader.provides('ClientInfo', self.client_info)

	#Login Request - Update client state info
	def handle01(self, name, packet):
		self.client_info.eid = packet.data['eid']
		del packet.data['eid']
		self.client_info.game_info = packet.data
		self.emit('cl_login', packet.data)

	#Spawn Position - Update client Spawn Position state
	def handle05(self, name, packet):
		self.client_info.spawn_position = packet.data
		self.emit('cl_spawn_update', packet.data)


	#Update Health - Update client Health state
	def handle06(self, name, packet):
		self.client_info.health = packet.data
		self.emit('cl_health_update', packet.data)

	#Position Update Packets - Update client Position state
	def handle08(self, name, packet):
		for key, value in packet.data.items():
			self.client_info.position[key] = value
		self.emit('cl_position_update', self.client_info.position)

	#Player List Item - Update PlayerList (not actually a list...)
	def handle38(self, name, packet):
		name = packet.data['player_name']
		if packet.data['online']:
			self.client_info.player_list[name] = packet.data['ping']
		else:
			try:
				del self.client_info.player_list[name]
			except KeyError:
				print(
					'Tried to remove', name, 
					'from playerlist, but player did not exist'
				)
		self.emit('cl_plist_update', self.client_info.player_list)

	def handle40(self, name, packet):
		self.client_info.reset()
		self.emit('cl_disconnected')