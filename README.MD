## Overview
This Python application sets up the initial state for a Cluedo (Clue) game:
- Builds the mansion layout with rooms and their connections.
- Defines the characters and their starting positions.
- Defines the weapons.
- Randomly selects a secret solution: the murderer, the weapon, and the crime scene.

## Prerequisites
- Python 3.9 or higher (uses `dataclasses` and modern type hints)

## Steps to Run

Navigate to the source code directory:
```bash
$ cd AravindKamani_Project2_SourceCode/src
```

Run the main script:
```bash
$ python main.py
```

Output:
```bash
Game initialized!

Rooms:
- Kitchen
- Ballroom
- Conservatory
- Dining Room
- Billiard Room
- Library
- Lounge
- Hall
- Study

Suspects:
- Mr. Boddy (starting in Kitchen)
- Mrs. White (starting in Ballroom)
- Mr. Green (starting in Conservatory)
- Mrs. Peacock (starting in Dining Room)
- Mr. Mustard (starting in Billiard Room)
- Miss Scarlett (starting in Library)

Weapons:
- Revolver
- Dagger
- Lead Pipe
- Candlestick
- Wrench
- revolver

🔍 Secret Solution (for debugging):
The murder was committed by **Miss Scarlett** in the **Kitchen** with the **Revolver**.
```
