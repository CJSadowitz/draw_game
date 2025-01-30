from enum import Enum

class Turn_Type(Enum):
	SKIP      = 0
	DRAW_TWO  = 1
	DRAW_WILD = 2
	REVERSE   = 3
	REGULAR   = 4

class Turn:
	# returns next player's turn
	@staticmethod
	def update_turn(active_players, turn_index, turn_type, dir):
		if (turn_type.value < 3): # Skip/Draw/Draw Wild
			print ((turn_index + (2 * dir)) % len(active_players))
			return active_players[(turn_index + (2 * dir)) % len(active_players)]
		if (turn_type.value == 3): # Reverse
			dir *= -1
			return active_players[(turn_index + dir) % len(active_players)]
		if (turn_type.value == 4): # Regular
			return active_players[(turn_index + dir) % len(active_players)]
