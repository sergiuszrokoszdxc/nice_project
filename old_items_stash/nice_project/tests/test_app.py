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

    def test_show(self):
        """in progress"""
        r = self.client.get("/show")
        self.assertEqual(r.status_code, 200)

    def test_get_submit(self):
        """in progress"""
        r = self.client.get("/submit")
        self.assertEqual(r.status_code, 200)

    def test_post_submit(self):
        """in progress"""
        r = self.client.post("/submit")
        self.assertEqual(r.status_code, 200)
