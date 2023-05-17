"""Locations for the simulation"""

from __future__ import annotations


class Location:
    """A two-dimensional location.

    === Attributes ===
    row:
        A value representing the horizontal index
    col:
        A value representing the vertical index
    """
    row: int
    col: int

    def __init__(self, row: int, column: int) -> None:
        """Initialize a location.

        """
        self.row = row
        self.column = column

    def __str__(self) -> str:
        """Return a string representation.
        >>> bruh = Location(1, 2)
        >>> print(bruh)
        The location is row: 1, column: 2
        """
        return "({self.row}, {self.column})". \
            format(self=self)

    def __eq__(self, other: Location) -> bool:
        """Return True if self equals other, and false otherwise.

        """
        if isinstance(other, Location):
            return (self.row == other.row) and (self.column == other.column)
        return False


def manhattan_distance(origin: Location, destination: Location) -> int:
    """Return the Manhattan distance between the origin and the destination.
    >>> eiad = Location(3, 4)
    >>> bruh = Location(5, 7)
    >>> manhattan_distance(eiad, bruh)
    5
    >>> eiad = Location(1, 2)
    >>> bruh = Location(1, 0)
    >>> manhattan_distance(eiad, bruh)
    2
    """
    return abs(origin.row - destination.row) + abs(origin.column -
                                                   destination.column)


def deserialize_location(location_str: str) -> Location:
    """Deserialize a location.

    location_str: A location in the format 'row,col'
    >>> x = deserialize_location('3, 4')
    >>> print(x)
    (3, 4)
    """
    x = eval(location_str)
    return Location(int(x[0]), int(x[1]))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all()
