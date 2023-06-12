import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By

import unittest

class ChromeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome('./webdrivers/chromedriver.exe')
        return super().setUpClass()
    
    def setUp(self):
        self.driver.get('https://google.ca')
        return super().setUp()
    
    def test_landing_page(self):
        self.driver.find_element(By.XPATH, "//input[@value='Google Search']")
        print('Found element.')


    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()