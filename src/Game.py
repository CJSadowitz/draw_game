from src.Deck import Deck
import random

class Game:
	def __init__(self, deck=None, discard=None, starting_hand=7):
		if (deck is None):
			deck = Deck().get_deck()
		self.deck = deck

		if (discard is None):
			discard = []
		self.discard = discard

		self.starting_hand = starting_hand

		# player: [[r], [g], [b], [y], [w]]
		self.player_hands = {}

	def shuffle_deck(self):
		size = len(self.deck)
		for i in range(size):
			random_index = random.randint(0, size - 1)
			self.deck[i], self.deck[random_index] = self.deck[random_index], self.deck[i]

	def set_starting_hands(self, player_names):
		for player in player_names:
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
