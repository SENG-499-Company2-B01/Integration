import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import page

import unittest

class ChromeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome('../webdrivers/chromedriver.exe')
        return super().setUpClass()
    
    def setUp(self):
        self.login_page = page.LoginPage(self.driver)
        self.driver.get('http://localhost:3000')
        return super().setUp()
    
    def test_login_page(self):
        self.login_page.login('test123','test123')
        print('Login complete.')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()