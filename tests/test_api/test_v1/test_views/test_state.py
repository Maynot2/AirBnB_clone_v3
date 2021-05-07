import unittest
import json
from api.v1.app import app

class StateTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_state(self):
        json = json.dumps({
            "name": "Alaska"
        })

        response = self.app.post('/api/v1/state',
                                  headers={"Content-Type": "application/json"},
                                  data=json)

        self.assertEqual(str, type(response.json['state_id']))
        self.assertEqual(200, response.status_code)

if __name__ == "__main__":
    unittest.main()
