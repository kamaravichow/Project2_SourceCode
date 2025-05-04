import random
from dataclasses import dataclass
from typing import List, Dict, Set, Union, Optional, Tuple

from models import Character, Weapon, Room

# A Card can be a suspect, weapon, or room
Card = Union[Character, Weapon, Room]

@dataclass
class SuggestionRecord:
    suggester: str
    suspect: Character
    weapon: Weapon
    room: Room
    refuter: Optional[str] = None
    shown_card: Optional[Card] = None

class Player:
    def __init__(self, name: str, character: Character = None):
        self.name: str = name
        self.hand: List[Card] = []
        self.character: Character = character
        self.current_room: Optional[Room] = character.start_room if character else None
        self.notebook: Dict[str, Set[str]] = {}
        self.active: bool = True  # If False, player has made incorrect accusation

class GameEngine:
    def __init__(
        self,
        player_names: List[str],
        suspects: List[Character],
        weapons: List[Weapon],
        rooms: Dict[str, Room],
        adjacency: Dict[Room, List[Room]],
    ):
        # Store game board information
        self.suspects = suspects
        self.weapons = weapons
        self.rooms = rooms
        self.adjacency = adjacency

        # Choose secret solution
        self.solution: tuple[Character, Weapon, Room] = self.choose_solution(
            suspects, weapons, rooms
        )
        
        # Assign characters to players
        available_characters = suspects.copy()
        self.players: List[Player] = []
        self.player_order: List[str] = player_names.copy()
        
        for name in player_names:
            if available_characters:
                character = random.choice(available_characters)
                available_characters.remove(character)
                self.players.append(Player(name, character))
            else:
                # In case we have more players than characters
                self.players.append(Player(name))

        # Deal the remaining cards
        self._deal_cards(suspects, weapons, rooms)

        # Track possible owners for each card (players + CaseFile)
        all_cards: List[Card] = suspects + weapons + list(rooms.values())
        self.possible_owners: Dict[Card, Set[str]] = {
            card: set(player_names + ["CaseFile"])
            for card in all_cards
        }

        # History of all suggestions
        self.suggestions: List[SuggestionRecord] = []
        
        # Game state
        self.current_player_index: int = 0
        self.game_over: bool = False
        self.winner: Optional[str] = None

    @staticmethod
    def choose_solution(
        suspects: List[Character], weapons: List[Weapon], rooms: Dict[str, Room]
    ) -> tuple[Character, Weapon, Room]:
        culprit = random.choice(suspects)
        murder_weapon = random.choice(weapons)
        murder_room = random.choice(list(rooms.values()))
        return culprit, murder_weapon, murder_room

    def _deal_cards(
        self,
        suspects: List[Character],
        weapons: List[Weapon],
        rooms: Dict[str, Room],
    ) -> None:
        deck: List[Card] = suspects.copy() + weapons.copy() + list(rooms.values())
        # Remove solution cards
        for card in self.solution:
            deck.remove(card)
        random.shuffle(deck)
        n = len(self.players)
        for i, card in enumerate(deck):
            self.players[i % n].hand.append(card)

    def handle_suggestion(
        self,
        suggester: str,
        suspect: Character,
        weapon: Weapon,
        room: Room,
    ) -> SuggestionRecord:
        """
        Process a player's suggestion, allowing others to refute.
        Returns a record with refuter and shown_card if any.
        """
        record = SuggestionRecord(suggester, suspect, weapon, room)
        idx = self.player_order.index(suggester)
        n = len(self.players)
        # Ask each other player in turn
        for offset in range(1, n):
            player = self.players[(idx + offset) % n]
            # Find any matching card in hand
            matches = [c for c in player.hand if c in (suspect, weapon, room)]
            if matches:
                shown = random.choice(matches)
                record.refuter = player.name
                record.shown_card = shown
                # Deduction: only this player can own that card
                self.possible_owners[shown] = {player.name}
                break
        else:
            # No one could refute: all three are in the CaseFile
            for c in (suspect, weapon, room):
                self.possible_owners[c] = {"CaseFile"}
        self.suggestions.append(record)
        return record

    def deduce(self) -> Dict[str, str]:
        """
        Return any cards whose ownership is fully deduced (only one possible owner remains).
        """
        deductions: Dict[str, str] = {}
        for card, owners in self.possible_owners.items():
            if len(owners) == 1:
                deductions[card.name] = next(iter(owners))
        return deductions
        
    def get_player(self, player_name: str) -> Optional[Player]:
        """
        Find a player by name.
        """
        for player in self.players:
            if player.name == player_name:
                return player
        return None
        
    def get_current_player(self) -> Player:
        """
        Get the player whose turn it is.
        """
        return self.players[self.current_player_index]
        
    def next_player(self) -> Player:
        """
        Advance to the next active player.
        """
        original_index = self.current_player_index
        while True:
            self.current_player_index = (self.current_player_index + 1) % len(self.players)
            current_player = self.get_current_player()
            
            # If we've gone full circle and no active players, game is over
            if self.current_player_index == original_index and not current_player.active:
                self.game_over = True
                return current_player
                
            # Found an active player
            if current_player.active:
                return current_player
    
    def get_possible_moves(self, player: Player) -> List[Room]:
        """
        Get all rooms a player can move to from their current position.
        """
        if player.current_room is None:
            return []
        return self.adjacency.get(player.current_room, [])
    
    def move_player(self, player: Player, room: Room) -> bool:
        """
        Move a player to a new room if it's a valid move.
        Returns True if the move was successful.
        """
        if room in self.get_possible_moves(player):
            player.current_room = room
            return True
        return False
        
    def handle_accusation(self, 
                         player: Player, 
                         suspect: Character, 
                         weapon: Weapon, 
                         room: Room) -> bool:
        """
        Process a player's accusation.
        Returns True if the accusation is correct.
        """
        solution_suspect, solution_weapon, solution_room = self.solution
        
        correct = (suspect == solution_suspect and 
                  weapon == solution_weapon and 
                  room == solution_room)
                  
        if correct:
            # Game over, this player wins
            self.game_over = True
            self.winner = player.name
        else:
            # Player is eliminated from making future accusations
            player.active = False
            
        return correct
