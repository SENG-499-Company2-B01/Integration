import time
from locators import LoginPageLocators
from locators import ProfPrefPageLocators
from locators import ProfLandingPageLocators
from locators import AdminLandingPageLocators
from locators import GenerateSchedulePageLocators
from locators import CreateAccountPageLocators
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait

class BasePage(object):
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 50)

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
    
    def go_to_view(self):
        self.driver.find_element(*AdminLandingPageLocators.VIEW_SCHED_LINK).click()
    
    def go_to_create_account(self):
        self.driver.find_element(*AdminLandingPageLocators.CREATE_ACCT_LINK).click()


class GenerateSchedulePage(BasePage):
    def start_generation(self, semester: str):
        #ActionChains(self.driver,10).scroll_by_amount(0,200).perform()
        self.driver.find_element(*GenerateSchedulePageLocators.TERM_SELECT_DROPDOWN).click()
        self.wait.until(EC.visibility_of_element_located(GenerateSchedulePageLocators.TERM_SELECT_ITEM(semester)))
        self.driver.find_element(*GenerateSchedulePageLocators.TERM_SELECT_ITEM(semester)).click()
        self.wait.until(EC.invisibility_of_element_located(GenerateSchedulePageLocators.TERM_SELECT_ITEM(semester)))
        self.driver.find_element(*GenerateSchedulePageLocators.START_GEN_BUTTON).click()
    
    def wait_for_generation(self):
        self.wait.until(EC.visibility_of_element_located(GenerateSchedulePageLocators.SCHEDULE_CALENDAR))

class CreateAccountPage(BasePage):
    def fill_email(self, email):
        self.driver.find_element(*CreateAccountPageLocators.EMAIL_FIELD).send_keys(email)
    
    def fill_name(self, first_name, last_name):
        self.driver.find_element(*CreateAccountPageLocators.FIRSTNAME_FIELD).send_keys(first_name)
        self.driver.find_element(*CreateAccountPageLocators.LASTNAME_FIELD).send_keys(last_name)
    
    def fill_expertise(self, expertise):
        self.driver.find_element(*CreateAccountPageLocators.EXPERTISE_FIELD).send_keys(expertise)
    
    def fill_experience(self, experience):
        self.driver.find_element(*CreateAccountPageLocators.EXPERIENCE_FIELD).send_keys(experience)

    def fill_education(self, education):
        self.driver.find_element(*CreateAccountPageLocators.EDUCATION_FIELD).send_keys(education)

    def fill_password(self, password):
        self.driver.find_element(*CreateAccountPageLocators.PASSWORD_FIELD).send_keys(password)
        self.driver.find_element(*CreateAccountPageLocators.CONFIRMEDPASSWORD_FIELD).send_keys(password)

    def submit_form(self):
        ActionChains(self.driver).scroll_by_amount(0,300).perform()
        self.driver.find_element(*CreateAccountPageLocators.CREATE_BUTTON).click()