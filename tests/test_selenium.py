import re
import threading
import time
import unittest
from selenium import webdriver
from app import create_app


class SeleniumTestCase(unittest.TestCase):
    client = None

    @classmethod
    def setUpClass(cls):
        # start Chrome
        try:
            cls.client = webdriver.Chrome(service_args=["--verbose", "--log-path=chrome.log"])
        except:
            pass

        # skip these tests if the browser could not be started
        if cls.client:
            # create the application
            cls.app = create_app('testing')
            cls.app_context = cls.app.app_context()
            cls.app_context.push()

            # suppress logging to keep unittest output clean
            import logging
            logger = logging.getLogger('werkzeug')
            logger.setLevel("ERROR")

            # start the Flask server in a thread
            threading.Thread(target=cls.app.run).start()

            # give the server a second to ensure it is up
            time.sleep(1)

    @classmethod
    def tearDownClass(cls):
        if cls.client:
            # stop the flask server and the browser
            cls.client.get('http://localhost:5000/shutdown')
            cls.client.close()

            # remove application context
            cls.app_context.pop()

    def setUp(self):
        if not self.client:
            self.skipTest('Web browser not available')

    def tearDown(self):
        pass

    def test_home_page(self):
        # navigate to home page
        self.client.get('http://localhost:5000/')
        self.assertTrue(re.search('Generator', self.client.page_source))

    def test_button(self):
        # finding the button using ID
        self.client.get('http://localhost:5000/')
        button = self.client.find_element_by_id('create-random-string')

        # clicking on the button
        button.click()

        # Check randomfield
        element = self.client.find_element_by_id('randomfield')
        text = element.text

        # clicking button again then compare to confirm they are not equal
        button.click()
        self.assertNotEqual(text,element.text)
