import datetime
import unittest

from nice_project.app import flask_app


class TestApp(unittest.TestCase):
    def setUp(self):
        flask_app.config["TESTING"] = True
        self.client = flask_app.test_client()

    def test_index(self):
        """in progress"""
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)

    def test_save_text(self):
        """in progress"""
        r = self.client.get("/store/foo")
        self.assertEqual(r.status_code, 200)
