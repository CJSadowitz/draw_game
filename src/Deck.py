from enum import Enum

class Color(Enum):
	ZERO     = 0
	ONE      = 1
	TWO      = 2
	THREE    = 3
	FOUR     = 4
	FIVE     = 5
	SIX      = 6
	SEVEN    = 7
	EIGHT    = 8
	NINE     = 9
	SKIP     = 10
	REVERSE  = 11
	DRAW_TWO = 12

class Wild(Enum):
	CHNG_COLOR = 0
	DRAW_FOUR  = 1

class Deck:
	def __init__(self):
		red = [f"RED_{card.name}" for card in Color]
		green = [f"GREEN_{card.name}" for card in Color]
		blue = [f"BLUE_{card.name}" for card in Color]
		yellow = [f"YELLOW_{card.name}" for card in Color]
		wild = [f"WILD_{card.name}" for card in Wild]
		list_of_cards = [
			red, red[1:],
			green, green[1:],
			blue, blue[1:],
			yellow, yellow[1:],
			wild, wild, wild, wild
		]
		self.deck = [item for sublist in list_of_cards for item in sublist]

	def get_deck(self):
		return self.deck

