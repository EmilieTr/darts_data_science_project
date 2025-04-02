from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_driver():
    """
    Initializes and returns a Selenium WebDriver instance.
    """
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service)