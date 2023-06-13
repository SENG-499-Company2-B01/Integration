from locators import LoginPageLocators
from selenium import webdriver

class BasePage(object):
    def __init__(self, driver: webdriver.Chrome):
        self.driver = driver

class LoginPage(BasePage):
    def login(self, netlink_id, password):
        self.driver.find_element(*LoginPageLocators.NETLINK_INPUT).send_keys(netlink_id)
        self.driver.find_element(*LoginPageLocators.PASSWORD_INPUT).send_keys(password)
        self.driver.find_element(*LoginPageLocators.SIGNIN_BUTTON).click()