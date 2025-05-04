from dataclasses import dataclass


@dataclass(frozen=True)
class Room:
    name: str


@dataclass(frozen=True)
class Character:
    name: str
    start_room: Room


@dataclass(frozen=True)
class Weapon:
    name: str
