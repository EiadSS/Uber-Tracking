"""Dispatcher for the simulation"""

from typing import Optional
from driver import Driver
from passenger import Passenger


class Dispatcher:
    """A dispatcher fulfills requests from passengers and drivers for a
    ride-sharing service.

    When a passenger requests a driver, the dispatcher assigns a driver to the
    passenger. If no driver is available, the passenger is placed on a waiting
    list for the next available driver. A passenger that has not yet been
    picked up by a driver may cancel their request.

    When a driver requests a passenger, the dispatcher assigns a passenger from
    the waiting list to the driver. If there is no passenger on the waiting list
    the dispatcher does nothing. Once a driver requests a passenger, the driver
    is registered with the dispatcher, and will be used to fulfill future
    passenger requests.

     === Attributes ===
    queue: A list of passengers of who is waiting for a driver.

    === Private Attributes ===
    _drivers:
        A dictionary whose key is driver.id, and value is the driver
    _waiting_passengers:
        A list of passengers waiting to be assigned a driver.
    """

    _drivers: dict[str, Driver]
    _waiting_passengers: list[Passenger]
    queue: list[Passenger]

    def __init__(self) -> None:
        """Initialize a Dispatcher.
        >>> eiad = Dispatcher()
        >>> print(eiad._drivers)
        {}
        """
        self._drivers = {}
        self._waiting_passengers = []
        self.queue = []

    def __str__(self) -> str:
        """Return a string representation.

        """
        return '{self._drivers}, {self._waiting_passengers}'.format(self=self)

    def request_driver(self, passenger: Passenger) -> Optional[Driver]:
        """Return a driver for the passenger, or None if no driver is available.

        Add the passenger to the waiting list if there is no available driver.
        """
        if len(self._drivers) == 0:
            self._waiting_passengers.insert(0, passenger)
            self.queue.insert(0, passenger)
            return None
        else:
            final_drive = list(self._drivers.values())[0]
            for x in self._drivers:
                driver = self._drivers[x]
                if driver.get_travel_time(passenger.origin) < \
                        final_drive.get_travel_time(passenger.origin):
                    final_drive = driver
            return final_drive

    def cancel_ride(self, passenger: Passenger) -> None:
        """Cancel the ride for passenger.

        """
        if passenger in self._waiting_passengers:
            y = []
            for x in range(len(self._waiting_passengers)):
                if self._waiting_passengers[x] == passenger:
                    y.append(x)
            c = 0
            for i in y:
                self._waiting_passengers.pop(i - c)
                c += 1

    def request_passenger(self, driver: Driver) -> Optional[Passenger]:
        """Return a passenger for the driver, or None if no passenger is availab

        If this is a new driver, register the driver for future passenger reques
        """
        if driver.id not in self._drivers:
            self._drivers[driver.id] = driver
        if not self.queue:
            return None
        else:
            return self.queue.pop()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['typing', 'driver', 'passenger']})
