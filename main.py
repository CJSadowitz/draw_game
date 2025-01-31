import pygame
from turn_networking import Server
from turn_networking import Client
from src.Game import Game
import json
import threading
import time

def main():
	print ("Host or Client (0 or 1)")
	conn = input()
	C = Client.Client()
	if (conn == '0'):
		S = Server.Server()
		game = Game()
		# Check Validity First
		S.add_rule(game.check_turn)
		S.add_rule(game.check_move)
		S.add_rule(game.game_state_request)
		# Then Make Move
		S.add_rule(game.make_move)
		# Create Game State
		S.convert_game_state_func(game.game_state_message)
		# Lobby is active/Players are in Game
		# Everything is typically handled Directly in here after previous setup
		lobby_thread = threading.Thread(target=S.create_lobby, args=(4,))
		lobby_thread.start()

		time.sleep(0.2)
		# Setting Timeout is required
		C.set_timeout(1.0)

		client_thread = threading.Thread(target=C.join_lobby, args=())
		client_thread.start()

		names = ["player_1", "player_2", "player_3", "player_4"]

		# Start Game
		game.set_player_names(names)
		game.shuffle_deck()
		game.set_starting_hands()
		# This is automatic in the thread, but I need to see response
		while True:
			print ("SERVER:", S.response)
			time.sleep(2.0)

	if (conn == '1'):
		C.set_timeout(1.0)
		client_thread = threading.Thread(target=C.join_lobby, args=())
		client_thread.start()
		# In lobby
		while True:
			print ("Input Move: 0-5")
			print (C.get_game_state())
			move = input()
			if (int(move) <= 5):
				uuid = "player_1"
				msg = {}
				msg["uuid"] = uuid
				msg["move"] = move
				C.set_message(json.dumps(msg))
				# print (json.dumps(msg))
				print ("get game state:",C.get_game_state())
			else: # Doesn't work :)
				msg = {}
				msg["uuid"] = "player_1"
				msg["more_info"] = "more_info"
				C.set_message(json.dumps(msg))
				print ("get game state:", C.get_game_state())

if __name__ == "__main__":
	main()
