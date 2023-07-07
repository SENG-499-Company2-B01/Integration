import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import page
import time

import unittest


class ChromeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.get('http://localhost:3000')
        cls.driver.fullscreen_window()
        return super().setUpClass()
    
    def setUp(self):
        self.login_page = page.LoginPage(self.driver)
        self.prof_pref_page = page.ProfPrefPage(self.driver)
        self.prof_landing_page = page.ProfLandingPage(self.driver)
        self.admin_landing_page = page.AdminLandingPage(self.driver)
        self.generate_schedule_page = page.GenerateSchedulePage(self.driver)
        return super().setUp()
    
    def test_1_prof_login(self):
        self.login_page.login('Celina.Berg','Celina.Berg12345')

    def test_2_prof_pref(self):
        self.prof_landing_page.go_to_set_preferences()
        self.prof_pref_page.set_semester('summer')
        self.prof_pref_page.set_able_to_teach(True)
        self.prof_pref_page.set_preferred_time("7:00 am", "8:30 am")

    def test_3_prof_sign_out(self):
        self.prof_landing_page.sign_out()

    def test_4_admin_login(self):
        self.driver.get('http://localhost:3000')
        self.driver.fullscreen_window()
        self.login_page.login('Rich.Little', 'Rich.Little12345')

    def test_5_generate_schedule(self):
        self.admin_landing_page.go_to_generate()
        self.generate_schedule_page.start_generation()

    def test_6_admin_sign_out(self):
        self.admin_landing_page.sign_out()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()