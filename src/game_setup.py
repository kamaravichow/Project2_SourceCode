import random

from models import Character, Room, Weapon


def build_mansion() -> dict[str, Room]:
    """
    Create all rooms in the mansion.
    """
    names = [
        "Kitchen",
        "Ballroom",
        "Conservatory",
        "Dining Room",
        "Billiard Room",
        "Library",
        "Lounge",
        "Hall",
        "Study",
    ]
    return {name: Room(name) for name in names}


def define_adjacency(rooms: dict[str, Room]) -> dict[Room, list[Room]]:
    """
    Define which rooms connect to each other (including secret passages).
    """
    adj = {
        rooms["Kitchen"]: [
            rooms["Ballroom"],
            rooms["Dining Room"],
            rooms["Study"],
        ],  # secret to Study
        rooms["Ballroom"]: [
            rooms["Kitchen"],
            rooms["Conservatory"],
            rooms["Billiard Room"],
        ],
        rooms["Conservatory"]: [
            rooms["Ballroom"],
            rooms["Library"],
            rooms["Lounge"],
        ],  # secret to Lounge
        rooms["Dining Room"]: [
            rooms["Kitchen"],
            rooms["Billiard Room"],
            rooms["Lounge"],
        ],
        rooms["Billiard Room"]: [
            rooms["Dining Room"],
            rooms["Ballroom"],
            rooms["Hall"],
            rooms["Library"],
        ],
        rooms["Library"]: [
            rooms["Billiard Room"],
            rooms["Conservatory"],
            rooms["Study"],
        ],
        rooms["Lounge"]: [rooms["Dining Room"], rooms["Hall"], rooms["Conservatory"]],
        rooms["Hall"]: [rooms["Lounge"], rooms["Billiard Room"], rooms["Study"]],
        rooms["Study"]: [
            rooms["Hall"],
            rooms["Library"],
            rooms["Kitchen"],
        ],  # secret to Kitchen
    }
    return adj


def define_characters(rooms: dict[str, Room]) -> list[Character]:
    """
    Instantiate all suspects with their starting rooms.
    """
    start_positions = {
        "Miss Scarlett": "Lounge",
        "Colonel Mustard": "Dining Room",
        "Mrs. White": "Kitchen",
        "Mr. Green": "Hall",
        "Mrs. Peacock": "Conservatory",
        "Professor Plum": "Study",
    }
    return [Character(name, rooms[start_positions[name]]) for name in start_positions]


def define_weapons() -> list[Weapon]:
    """
    Instantiate all weapons.
    """
    names = ["Candlestick", "Revolver", "Rope", "Lead Pipe", "Wrench", "Knife"]
    return [Weapon(name) for name in names]


def choose_solution(
    characters: list[Character], weapons: list[Weapon], rooms: dict[str, Room]
) -> tuple[Character, Weapon, Room]:
    """
    Randomly select the murderer, weapon, and room for the secret solution.
    """
    culprit = random.choice(characters)
    murder_weapon = random.choice(weapons)
    murder_room = random.choice(list(rooms.values()))
    return culprit, murder_weapon, murder_room


if __name__ == "__main__":
    rooms = build_mansion()
    adjacency = define_adjacency(rooms)
    suspects = define_characters(rooms)
    weapons = define_weapons()
    solution = choose_solution(suspects, weapons, rooms)
    print("🔍 Solution (secret):", solution)
