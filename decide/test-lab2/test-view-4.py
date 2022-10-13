import time

from pyexpat import model
from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from base.tests import BaseTestCase
from voting.models import Question, Voting

class AdminTestCase(StaticLiveServerTestCase):


    def setUp(self):
        #Load base test functionality for decide
        self.base = BaseTestCase()
        self.base.setUp()

        options = webdriver.ChromeOptions()
        options.headless = True
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-using")
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

        super_user = User(username='administrator', is_staff=True, is_superuser=True)
        super_user.set_password('administrator')
        super_user.save()

        super().setUp()            
            
    def tearDown(self):           
        super().tearDown()
        self.driver.quit()

        self.base.tearDown()

    def test_createQuestion(self):
        self.driver.get(f'{self.live_server_url}/admin/')
        self.driver.find_element(By.ID,'id_username').send_keys("administrator")
        self.driver.find_element(By.ID,'id_password').send_keys("administrator",Keys.ENTER)
        self.driver.get(f'{self.live_server_url}/admin/voting/question/add/')
        self.driver.find_element(By.ID,'id_desc').send_keys("test")
        self.driver.find_element(By.NAME, "_save").click()
        time.sleep(5)        
        self.assertEquals(self.driver.find_element(By.CSS_SELECTOR, "th.field-__str__").find_element(By.TAG_NAME, 'a').text, "test")
