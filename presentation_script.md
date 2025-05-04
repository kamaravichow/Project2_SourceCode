# Clue/Cluedo Game Presentation Script

## Introduction

"Hello everyone! Today I'll be demonstrating a text-based implementation of the classic board game Clue, also known as Cluedo in some countries. This implementation features all the core mechanics of the original game, including player movement, making suggestions, gathering clues, and finally making an accusation to solve the mystery."

## Game Overview

"In Clue, a murder has taken place in a mansion, and the players are tasked with figuring out WHO committed the murder, with WHAT weapon, and WHERE in the mansion. Let me show you how this digital version works."

## Running the Demo

"I'll be using a guided demo that showcases all the game's features. Let's start by running the demo script:"

```
python src/demo.py
```

## Key Features to Highlight

### 1. Game Setup & Board Layout

"As you can see, the game initializes with:
- A mansion with 9 different rooms
- 6 suspects with their starting positions
- 6 possible murder weapons
- Each player is dealt a hand of cards

The game tracks where everyone is located, and you can see that information displayed on the board."

### 2. Player Movement

"On my turn, I can see which rooms I can move to from my current location. Let me demonstrate by moving to a new room."

[Select option 1 to move to a room]

"Notice how I can only move to rooms that are adjacent to my current location, following the mansion's layout. This is just like the physical board game where you have to follow the paths between rooms."

### 3. Making Suggestions

"Now that I'm in a new room, I can make a suggestion. This is how players gather information in Clue."

[Select option 2 to make a suggestion]

"When making a suggestion, I must use my current room as the location, but I can choose any suspect and weapon. The game will then check if any player can refute my suggestion by showing they have one of the cards I mentioned."

### 4. Tracking Suggestion History

"The game keeps track of all suggestions made during play. This information is crucial for deduction."

[Select option 4 to view suggestion history]

"This history shows what suggestions were made and who refuted them. Over time, this helps players eliminate possibilities and narrow down the solution."

### 5. AI Players

"Let me end my turn to show how other players take their turns."

[Select option 5 to end your turn]

"The AI players follow the same rules - they move to adjacent rooms and make suggestions. Their actions also provide information that all players can use for deduction."

### 6. Making an Accusation

"When a player believes they've figured out the solution, they can make an accusation. If correct, they win the game. If incorrect, they're eliminated from making future accusations."

[Select option 3 to make an accusation]

"For this demo, I'll make the correct accusation to show you how the game concludes."

## Game Architecture

"Let me briefly explain the technical architecture of the game:

1. **Models** - Basic data structures for rooms, characters, and weapons
2. **Game Engine** - Core game logic, suggestion handling, and deduction system
3. **User Interface** - Text-based interface for player interaction
4. **Game Loop** - Manages turn-based gameplay and win conditions"

## Conclusion

"This implementation demonstrates all the essential elements of Clue:
- Room navigation and player movement
- Making and refuting suggestions
- Tracking information for deduction
- Making accusations to solve the case

The game can be played with 3-6 human players, making it suitable for classroom or family settings. Thank you for watching this demonstration!"

## Q&A Preparation

Common questions you might receive:

### How did you implement the deduction system?
"The game tracks all possible owners for each card. When players refute suggestions, we eliminate possibilities until only one owner remains for certain cards."

### How does the game handle incorrect accusations?
"If a player makes an incorrect accusation, they remain in the game but can no longer make accusations. They can still move and make suggestions to help other players."

### Could this be extended with a graphical interface?
"Absolutely! The game engine is separate from the user interface, so it would be straightforward to add a graphical layer using Pygame or another library while keeping the core logic intact."

### How did you ensure the game is balanced?
"The game follows the rules of traditional Clue closely, which has stood the test of time as a well-balanced game. Card dealing is randomized but ensures fair distribution among players."
