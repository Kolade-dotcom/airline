from django.db.models import Max
from django.test import TestCase, Client
from .models import *

# Create your tests here.


class FlightTest(TestCase):
    def setUp(self) -> None:
        # Create some airports.
        a1 = Airport.objects.create(code="AAA", city="City A")
        a2 = Airport.objects.create(code="BBB", city="City B")

        # Create some fligths.
        Flight.objects.create(origin=a1, destination=a2, duration=200)
        Flight.objects.create(origin=a1, destination=a2, duration=-200)
        Flight.objects.create(origin=a2, destination=a1, duration=100)
        Flight.objects.create(origin=a1, destination=a1, duration=100)

        # Create client
        client = Client()

    def test_departures_count(self) -> None:
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self) -> None:
        a = Airport.objects.get(code="AAA")
        self.assertEqual(a.arrivals.count(), 2)

    def test_valid_flight(self) -> None:
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=200)
        self.assertTrue(f.is_valid_flight())

    def test_invalid_flight_destination(self) -> None:
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid_flight())

    def test_index(self) -> None:
        """Checks that page loaded successfully and there are only 3 flights available."""
        response = self.client.get("/flights/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["flights"].count(), 4)

    def test_valid_flights_page(self) -> None:
        """Checks that flight page loads for valid flight"""
        a1 = Airport.objects.get(code="AAA")
        f = Flight.objects.get(origin=a1, destination=a1)

        response = self.client.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flights_page(self) -> None:
        """Checks that flight page does not load for invalid flights"""
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]

        try:
            response = self.client.get(f"/flights/{max_id + 1}")
            self.assertEqual(response.status_code, 404)
        except Flight.DoesNotExist:
            pass

    def test_flight_page_passengers(self) -> None:
        """Checks that flight page loads and displays correct number of passengers for a flight with passengers."""
        f = Flight.objects.get(pk=1)
        p = Passenger.objects.create(first="Kolade", last="Salako")
        f.passengers.add(p)

        response = self.client.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_non_passengers(self) -> None:
        """Checks that flight page loads and displays correct number of non-passengers for a flight with non-passengers."""
        f = Flight.objects.get(pk=1)
        Passenger.objects.create(first="Kolade", last="Salako")

        response = self.client.get(f"/flights/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["non_passengers"].count(), 1)

    def test_invalid_flight_duration(self) -> None:
        a1 = Airport.objects.get(code="AAA")
        a2 = Airport.objects.get(code="BBB")
        f = Flight.objects.get(origin=a1, destination=a2, duration=-200)
        self.assertFalse(f.is_valid_flight())
