import pytest

from hypothesis import given
from hypothesis.strategies import integers, lists

from location import Location, deserialize_location, manhattan_distance
from event import create_event_list, PassengerRequest, DriverRequest, Pickup, \
    Dropoff, Cancellation
from monitor import Monitor, Activity, DRIVER, PASSENGER, PICKUP, DROPOFF, \
    CANCEL, REQUEST
from dispatcher import Dispatcher
from simulation import Simulation
from container import PriorityQueue
from passenger import Passenger
from driver import Driver


def test_location_print() -> None:
    """ Tests for the correct implementation of the creating and print of the
    Location class
    """
    location = Location(0, 0)
    assert str(location) == "(0, 0)"
    location2 = deserialize_location("2, 2")
    assert str(location2) == "(2, 2)"


def test_event_creation() -> None:
    """ Test for correct implementation of the event creations

    """
    events = create_event_list("events.txt")
    assert (len(events), 12)
    for event in events:
        instance = isinstance(event, PassengerRequest) or isinstance(event,
                                                                     DriverRequest)
        assert (instance, True)
    driverRequest = events[0]
    assert driverRequest.timestamp == 0
    passengerRequest = events[-1]
    assert passengerRequest.timestamp == 25


def test_simulation_run() -> None:
    """Test simulation run on a basic set of events"""
    events = create_event_list("events.txt")

    assert len(events) == 12
    sim = Simulation()
    report = sim.run(events)
    assert len(report) == 3
    assert report['average_passenger_wait_time'] == pytest.approx(0.5)
    assert report['average_driver_total_distance'] == pytest.approx(4.5)
    assert report['average_driver_trip_distance'] == pytest.approx(
        3.8333333333333335)


def test_special_events() -> None:
    """Test Cancellation and Pickup on a basic set of events"""

    # Environment Setup
    events = create_event_list("events.txt")
    dvr_request, psg_request = events[0], events[-1]
    driver, passenger = dvr_request.driver, psg_request.passenger
    monitor = Monitor()
    dispatcher = Dispatcher()
    dvr_request.do(dispatcher, monitor)
    psg_request.do(dispatcher, monitor)

    # Testing
    trip = Pickup(0, passenger, driver)
    dropoff = trip.do(dispatcher, monitor)

    assert isinstance(dropoff[0], Dropoff) == True
    assert passenger.status == 'satisfied'

    # ES
    events = create_event_list("events.txt")
    dvr_request, psg_request = events[1], events[-2]
    driver, passenger = dvr_request.driver, psg_request.passenger
    monitor = Monitor()
    dispatcher = Dispatcher()
    dvr_request.do(dispatcher, monitor)
    psg_request.do(dispatcher, monitor)

    # Testing
    cancel = Cancellation(0, passenger)
    result = cancel.do(dispatcher, monitor)
    assert result == []
    assert passenger.status == 'cancelled'


def test_container_adds() -> None:
    """Test the adding and removing of events in a priorityqueue"""
    egad = PriorityQueue()
    assert egad._items == []
    egad.add("bruh")
    egad.add("idk")
    egad.add("lol")
    assert egad._items == ["bruh", "idk", "lol"]
    egad.add("cro")
    assert egad._items == ["bruh", "cro", "idk", "lol"]
    egad.remove()
    assert egad._items == ["cro", "idk", "lol"]
    egad.add("lol")
    assert egad._items == ["cro", "idk", "lol", "lol"]
    egad.add("bro")
    assert egad._items == ["bro", "cro", "idk", "lol", "lol"]
    egad.remove()
    egad.remove()
    assert egad._items == ["idk", "lol", "lol"]
    egad.add("z")
    assert egad._items == ["idk", "lol", "lol", "z"]
    egad.remove()
    egad.remove()
    assert egad._items == ["lol", "z"]
    egad.add("mon")
    assert egad._items == ["lol", "mon", "z"]
    egad.remove()
    egad.remove()
    egad.remove()
    assert egad._items == []


def test_container_add_nice() -> None:
    bob = PriorityQueue()
    bob.add(2)
    bob.add(1)
    assert bob._items == [1, 2]
    bob.add(4)
    bob.add(3)
    assert bob._items == [1, 2, 3, 4]
    bob.add(7)
    bob.add(5)
    assert bob._items == [1, 2, 3, 4, 5, 7]
    bob.remove()
    bob.add(1)
    assert bob._items == [1, 2, 3, 4, 5, 7]
    eiad = PriorityQueue()
    assert len(eiad._items) == 0
    eiad.add(2)
    assert eiad._items == [2]
    eiad.add(3)
    assert eiad._items == [2, 3]
    eiad.add(4)
    assert eiad._items == [2, 3, 4]
    eiad.add(4)
    assert eiad._items == [2, 3, 4, 4]
    eiad.add(4)
    assert eiad._items == [2, 3, 4, 4, 4]
    eiad.remove()
    eiad.remove()
    eiad.add(4)
    assert eiad._items == [4, 4, 4, 4]


@given(integers())
def test_container_property_none(n1: int) -> None:
    eiad = PriorityQueue()
    assert eiad.add(n1) is None


@given(lists(integers()), integers())
def test_new_item_count(lst: list[int], n1: int) -> None:
    """Test that the correct number of items is added.
    """
    eiad = PriorityQueue()
    y = len(eiad._items)
    for x in lst:
        eiad.add(x)
        y += 1
    eiad.add(n1)
    y += 1

    assert len(eiad._items) == y


def test_location_str() -> None:
    """Test the string comprehension of location instances"""
    eiad = Location(0, 0)
    assert str(eiad) == "(0, 0)"


def test_location_eq() -> None:
    bruh = Location(0, 0)
    eiad = Location(0, 0)
    assert (eiad == bruh) is True
    idk = Location(1, 2)
    assert (eiad == idk) is False
    idk = Location(0, 0)
    assert (eiad == idk) is True
    idk = Location(1, 0)
    assert (eiad == idk) is False
    idk = Location(0, 1)
    assert (eiad == idk) is False
    idk = Location(1, 1)
    eiad = Location(1, 1)
    assert (eiad == idk) is True
    idk = 1
    assert (eiad == idk) is False


@given(integers(), integers(), integers(), integers())
def test_location_hatman(n1: int, n2: int, n3: int, n4: int) -> None:
    """Test that the correct number of items is added.
    """
    eiad = Location(abs(n1), abs(n2))
    bruh = Location(abs(n3), abs(n4))
    assert manhattan_distance(eiad, bruh) == abs(abs(n4) - abs(n2)) + \
           abs(abs(n3) - abs(n1))


@given(integers(), integers())
def test_location_deser(n1: int, n2: int) -> None:
    """Test that the correct number of items is added.
    """
    x = abs(n1)
    y = abs(n2)
    idk = '{n1},{n2}'.format(n1=x, n2=y)
    bruh = deserialize_location(idk)
    eiad = Location(x, y)
    assert bruh == eiad


def test_location_lize() -> None:
    """test cases to make sure desrelaize works correctly"""
    assert deserialize_location("3,4") == Location(3, 4)
    assert deserialize_location("(100000000,4294729479)") == \
           Location(100000000, 4294729479)


def test_passenger_hypeq() -> None:
    eiad = Passenger("bruh", 2, Location(1, 3), Location(1, 2))
    idk = Passenger("bruh", 2, Location(1, 3), Location(1, 2))
    assert (eiad == idk) is True
    idk.origin = Location(5, 4)
    assert (eiad == idk) is False
    idk.origin = Location(1, 3)
    idk.destination = Location(5, 4)
    assert (eiad == idk) is False
    idk.destination = Location(1, 2)
    idk.id = '12'
    assert (eiad == idk) is False
    idk.id = "bruh"
    idk.patience = 3
    assert (eiad == idk) is False
    assert (idk == 2) is False
    idk.patience = 2
    assert (idk == eiad) is True


def test_driver_eq() -> None:
    eiad = Driver("lol", Location(1, 2), 3)
    bro = Driver("lol", Location(1, 2), 3)
    assert (eiad == 1) is False
    assert (eiad == bro) is True
    bro.id = '12'
    assert (eiad == bro) is False
    bro.id = "lol"
    bro.location = Location(1, 1)
    assert (eiad == bro) is False
    bro.location = Location(1, 2)
    bro._speed = 2
    assert (eiad == bro) is False
    bro._speed = 3
    assert (eiad == bro) is True


@given(integers(), integers(), integers(), integers())
def test_driver_timetravle(n1: int, n2: int, n3, n4) -> None:
    x = Location(abs(n1), abs(n2))
    y = Driver('eiad', Location(abs(n3), abs(n4)), 3)
    assert isinstance(y.get_travel_time(x), int)


def test_driver_gettime() -> None:
    eiad = Driver('eiad', Location(0, 0), 2)
    assert eiad.get_travel_time(Location(3, 5)) == 4
    assert eiad.get_travel_time(Location(0, 5)) == 2
    assert eiad.get_travel_time(Location(3, 0)) == 2
    eiad.location = Location(2, 2)
    assert eiad.get_travel_time(Location(0, 0)) == 2
    assert eiad.get_travel_time(Location(2, 1)) == 0
    assert eiad.get_travel_time(Location(1, 2)) == 0
    assert eiad.get_travel_time(Location(2, 2)) == 0


@given(integers(), integers(), integers(), integers(), integers())
def test_drive_start_drive(n1, n2, n3, n4, n5) -> None:
    if n5 == 0:
        n5 += 1

    n1, n2, n3, n4, n5 = abs(n1), abs(n2), abs(n3), abs(n4), abs(n5)
    location = Location(n3, n4)
    eiad = Driver('eiad', Location(n1, n2), n5)
    assert isinstance(eiad.start_drive(location), int) is True
    assert eiad.is_idle is False


def test_dispathcer_requestdrive() -> None:
    eiad = Dispatcher()
    idk = Passenger('eiad', 3, Location(1, 2), Location(5, 2))
    assert eiad.request_driver(idk) is None
    assert eiad._waiting_passengers == [idk]


def test_dispathcer_requestpassenger() -> None:
    eiad = Dispatcher()
    idk = Passenger('idk', 3, Location(7, 7), Location(5, 2))
    damyan = Driver('damyan', Location(1, 1), 1)
    assert eiad.request_passenger(damyan) is None
    assert eiad._drivers == {'damyan': damyan}
    assert eiad.request_passenger(damyan) is None
    assert eiad._drivers == {'damyan': damyan}
    assert eiad.request_driver(idk) == eiad._drivers['damyan']
    assert eiad._waiting_passengers == []
    eiad._drivers.pop('damyan')
    assert eiad._drivers == {}
    assert eiad.cancel_ride(idk) is None
    assert eiad.request_driver(idk) is None
    assert eiad._waiting_passengers == [idk]
    assert eiad.request_passenger(damyan) == idk
    assert eiad._waiting_passengers == [idk]
    eiad._drivers.pop('damyan')
    bruh = Passenger('bruh', 2, Location(3, 3), Location(2, 1))
    assert eiad.request_driver(bruh) is None
    assert eiad.request_driver(idk) is None
    assert eiad._waiting_passengers == [idk, bruh, idk]
    assert eiad.request_passenger(damyan) == bruh
    assert eiad.request_passenger(damyan) == idk
    assert eiad.request_passenger(damyan) is None
    assert eiad.cancel_ride(idk) is None
    assert eiad._waiting_passengers == [bruh]
    eiad.cancel_ride(bruh)
    eiad.cancel_ride(idk)
    assert eiad._waiting_passengers == []
    assert eiad._drivers == {'damyan': damyan}
    nizar = Driver("nizar", Location(4, 6), 2)
    eiad.request_passenger(nizar)
    assert eiad._drivers == {'damyan': damyan, 'nizar': nizar}
    bill = Driver('bill', Location(7, 7), 1)
    eiad.request_passenger(bill)
    assert eiad.request_driver(idk) == bill


def test_monitor_avg_trip_dis() -> None:
    eiad = Monitor()
    eiad.notify(2, DRIVER, REQUEST, "Eiad", Location(1, 1))
    eiad.notify(5, DRIVER, PICKUP, "Eiad", Location(5, 3))
    eiad.notify(7, DRIVER, DROPOFF, "Eiad", Location(3, 3))
    assert eiad._average_total_distance() == 8
    assert eiad._average_trip_distance() == 2
    eiad.notify(3, DRIVER, PICKUP, "bruh", Location(1, 1))
    assert eiad._average_total_distance() == 4
    eiad.notify(5, DRIVER, CANCEL, "bruh", Location(6, 6))
    assert eiad._average_total_distance() == 9
    assert eiad._average_trip_distance() == 6


def test_learning_pop() -> None:
    eiad = LinkedList([1, 2, 3, 4])
    assert eiad.pop(0) == _Node(1)


if __name__ == '__main__':
    pytest.main(['sample_tests.py'])
