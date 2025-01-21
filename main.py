import pygame
from src.Game import Game

def main():
	names = ["player_1", "player_2", "player_3", "player_4"]
	game = Game(names)
	game.shuffle_deck()
	game.set_starting_hands()
	print (game.get_game_state())

if __name__ == "__main__":
	main()
