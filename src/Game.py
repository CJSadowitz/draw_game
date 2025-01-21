from src.Deck import Deck

class Game:
	def __init__(self):
		# List of cards = Deck
		self.deck = Deck().get_deck()
		# List of cards = discard
		self.discard = []
		# Dict of players and a list of lists for each sorted card in their hand
		self.player_hands = {}

	def shuffle_deck():
		pass

	def set_starting_hands(player_names):
		# for (player in player_names):
		pass
