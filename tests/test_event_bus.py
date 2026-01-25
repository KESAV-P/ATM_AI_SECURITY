import unittest
from event_bus import generate_event, COOLDOWN_SECONDS, _last_triggered
import time

class TestEventBus(unittest.TestCase):
    def setUp(self):
        _last_triggered.clear()
        self.base_data = {
            "helmet": False,
            "mask": False,
            "sunglasses": False,
            "people_count": 1,
            "camera_blackout": False,
            "confidence": 0.0
        }

    def test_single_person_no_event(self):
        data = self.base_data.copy()
        events = generate_event(data)
        self.assertEqual(len(events), 0)

    def test_multiple_persons_trigger(self):
        data = self.base_data.copy()
        data["people_count"] = 2
        events = generate_event(data)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "MULTIPLE_PERSONS")
        self.assertEqual(events[0]["severity"], "HIGH")

    def test_helmet_trigger(self):
        data = self.base_data.copy()
        data["helmet"] = True
        events = generate_event(data)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["type"], "FACE_CONCEALMENT")

    def test_cooldown(self):
        data = self.base_data.copy()
        data["people_count"] = 2
        
        # First trigger
        events1 = generate_event(data)
        self.assertEqual(len(events1), 1)
        
        # Immediate second trigger (should be blocked)
        events2 = generate_event(data)
        self.assertEqual(len(events2), 0)
        
        # Manually reset cooldown (mocking time passing would be better but this is quick)
        _last_triggered.clear()
        events3 = generate_event(data)
        self.assertEqual(len(events3), 1)

if __name__ == '__main__':
    unittest.main()
