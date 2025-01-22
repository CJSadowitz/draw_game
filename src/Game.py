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
	def check_move(self, move):
		# move json:
		#	{
		#		player_name: "name",
		#		move: 0-4 (card moves) or 5 (draw),
		#	}
		data = json.loads(move)
		if (data["player_name"] not in self.player_names):
			return False
		moves = self.get_legal_moves(data["player_name"])
		return moves[data["move"]]

	def shuffle_deck(self):
		size = len(self.deck)
		for i in range(size):
			random_index = random.randint(0, size - 1)
			self.deck[i], self.deck[random_index] = self.deck[random_index], self.deck[i]

	def set_starting_hands(self):
		if (self.player_names == None):
			print ("No players provided")
			return

		if (self.starting_hand * len(self.player_names) > len(self.deck) + 1):
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
				if card[0] == 'r':
					red.append(card)
				elif card[0] == 'g':
					green.append(card)
				elif card[0] == 'b':
					blue.append(card)
				elif card[0] == 'y':
					yellow.append(card)
				elif card[0] == 'w':
					wild.append(card)
				self.deck.remove(card)
			self.player_hands[player] = [red, green, blue, yellow, wild]

		self.discard = self.deck[0]
		self.deck.remove(self.deck[0])

	# Getters
	def get_legal_moves(self, name):
		# [R, G, B, Y, W, D]
		# All Booleans
		if (name not in self.player_names):
			return None
		moves = []
		for i in range(5):
			moves.append(self.player_hands[name][i])

		discard = self.discard
		legal_moves = []

		for list in moves:
			if (list == []):
				print ("[]", end=" ")
				continue
			print (list[0], end=" ")
		print ("")

		for i in range(4):
			if (moves[i] == []):
				legal_moves.append(False)
				continue
			# Check Color
			if (discard[0] == moves[i][0][0]):
				legal_moves.append(True)
			# Check Number
			elif (discard[1:] == moves[i][0][1:]):
				legal_moves.append(True)
			else:
				legal_moves.append(False)

		if (True in legal_moves):
			legal_moves.append(False)
		else:
			legal_moves.append(True)

		if (len(self.deck) > 0):
			legal_moves.append(True)
		else:
			legal_moves.append(False)

		return legal_moves

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

	def get_player_card_list(self, name):
		pass
