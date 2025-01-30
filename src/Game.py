from src.Deck import Deck
from src.Turn import Turn, Turn_Type
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

		# Provide more data in game_state to requesting user
		self.more_info = [False, ""]

		# Player Information
		self.legal_moves = []
		self.current_cards = []

		self.active_players = []

		# Turn Information
		self.turn = None
		self.turn_dir = 1

	# Setters
	def set_deck(self, deck_list):
		self.deck = deck_list

	def set_discard(self, discard_list):
		self.discard = discard_list

	def set_player_names(self, names):
		self.player_names = names

	# Server Rules

	# request json:
	#	{
	#		uuid: "name",
	#		type: "more_info"
	#	}

	def game_state_request(self, message):
		data = json.loads(message)
		if (data["uuid"] not in self.player_names or data["uuid"] != self.turn):
			return False
		if (data["type"] == "more_info"):
			self.more_info = [True, data["uuid"]]
		return True

	# move json:
	#	{
	#		uuid: "name",
	#		move: 0-4 (card moves) or 5 (draw),
	#	}

	def check_turn(self, move):
		data = json.loads(move)
		if (str(data["uuid"]) not in self.player_names):
			return False
		if self.turn == data["uuid"]:
			return True
		else:
			return False

	def check_move(self, move):
		data = json.loads(move)
		move = int(data["move"])
		if (str(data["uuid"]) not in self.player_names):
			return False
		moves = self.get_legal_moves(data["uuid"])
		return moves[move]

	def make_move(self, move):
		# After Validation
		data = json.loads(move)
		move = int(data["move"])
		turn_index = self.active_players.index(data["uuid"])
		if (move == 5): # Draw Cards
			drawn_cards = []
			playable_bool = False
			# Draw Cards until player get a playable card
			while len(self.deck) > 0:
				drawn_card = self.deck[0]
				self.deck.remove(drawn_card)
				drawn_cards.append(drawn_card)
				if (self.playable(drawn_card)):
					playable_bool = True
					# Add cards to player hands
					self.add_cards(drawn_cards, self.turn)
					break
			# Player can no longer draw cards
			if (playable_bool == False):
				# Clear Hand
				index = 0
				for card_lists in self.player_hands[data["uuid"]]:
					self.discard.extend(card_lists)
					self.player_hands[data["uuid"]][index].clear() ###########################################
					index += 1
				# Remove Player
				self.active_players.remove(data["uuid"])
			# Update Turn
			self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.REGULAR, self.turn_dir)
			return True

		# Play Card
		card = self.player_hands[data["uuid"]][move][0]
		self.player_hands[data["uuid"]][move].remove(card)
		self.discard.append(card)

		# Wild Cards
		if (card[0] == 'w'):
			card_type = int(card[1:])
			if (card_type == 0):
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.REGULAR, self.turn_dir)
				# Change Color Logic ################################################################
			if (card_type == 1): # Draw Four AND Change Color
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.DRAW_WILD, self.turn_dir)
				player_who_gets_cards = self.active_players[turn_index + self.turn_dir]
			return True

		# Colored Cards
		match (int(card[1:])):
			case (10): # skip
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.SKIP, self.turn_dir)
			case (11): # reverse
				self.turn_dir *= -1
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.REVERSE, self.turn_dir)
			case (12): # draw two
				player = self.active_players[turn_index + self.turn_dir % len(self.active_players)]
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.DRAW_TWO, self.turn_dir)
				# Give 'player' two cards
				# BELOW NEEDS TO BE CHANGED SUCH THAT "PLAYER" IS THE ONE WHO LOSES
				if (len(self.deck) < 2): # Lose condition
					index = 0
					for card_lists in self.player_hands[data["uuid"]]:
						self.discard.extend(card_lists)
						self.player_hands[data["uuid"]][index].clear() ###########################
						index += 1
					# Remove Player
					self.active_players.remove(data["uuid"])
				else:
					# Give player the cards
					player_who_gets_cards = self.active_players[turn_index + self.turn_dir]
					# Add Cards Logic
			case _:
				# Regular Card
				self.turn = Turn.update_turn(self.active_players, turn_index, Turn_Type.REGULAR, self.turn_dir)
		return True

	# Game Logic
	def update_game(self, message):
		# After Validation and Is Game State Message
		data = json.loads(message)
		self.deck = data["deck"]
		self.discard = data["discard"]
		self.turn = data["turn"]
		if ("legal" in data):
			self.legal_moves = data["legal"]["legal_moves"]
		if ("cards" in data):
			self.current_cards = data["cards"]["cards"]


	def playable(self, card):
		if card == []:
			return False
		card = card[0]
		# Check Color i.e. Wild is always playable...
		if (card[0] == self.discard[len(self.discard) - 1][0]):
			return True
		# Check Number for everything except wild... but it would be handled above
		if (card[1:] == self.discard[len(self.discard) - 1][1:]):
			return True
		return False

	def add_cards(self, card_list, player):
		red = []
		green = []
		blue = []
		yellow = []
		wild = []
		for card in card_list:
			if (card[0] == 'r'):
				red.append(card)
			elif (card[0] == 'g'):
				green.append(card)
			elif (card[0] == 'b'):
				blue.append(card)
			elif (card[0] == 'y'):
				yellow.append(card)
			elif (card[0] == 'w'):
				wild.append(card)
		cards = [red, green, blue, yellow, wild]
		index = 0
		for card_list in self.player_hands[player]:
			card_list.extend(cards[index])
			index = index + 1

	# Host Side Only
	def shuffle_deck(self):
		size = len(self.deck)
		for i in range(size):
			random_index = random.randint(0, size - 1)
			self.deck[i], self.deck[random_index] = self.deck[random_index], self.deck[i]

	def reset_deck(self):
		# Double Check the logic
		discard_card = self.discard[-1]
		self.discard.remove(discard_card)
		# Put all of the discard into the deck
		self.deck.extend(self.discard)
		self.discard.clear()
		# Place back the discard
		self.discard.append(discard_card)

	def set_starting_hands(self):
		if (self.player_names == None):
			print ("SET_STARTING_HANDS: No players provided")
			return

		if (self.starting_hand * len(self.player_names) > len(self.deck) + 1):
			print ("SET_STARTING_HANDS: Starting hand is too large, lower the size")
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

		self.active_players = self.player_names

		# Handle Wild Starting Card

		self.discard.append(self.deck[0])
		self.deck.remove(self.deck[0])
		self.turn = self.player_names[0]

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

		for i in range(4):
			legal_moves.append(self.playable(moves[i]))

		# Wild Condition
		if (True in legal_moves):
			legal_moves.append(False)
		else:
			legal_moves.append(True)

		# Draw Condition
		if (len(self.deck) > 0):
			legal_moves.append(True)
		else:
			legal_moves.append(False)

		return legal_moves

	# Messages
	def game_state_message(self):
		#	{
		#		p1_cards: [],
		#		p2_cards: [],
		#		...,
		#		p1_deck_lengths: [],
		#		p2_deck_lengths: [],
		#		...,
		#		discard: [length, discard_list]
		#		draw: len(self.deck)
		#		turn: uuid
		#	}
		data = {}
		for player in self.player_hands:
			name = str(player)
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
		data["turn"] = self.turn

		if (self.more_info[0] == True):
			data["legal"] = self.legal_moves_message(self.more_info[1])
			data["cards"] = self.player_card_list_message(self.more_info[1])
			self.more_info = [False, ""]

		return json.dumps(data)

	def legal_moves_message(self, name):
		#	{
		#		uuid: name,
		#		legal_moves: [r,g,b,y,w,d] (All booleans)
		#	}
		data = {}
		data["uuid"] = name
		legal_moves = self.get_legal_moves(name)
		data["legal_moves"] = legal_moves
		return data

	def player_card_list_message(self, name):
		#	{
		#		uuid: name,
		#		cards: [[], [], [], [], []]
		#	}
		data = {}
		data["uuid"] = name
		cards = self.player_hands[name]
		data["cards"] = cards
		return data
