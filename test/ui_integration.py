import pytest
from selenium import webdriver
import page
import time

import unittest


class ChromeTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.driver.get('https://company2-frontend.onrender.com/')
        cls.driver.fullscreen_window()
        return super().setUpClass()
    
    def setUp(self):
        self.login_page = page.LoginPage(self.driver)
        self.prof_pref_page = page.ProfPrefPage(self.driver)
        self.prof_landing_page = page.ProfLandingPage(self.driver)
        self.admin_landing_page = page.AdminLandingPage(self.driver)
        self.generate_schedule_page = page.GenerateSchedulePage(self.driver)
        self.create_account_page = page.CreateAccountPage(self.driver)
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
        self.driver.get('https://company2-frontend.onrender.com/')
        self.driver.fullscreen_window()
        self.login_page.login('Rich.Little', 'Rich.Little12345')

    def test_5_generate_schedule(self):
        self.generate_schedule_page.start_generation("Spring")
        self.generate_schedule_page.wait_for_generation()

    def test_6_create_prof_account(self):
        self.admin_landing_page.go_to_create_account()
        self.create_account_page.fill_email("test@test.com")
        self.create_account_page.fill_name("Testfirst", "Testlast")
        self.create_account_page.fill_expertise("test")
        self.create_account_page.fill_education("test")
        self.create_account_page.fill_experience("5")
        self.create_account_page.fill_password("test")
        self.create_account_page.submit_form()

    def test_7_admin_sign_out(self):
        self.admin_landing_page.sign_out()
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

if __name__ == "__main__":
    unittest.main()