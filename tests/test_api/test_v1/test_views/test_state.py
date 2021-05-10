"""
    Tests for State API
"""

import unittest
import json
from api.v1.app import app


class StateTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_create_state(self):
        json_obj = json.dumps({
            "name": "Alaska"
        })

        response = self.app.post('/api/v1/states',
                                 headers={"Content-Type": "application/json"},
                                 data=json_obj)

        print(response.json)
        print(response.status_code)

        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(201, response.status_code)
        self.assertEqual('Alaska', response.json['name'])

if __name__ == "__main__":
    unittest.main()
