import unittest
import os

import requests
# TODO ths needs to b changed for nginx deploy
HOST = "nice_project" or os.environ.get("NGINX_HOST")
PORT = "5001" or os.environ.get("NGINX_PORT")
URL = "http://" + HOST + ":" + PORT


class TestAcceptance(unittest.TestCase):
    def test_index(self):
        """in progress"""
        r = requests.get(URL + "/")
        self.assertEqual(r.status_code, 200)

    def test_show(self):
        """in progress"""
        r = requests.get(URL + "/show")
        self.assertEqual(r.status_code, 200)

    def test_submit(self):
        """in progress"""
        r = requests.get(URL + "/submit")
        self.assertEqual(r.status_code, 200)
