import unittest
from app import app, taxis, Booking

class TestTaxiBooking(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Reset taxis and bookings before each test
        for taxi in taxis:
            taxi.current_point = 'A'
            taxi.free_time = 0
            taxi.earnings = 0
            taxi.bookings = []
        Booking.id_counter = 1

    def test_scenario_1(self):
        # Input 1
        response = self.app.post('/', data={
            'cid': '1',
            'pickup': 'A',
            'drop': 'B',
            'ptime': '9'
        })
        self.assertIn(b"Taxi-1 is allotted", response.data)
        
        # Verify Taxi-1 state after Input 1
        # Pickup A, Drop B. Distance 15km. Fare 100 + (10*10) = 200.
        # Travel A->B is 1 hr. Pickup 9, Drop 10.
        taxi1 = taxis[0]
        self.assertEqual(taxi1.earnings, 200)
        self.assertEqual(taxi1.current_point, 'B')
        self.assertEqual(taxi1.free_time, 10)

        # Input 2
        response = self.app.post('/', data={
            'cid': '2',
            'pickup': 'B',
            'drop': 'D',
            'ptime': '9'
        })
        # Taxi-1 is busy until 10. Taxi-2 (at A) is free.
        # Taxi-2 to B is 15km.
        self.assertIn(b"Taxi-2 is allotted", response.data)

        # Verify Taxi-2 state after Input 2
        # Pickup B, Drop D. Distance 30km. Fare 100 + (25*10) = 350.
        # Travel B->D is 2 hr. Pickup 9, Drop 11.
        taxi2 = taxis[1]
        self.assertEqual(taxi2.earnings, 350)
        self.assertEqual(taxi2.current_point, 'D')
        self.assertEqual(taxi2.free_time, 11)

        # Input 3
        response = self.app.post('/', data={
            'cid': '3',
            'pickup': 'B',
            'drop': 'C',
            'ptime': '12'
        })
        # Taxi-1 (at B, free 10, earns 200)
        # Taxi-2 (at D, free 11, earns 350)
        # Pickup at B.
        # Taxi-1 dist to B: 0. Earnings 200.
        # Taxi-2 dist to B: 30km (D->B). Earnings 350.
        # Taxi-1 should be chosen (closer + lower earnings anyway)
        self.assertIn(b"Taxi-1 is allotted", response.data)

        # Verify Taxi-1 state after Input 3
        # Pickup B, Drop C. Distance 15km. Fare 100 + (10*10) = 200.
        # Travel B->C is 1 hr. Pickup 12, Drop 13.
        # Total Earnings: 200 + 200 = 400.
        self.assertEqual(taxi1.earnings, 400)
        self.assertEqual(taxi1.current_point, 'C')
        self.assertEqual(taxi1.free_time, 13)

if __name__ == '__main__':
    unittest.main()
