from locators import LoginPageLocators
from locators import ProfPrefPageLocators
from locators import ProfLandingPageLocators
from locators import AdminLandingPageLocators
from locators import GenerateSchedulePageLocators
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

class BasePage(object):
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

class LoginPage(BasePage):
    def login(self, netlink_id, password):
        self.driver.find_element(*LoginPageLocators.NETLINK_INPUT).send_keys(netlink_id)
        self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginPageLocators.SIGNIN_BUTTON).click()

class ProfLandingPage(BasePage):
    def go_to_set_preferences(self):
        self.driver.find_element(*ProfLandingPageLocators.SET_PREF_BUTTON).click()

    def sign_out(self):
        self.driver.find_element(*ProfLandingPageLocators.USER_MENU_BUTTON).click()
        self.driver.find_element(*ProfLandingPageLocators.SIGN_OUT_BUTTON).click()
        

class ProfPrefPage(BasePage):
    def set_semester(self, sem):
        semester_locator = ProfPrefPageLocators.SEMESTER_FALL_RADIO if sem == 'Fall' else ProfPrefPageLocators.SEMESTER_WINTER_RADIO if sem == 'Winter' else ProfPrefPageLocators.SEMESTER_SUMMER_RADIO
        self.driver.find_element(*semester_locator).click()

    def set_able_to_teach(self, is_able, reason=''):
        if is_able:
            self.driver.find_element(*ProfPrefPageLocators.ABLE_TO_TEACH_RADIO_YES).click()
        else:
            self.driver.find_element(*ProfPrefPageLocators.ABLE_TO_TEACH_RADIO_NO).click()
            self.driver.find_element(*ProfPrefPageLocators.ABLE_TO_TEACH_TEXTBOX).send_keys(reason)

    def set_preferred_time(self, start, end):
        self.driver.find_element(*ProfPrefPageLocators.PREF_TIME_START).send_keys(start)
        self.driver.find_element(*ProfPrefPageLocators.PREF_TIME_END).send_keys(end)

class AdminLandingPage(BasePage):
    def sign_out(self):
        self.driver.find_element(*AdminLandingPageLocators.USER_MENU_BUTTON).click()
        self.driver.find_element(*AdminLandingPageLocators.SIGN_OUT_BUTTON).click()
    
    def go_to_generate(self):
        self.driver.find_element(*AdminLandingPageLocators.GENERATE_SCHED_LINK).click()

class GenerateSchedulePage(BasePage):
    def start_generation(self):
        self.driver.find_element(*GenerateSchedulePageLocators.START_GEN_BUTTON).click()
        #ActionChains(self.driver).move_to_element(button).click(button).perform()