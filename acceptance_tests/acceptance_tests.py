import unittest
import os

import requests

HOST = os.environ.get("NGINX_HOST")
PORT = os.environ.get("NGINX_PORT")
URL = "http://" + HOST + ":" + PORT


class TestAcceptance(unittest.TestCase):
    def test_index(self):
        """in progress"""
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)

    def test_save_test(self):
        """in progress"""
        r = requests.get(URL)
        self.assertEqual(r.status_code, 200)
