from src.Deck import Deck
import random
import string
import json

class Game:
	def __init__(self, player_names=None, deck=None, discard=None, starting_hand=12):
		if (deck is None):
			deck = Deck().get_deck()
		self.deck = deck

		if (discard is None):
			discard = []
		self.discard = discard

		self.starting_hand = starting_hand

		self.player_names = player_names

		# player: [[r], [g], [b], [y], [w]]
		self.player_hands = {}

	# Setters
	def set_deck(self, deck_list):
		self.deck = deck_list

	def set_discard(self, discard_list):
		self.discard = discard_list

	def set_player_names(self, names):
		self.player_names = names

	# Methods/Game Logic
	def shuffle_deck(self):
		size = len(self.deck)
		for i in range(size):
			random_index = random.randint(0, size - 1)
			self.deck[i], self.deck[random_index] = self.deck[random_index], self.deck[i]

	def set_starting_hands(self):
		if (self.player_names == None):
			print ("No players provided")
			return

		if (self.starting_hand * len(self.player_names) > len(self.deck)):
			print ("Starting hand is too large, lower the size")
			return

		for player in self.player_names:
			red = []
			green = []
			blue = []
			yellow = []
			wild = []
			for i in range(self.starting_hand):
				card = self.deck[i]
				if card[0] == 'R':
					red.append(card)
				elif card[0] == 'G':
					green.append(card)
				elif card[0] == 'B':
					blue.append(card)
				elif card[0] == 'Y':
					yellow.append(card)
				elif card[0] == 'W':
					wild.append(card)
				self.deck.remove(card)
			self.player_hands[player] = [red, green, blue, yellow, wild]

	# Getters
	def get_game_state(self):
		data = {}
		for player in self.player_hands:
			name = player
			cards = []
			lengths = []
			for i in range(5):
				try:
					cards.append(self.player_hands[player][i][0])
					lengths.append(len(self.player_hands[player][i][0]))
				except Exception as e:
					cards.append("[]")
					lengths.append(0)
			data[name + "_cards"] = cards
			data[name + "_len"]   = lengths
		data["discard"] = [len(self.discard), self.discard]
		data["deck"] = len(self.deck)

		return json.dumps(data)
