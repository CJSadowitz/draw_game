# Draw Game
A very shoddy card game
## Rules
- Each player will draw a large portion of the deck {*Still need to determine this*}
- Deck has a size of {*Still need to determine this*}
- Max player count {*Still need to determine this*}
- Every card is sorted by type in each person's hand
- The top card of each type is known to every player
- The number of cards a person has is known only to the owner
- A card can only be played if its the same type or number
- A wild +4 card can only be played if their is no legal move or the only legal move is to draw
- A wild card can be played at any time
- When drawing, the player will continue until they get a playable card
- If the player draws a playable card, they can chose to play or keep the card
- If the player does not have a legal move, they lose and their hand is return to the deck
- If a player runs out of cards, then they win
- Play continues until all positions are determined
</br>

## Installation
This game runs off of python, using pygame to render the screen </br>

### Download Repo
To build the game: </br>
Download the repository: `git clone https://github.com/CJSadowitz/draw_game.git` </br>

### Setup Python
Ensure that python is downloaded on your machine with: `python` </br>
Create a virtual environment: `python3 -m venv venv` </br>
Activate virtual environment: `source venv/bin/activate` </br>

### Install Dependencies
This game uses pygame and moderngl to render the screen. As such it may not render on Mac OS </br>
After activating the venv: `pip install -r requirements.txt` </br>

## To Play
After activating the venv: `python3 main.py` </br>
