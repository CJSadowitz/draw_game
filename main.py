import pygame
from src.Game import Game
import json

def main():
	names = ["player_1", "player_2", "player_3", "player_4"]
	game = Game(names)
	game.shuffle_deck()
	game.set_starting_hands()
	# print (game.get_game_state())
	# print (game.discard)
	# print (game.get_legal_moves("player_1"))
	move = {
			"player_name": "player_1",
			"move": 0
		}
	print (game.check_move(json.dumps(move)))

if __name__ == "__main__":
	main()
