import pygame
from src.Game import Game

def main():
	game = Game()
	game.shuffle_deck()
	names = ["player_1", "player_2", "player_3", "player_4"]
	game.set_starting_hands(names)
	print (game.player_hands)

if __name__ == "__main__":
	main()
