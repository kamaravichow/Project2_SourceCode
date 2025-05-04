#!/usr/bin/env python3
"""
Clue/Cluedo Game Demo
A demonstration version with automated players for presentation purposes.
"""

import os
import time
import random
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


def print_with_delay(text, delay=0.03):
    """Print text with a typewriter effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()


def setup_demo_game() -> GameEngine:
    """Initialize the game with predetermined values for demo purposes."""
    rooms = build_mansion()
    adjacency = define_adjacency(rooms)
    suspects = define_characters(rooms)
    weapons = define_weapons()
    
    # Use fixed player names for the demo
    player_names = ["You", "AI Player 1", "AI Player 2"]
    
    engine = GameEngine(
        player_names=player_names,
        suspects=suspects,
        weapons=weapons,
        rooms=rooms,
        adjacency=adjacency,
    )
    
    # For demo purposes, we'll know the solution to guide the demonstration
    solution_suspect, solution_weapon, solution_room = engine.solution
    
    return engine


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
    
    # Print adjacency for demo player
    demo_player = engine.get_player("You")
    possible_moves = engine.get_possible_moves(demo_player)
    
    if demo_player.current_room and possible_moves:
        print(f"\nFrom {demo_player.current_room.name}, you can move to:")
        for i, room in enumerate(possible_moves, 1):
            print(f"  {i}. {room.name}")


def print_player_status(player: Player):
    """Display a player's current status."""
    print(f"\n=== {player.name}'s TURN ===")
    if player.character:
        print(f"Playing as {player.character.name}")
    print(f"Currently in the {player.current_room.name if player.current_room else 'hallway'}")
    
    if player.name == "You":
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


def ai_player_turn(engine: GameEngine, step: int):
    """Simulate an AI player turn with predefined moves for the demo."""
    player = engine.get_current_player()
    
    print_with_delay(f"\n{player.name}'s turn...")
    time.sleep(1)
    
    # Demo AI just moves to an adjacent room and makes a suggestion
    possible_moves = engine.get_possible_moves(player)
    
    if possible_moves:
        # For demo purposes, we'll make a deterministic choice
        chosen_room = possible_moves[step % len(possible_moves)]
        print_with_delay(f"{player.name} moves to the {chosen_room.name}")
        engine.move_player(player, chosen_room)
        time.sleep(1)
        
        # Make a suggestion
        suspect = engine.suspects[step % len(engine.suspects)]
        weapon = engine.weapons[step % len(engine.weapons)]
        
        print_with_delay(f"{player.name} suggests that {suspect.name} committed the murder")
        print_with_delay(f"with the {weapon.name} in the {chosen_room.name}")
        
        record = engine.handle_suggestion(
            suggester=player.name,
            suspect=suspect,
            weapon=weapon,
            room=chosen_room
        )
        
        time.sleep(1)
        if record.refuter:
            print_with_delay(f"{record.refuter} refutes the suggestion.")
        else:
            print_with_delay("No player could refute this suggestion!")
    else:
        print_with_delay(f"{player.name} has no valid moves and skips their turn.")
    
    time.sleep(1)
    engine.next_player()
    input("\nPress Enter to continue...")


def demo_make_suggestion(engine: GameEngine):
    """Guided suggestion flow for demo purposes."""
    player = engine.get_player("You")
    
    print_with_delay("\n=== MAKE A SUGGESTION ===")
    print_with_delay(f"You are suggesting a murder in the {player.current_room.name}")
    
    # Display numbered list of suspects
    print("\nSuspects:")
    for i, suspect_option in enumerate(engine.suspects):
        print(f"  {i}. {suspect_option.name}")
    suspect_idx = int(input("Choose a suspect (enter number 0-5): ")) % len(engine.suspects)
    suspect = engine.suspects[suspect_idx]
    
    # Display numbered list of weapons
    print("\nWeapons:")
    for i, weapon_option in enumerate(engine.weapons):
        print(f"  {i}. {weapon_option.name}")
    weapon_idx = int(input("Choose a weapon (enter number 0-5): ")) % len(engine.weapons)
    weapon = engine.weapons[weapon_idx]
    
    print_with_delay(f"\nYou suggest that {suspect.name} committed the murder")
    print_with_delay(f"with the {weapon.name} in the {player.current_room.name}")
    
    # Process suggestion
    record = engine.handle_suggestion(
        suggester=player.name,
        suspect=suspect,
        weapon=weapon,
        room=player.current_room
    )
    
    time.sleep(1)
    clear_screen()
    
    print_with_delay(f"You suggested that {suspect.name} committed the murder")
    print_with_delay(f"with the {weapon.name} in the {player.current_room.name}")
    
    if record.refuter:
        if record.refuter == player.name:
            print_with_delay("\nYou have one of these cards in your hand!")
        else:
            if record.shown_card and record.refuter == engine.get_current_player().name:
                print_with_delay(f"\n{record.refuter} showed you the {record.shown_card.name} card")
            else:
                print_with_delay(f"\n{record.refuter} refuted your suggestion but kept their card hidden")
    else:
        print_with_delay("\nNo one could refute your suggestion!")
        print_with_delay("These cards might be in the solution!")
    
    input("\nPress Enter to continue...")


def demo_make_accusation(engine: GameEngine):
    """Guided accusation flow for demo purposes."""
    player = engine.get_player("You")
    
    # Get solution for demo purposes
    solution_suspect, solution_weapon, solution_room = engine.solution
    
    print_with_delay("\n=== MAKE AN ACCUSATION ===")
    print_with_delay("In a real game, an incorrect accusation would eliminate you.")
    
    print_with_delay("\nFor this demo, make the correct accusation:")
    print_with_delay(f"- Suspect: {solution_suspect.name}")
    print_with_delay(f"- Weapon: {solution_weapon.name}")
    print_with_delay(f"- Room: {solution_room.name}")
    
    # Display numbered lists for reference
    print("\nSuspects (for reference):")
    for i, suspect in enumerate(engine.suspects):
        print(f"  {i}. {suspect.name}")
        
    print("\nWeapons (for reference):")
    for i, weapon in enumerate(engine.weapons):
        print(f"  {i}. {weapon.name}")
        
    print("\nRooms (for reference):")
    for i, room in enumerate(list(engine.rooms.values())):
        print(f"  {i}. {room.name}")
    
    input("\nPress Enter to make this accusation...")
    
    print_with_delay(f"\nYou accuse {solution_suspect.name} of committing the murder")
    print_with_delay(f"with the {solution_weapon.name} in the {solution_room.name}")
    print_with_delay("\nChecking your accusation...")
    time.sleep(2)  # Dramatic pause
    
    # Always correct in demo mode
    engine.handle_accusation(
        player=player,
        suspect=solution_suspect,
        weapon=solution_weapon,
        room=solution_room
    )
    
    print_with_delay("\n🎉 CONGRATULATIONS! 🎉")
    print_with_delay("Your accusation was correct! You've solved the murder!")
    
    input("\nPress Enter to continue...")


def demo_player_turn(engine: GameEngine, step: int):
    """Guided player turn for the demo."""
    player = engine.get_player("You")
    
    while True:
        clear_screen()
        print_board(engine)
        print_player_status(player)
        
        print("\nDemo Options:")
        print("  1. Move to a room")
        print("  2. Make a suggestion")
        print("  3. Make an accusation")
        print("  4. View suggestion history")
        print("  5. End your turn")
        
        if step == 0:
            print("\nDEMO GUIDE: Start by moving to a new room (option 1)")
            choice = "1"
        elif step == 1:
            print("\nDEMO GUIDE: Now make a suggestion (option 2)")
            choice = "2"
        elif step == 2:
            print("\nDEMO GUIDE: View the suggestion history (option 4)")
            choice = "4"
        elif step == 3:
            print("\nDEMO GUIDE: End your turn to see AI players (option 5)")
            choice = "5"
        elif step == 4:
            print("\nDEMO GUIDE: Make a winning accusation (option 3)")
            choice = "3"
        else:
            choice = input("\nWhat would you like to do? ")
        
        if choice == '1':  # Move
            possible_moves = engine.get_possible_moves(player)
            if not possible_moves:
                print_with_delay("No valid moves available.")
                input("Press Enter to continue...")
                continue
            
            # For demo, choose first available room in step 0
            if step == 0:
                print_with_delay("\nChoosing the first available room for you...")
                room = possible_moves[0]
            else:
                # Let presenter choose in later steps
                print("\nAvailable rooms:")
                for i, room_option in enumerate(possible_moves, 1):
                    print(f"  {i}. {room_option.name}")
                room_idx = int(input("Choose room number: ")) - 1
                if 0 <= room_idx < len(possible_moves):
                    room = possible_moves[room_idx]
                else:
                    room = possible_moves[0]
            
            engine.move_player(player, room)
            print_with_delay(f"You moved to the {room.name}")
            input("Press Enter to continue...")
            
            if step == 0:
                return 1  # Progress to next step
            
        elif choice == '2':  # Suggest
            demo_make_suggestion(engine)
            if step == 1:
                return 2  # Progress to next step
            
        elif choice == '3':  # Accuse
            demo_make_accusation(engine)
            return -1  # End demo after accusation
            
        elif choice == '4':  # History
            clear_screen()
            print_suggestion_history(engine.suggestions)
            input("\nPress Enter to continue...")
            if step == 2:
                return 3  # Progress to next step
            
        elif choice == '5':  # End turn
            engine.next_player()
            if step == 3:
                return 4  # Progress to next step
            return step  # Don't progress otherwise
            
        else:
            print_with_delay("Invalid option. Try again.")
            input("Press Enter to continue...")


def display_solution(engine: GameEngine):
    """Display the correct solution."""
    suspect, weapon, room = engine.solution
    
    print_with_delay("\n=== THE SOLUTION ===\n")
    print_with_delay(f"The murder was committed by {suspect.name}")
    print_with_delay(f"with the {weapon.name}")
    print_with_delay(f"in the {room.name}")


def run_demo():
    """Run the guided demo."""
    clear_screen()
    print_with_delay("==== CLUE/CLUEDO GAME DEMO ====", delay=0.05)
    time.sleep(1)
    
    print_with_delay("\nThis demo will guide you through the main features of the game.")
    print_with_delay("Follow the prompts to showcase how the game works.")
    print_with_delay("\nIn this demo, you'll play as the first player against two AI opponents.")
    
    input("\nPress Enter to start the demo...")
    
    engine = setup_demo_game()
    
    # Demo steps guide the presenter through key features
    step = 0
    
    while not engine.game_over and step >= 0:
        current_player = engine.get_current_player()
        
        if current_player.name == "You":
            step = demo_player_turn(engine, step)
        else:
            ai_player_turn(engine, step)
    
    # Game over
    clear_screen()
    if engine.winner:
        print_with_delay(f"\n🎉 GAME OVER! {engine.winner} has solved the case! 🎉", delay=0.05)
    
    display_solution(engine)
    
    print_with_delay("\n==== END OF DEMO ====", delay=0.05)
    print_with_delay("\nKey features demonstrated:")
    print_with_delay("1. Game board and player movement")
    print_with_delay("2. Making suggestions and deductions")
    print_with_delay("3. Tracking suggestion history")
    print_with_delay("4. Making accusations")
    print_with_delay("5. Turn-based gameplay")
    
    print_with_delay("\nThank you for watching the Clue/Cluedo game demo!")


if __name__ == "__main__":
    run_demo()
