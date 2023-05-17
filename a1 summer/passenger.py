"""
The passenger module contains the Passenger class. It also contains
constants that represent the status of the passenger.

=== Constants ===
WAITING: A constant used for the waiting passenger status.
CANCELLED: A constant used for the cancelled passenger status.
SATISFIED: A constant used for the satisfied passenger status
"""

from location import Location

WAITING = "waiting"
CANCELLED = "cancelled"
SATISFIED = "satisfied"


class Passenger:
    """A passenger for a trip-sharing service.

    === Attributes ===
    id:
        A unique identifier for the passenger.
    patience:
        The amount of time the passenger will wait for a driver.
    origin:
        The initial location of the passenger.
    destination:
        The destination for the passenger.
    status:
        The current status of the passenger.

    === Representation Invariants ===
    -  status: "waited" | "cancelled" | "satisfied"
    """
    id: str
    patience: int
    origin: Location
    destination: Location
    status: str

    def __init__(self, identifier: str, patience: int, origin: Location,
                 destination: Location) -> None:
        """Initialize a Passenger.
        >>> eiad = Passenger('123', 2, Location(1, 2), Location(4, 5))
        >>> eiad.origin.row
        1
        """
        self.id = identifier
        self.patience = patience
        self.origin = origin
        self.destination = destination
        self.status = WAITING

    def __eq__(self, other: object) -> bool:
        """
        >>> eiad = Passenger("bruh", 2, Location(1, 1), Location(2, 2))
        >>> bruh = Passenger("bruh", 2, Location(1, 1), Location(2, 2))
        >>> eiad == bruh
        True
        >>> x = 2
        >>> eiad == x
        False
        >>> lol = Passenger("bru", 2, Location(1, 1), Location(2, 2))
        >>> eiad == lol
        False
        """
        if isinstance(other, Passenger):
            return self.id == other.id and self.patience == other.patience and \
                   self.origin == other.origin and self.destination == \
                   other.destination and self.status == other.status
        return False

    def __str__(self):
        return "{self.id}".format(self=self)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['location']})
