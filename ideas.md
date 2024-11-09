# Game Concept Ideas:
## Entity Component System
Suppose I made this in an ECS style. </br>
Each person who wants to play the game could play any card game they want. </br>
I need to build a system that allows for the server to transfer a game config </br>
to each player who wants to play that game? </br>
Maybe make an easy editor such that any player can intuitively make a game? </br>
### Game play Entities
- Player
- Table
- Card
### All Components
- Hand *list of sorted cards*
- Score *score*
- Value *value of card*
- Type *what kind of card this is*
- Deck
- Turn
- Status
- Renderable
- Position
### Player Components
- Hand
- Score
- Turn Number
- Status
- Render Static
### Card Components
- Value
- Type
- Render Dynamic
### Table Components
- Deck
- Turn Counter
### System
**All Exectuable Actions** </br>
Every System actions upon entities using its components? </br>
All systems are ran on the server? Player just sends commands? </br>
- *Player* uses *Card*
- *Card* enters *Table*
- *Card* interacts *Player(s)*
- *Card* leaves *Table*
- *Player* gets *Card*
- Render *Players* and *Deck*
</br>
So is the Card the system that interacts between the player's and the table? </br>
But the Card can interact between the 1 or more players? </br>
