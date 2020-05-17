import datetime
import unittest

from nice_project.app import store_with_time
from nice_project.app import flask_app


class TestAppUtils(unittest.TestCase):
    def test_store_with_time(self):
        """store_with_time should return tuple with actual
         datetime and value passed"""
        now = datetime.datetime.now()
        returned_datetime, returned_value = \
            store_with_time(unittest.mock.DEFAULT)
        self.assertEqual(returned_value, unittest.mock.DEFAULT)
        self.assertTrue((returned_datetime - now).total_seconds() < 1)


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
