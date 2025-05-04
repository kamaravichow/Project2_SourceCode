import os
import time
from typing import Dict, List, Optional, Tuple

from game_engine import GameEngine, Player, SuggestionRecord
from game_setup import (
    build_mansion,
    define_adjacency,
    define_characters,
    define_weapons,
)
from models import Character, Room, Weapon


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def setup_game(player_names: List[str]) -> GameEngine:
    """Initialize the game and return a GameEngine instance."""
    rooms = build_mansion()
    adjacency = define_adjacency(rooms)
    suspects = define_characters(rooms)
    weapons = define_weapons()
    
    return GameEngine(
        player_names=player_names,
        suspects=suspects,
        weapons=weapons,
        rooms=rooms,
        adjacency=adjacency,
    )


def print_board(engine: GameEngine):
    """Display the game board and player positions."""
    print("\n=== MANSION LAYOUT ===\n")
    
    # Print each room and who's in it
    for room_name, room in engine.rooms.items():
        players_in_room = [p for p in engine.players if p.current_room == room and p.active]
        player_names = ", ".join([p.name for p in players_in_room])
        
        if players_in_room:
            print(f"📍 {room.name}: {player_names}")
        else:
            print(f"   {room.name}")
    
    # Print adjacency (possible moves) for current player
    current_player = engine.get_current_player()
    possible_moves = engine.get_possible_moves(current_player)
    
    if current_player.current_room and possible_moves:
        print(f"\nFrom {current_player.current_room.name}, you can move to:")
        for i, room in enumerate(possible_moves, 1):
            print(f"  {i}. {room.name}")


def print_player_status(player: Player):
    """Display a player's current status."""
    print(f"\n=== {player.name}'s TURN ===")
    if player.character:
        print(f"You are playing as {player.character.name}")
    print(f"You are currently in the {player.current_room.name if player.current_room else 'hallway'}")
    
    print("\nYour hand:")
    for card in player.hand:
        print(f"  - {card.name}")


def print_suggestion_history(suggestions: List[SuggestionRecord]):
    """Display the history of suggestions and refutations."""
    if not suggestions:
        print("\nNo suggestions have been made yet.")
        return
        
    print("\n=== SUGGESTION HISTORY ===\n")
    for i, record in enumerate(suggestions, 1):
        print(f"{i}. {record.suggester} suggested: {record.suspect.name} with the {record.weapon.name} in the {record.room.name}")
        if record.refuter:
            print(f"   → Refuted by {record.refuter}")
        else:
            print(f"   → No one could refute!")


def get_room_choice(rooms: List[Room]) -> Optional[Room]:
    """Let player choose a room from a list."""
    while True:
        try:
            choice = input("Enter room number (or 'c' to cancel): ")
            if choice.lower() == 'c':
                return None
                
            idx = int(choice) - 1
            if 0 <= idx < len(rooms):
                return rooms[idx]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number or 'c' to cancel.")


def get_card_choice(cards: List, prompt: str) -> Optional:
    """Let player choose a card from a list."""
    print(prompt)
    for i, card in enumerate(cards, 1):
        print(f"  {i}. {card.name}")
        
    while True:
        try:
            choice = input("Enter number (or 'c' to cancel): ")
            if choice.lower() == 'c':
                return None
                
            idx = int(choice) - 1
            if 0 <= idx < len(cards):
                return cards[idx]
            else:
                print("Invalid choice. Try again.")
        except ValueError:
            print("Please enter a number or 'c' to cancel.")


def make_suggestion(engine: GameEngine, player: Player) -> None:
    """Allow a player to make a suggestion."""
    if not player.current_room:
        print("You must be in a room to make a suggestion.")
        return
    
    print("\n=== MAKE A SUGGESTION ===")
    print(f"You are suggesting a murder in the {player.current_room.name}")
    
    # Choose suspect
    suspect = get_card_choice(engine.suspects, "Choose a suspect:")
    if not suspect:
        return
    
    # Choose weapon
    weapon = get_card_choice(engine.weapons, "Choose a weapon:")
    if not weapon:
        return
        
    print(f"\nYou suggest that {suspect.name} committed the murder")
    print(f"with the {weapon.name} in the {player.current_room.name}")
    
    # Process suggestion
    record = engine.handle_suggestion(
        suggester=player.name,
        suspect=suspect,
        weapon=weapon,
        room=player.current_room
    )
    
    input("\nPress Enter to continue...")
    clear_screen()
    
    print(f"You suggested that {suspect.name} committed the murder")
    print(f"with the {weapon.name} in the {player.current_room.name}")
    
    if record.refuter:
        if record.refuter == player.name:
            # If the suggesting player is also refuting (has one of the cards)
            print(f"\nYou have one of these cards in your hand!")
        else:
            if record.shown_card and record.refuter == engine.get_current_player().name:
                print(f"\n{record.refuter} showed you the {record.shown_card.name} card")
            else:
                print(f"\n{record.refuter} refuted your suggestion but kept their card hidden")
    else:
        print("\nNo one could refute your suggestion!")
    
    input("\nPress Enter to continue...")


def make_accusation(engine: GameEngine, player: Player) -> None:
    """Allow a player to make an accusation."""
    print("\n=== MAKE AN ACCUSATION ===")
    print("WARNING: If you're wrong, you will be eliminated from the game!")
    print("Are you sure you want to make an accusation? (y/n)")
    
    if input("> ").lower() != 'y':
        return
    
    # Choose suspect
    suspect = get_card_choice(engine.suspects, "Who committed the murder?")
    if not suspect:
        return
    
    # Choose weapon
    weapon = get_card_choice(engine.weapons, "What was the murder weapon?")
    if not weapon:
        return
    
    # Choose room
    room = get_card_choice(list(engine.rooms.values()), "Where was the murder committed?")
    if not room:
        return
    
    print(f"\nYou accuse {suspect.name} of committing the murder")
    print(f"with the {weapon.name} in the {room.name}")
    print("\nChecking your accusation...")
    time.sleep(2)  # Dramatic pause
    
    # Process accusation
    correct = engine.handle_accusation(
        player=player,
        suspect=suspect,
        weapon=weapon,
        room=room
    )
    
    if correct:
        print("\n🎉 CONGRATULATIONS! 🎉")
        print("Your accusation was correct! You've solved the murder!")
    else:
        print("\n❌ Your accusation was incorrect! ❌")
        print("You are now eliminated from making accusations.")
    
    input("\nPress Enter to continue...")


def player_turn(engine: GameEngine) -> None:
    """Handle a single player's turn."""
    player = engine.get_current_player()
    
    if not player.active:
        print(f"\n{player.name}'s turn is skipped (eliminated)")
        time.sleep(1)
        engine.next_player()
        return
    
    while True:
        clear_screen()
        print_board(engine)
        print_player_status(player)
        
        print("\nOptions:")
        print("  1. Move to a room")
        print("  2. Make a suggestion")
        print("  3. Make an accusation")
        print("  4. View suggestion history")
        print("  5. End your turn")
        
        choice = input("\nWhat would you like to do? ")
        
        if choice == '1':  # Move
            possible_moves = engine.get_possible_moves(player)
            if not possible_moves:
                print("No valid moves available.")
                input("Press Enter to continue...")
                continue
                
            room = get_room_choice(possible_moves)
            if room:
                engine.move_player(player, room)
                print(f"You moved to the {room.name}")
                input("Press Enter to continue...")
            
        elif choice == '2':  # Suggest
            make_suggestion(engine, player)
            
        elif choice == '3':  # Accuse
            make_accusation(engine, player)
            if engine.game_over:
                return
            
        elif choice == '4':  # History
            clear_screen()
            print_suggestion_history(engine.suggestions)
            input("\nPress Enter to continue...")
            
        elif choice == '5':  # End turn
            engine.next_player()
            break
            
        else:
            print("Invalid option. Try again.")
            input("Press Enter to continue...")


def get_player_names() -> List[str]:
    """Get the names of the players."""
    while True:
        try:
            count = int(input("How many players (3-6)? "))
            if 3 <= count <= 6:
                break
            print("Please enter a number between 3 and 6.")
        except ValueError:
            print("Please enter a valid number.")
    
    names = []
    for i in range(count):
        while True:
            name = input(f"Enter name for Player {i+1}: ").strip()
            if name and name not in names:
                names.append(name)
                break
            print("Please enter a unique non-empty name.")
    
    return names


def display_solution(engine: GameEngine):
    """Display the correct solution."""
    suspect, weapon, room = engine.solution
    
    print("\n=== THE SOLUTION ===\n")
    print(f"The murder was committed by {suspect.name}")
    print(f"with the {weapon.name}")
    print(f"in the {room.name}")


def main():
    clear_screen()
    print("==== WELCOME TO CLUE/CLUEDO ====\n")
    print("A murder has been committed in the mansion!")
    print("Your task is to figure out WHO did it, with WHAT weapon, and WHERE.\n")
    
    player_names = get_player_names()
    engine = setup_game(player_names)
    
    clear_screen()
    print("Game initialized! Let the investigation begin!\n")
    
    # Game loop
    while not engine.game_over:
        player_turn(engine)
    
    # Game over
    clear_screen()
    if engine.winner:
        print(f"\n🎉 GAME OVER! {engine.winner} has solved the case! 🎉")
    else:
        print("\n😔 GAME OVER! All players have been eliminated!")
    
    display_solution(engine)
    
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
