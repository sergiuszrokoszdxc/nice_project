import unittest

import requests


class TestAcceptance(unittest.TestCase):
    def test_index(self):
        """in progress"""
        r = requests.get("http://127.0.0.1:5000/")
        self.assertEqual(r.status_code, 200)

    def test_save_test(self):
        """in progress"""
        r = requests.get("http://127.0.0.1:5000/store/foo")
        self.assertEqual(r.status_code, 200)
