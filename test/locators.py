from selenium.webdriver.common.by import By

class LoginPageLocators(object):
    NETLINK_INPUT = (By.XPATH, '//input[1]')
    PASSWORD_INPUT = (By.XPATH, '//input[2]')
    SIGNIN_BUTTON = (By.XPATH, "//div[text()='SIGN IN']/parent::button")
    FORGOT_PASSWORD_LINK = (By.XPATH, "//div[contains(text(),'Forgot your')]")