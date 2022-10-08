class BadPositionError(Exception):
    """Exception which occours if positions are overlapping in our models"""
    def __init__(self, object, bad_object, bad_position: tuple) -> None:
        super().__init__(f"Can't set/change {bad_object}, overlapping with {object} at {bad_position} ")

class PositionOutOfBoundsError(Exception):
    """Exception which occours if position changed to be outside of the room"""
    def __init__(self, room, bad_object, bad_position: tuple) -> None:
        super().__init__(f"Can't set/change {bad_object}, would be outside of {room} at {bad_position} ")

class PersonAlreadyPresentError(Exception):
    """Exception which occours if person gets added to list twice"""
    def __init__(self, list, person) -> None:
        index = list.index(person)
        super().__init__(f"Can't add/set {person} in list {list}, already present at index {index}")

class RoomResizeError(Exception):
    """Exception which occours if room would collide when resized"""
    def __init__(self, room, collide_object, size) -> None:
        super().__init__(f"Can't resize room {room} with {room.size} to {size}, because it would collide with {collide_object}")
    
    