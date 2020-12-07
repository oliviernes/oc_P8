"""Functional tests"""
import time

from django.test import LiveServerTestCase, Client
from django.urls import reverse
from django.core import mail

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pdb

class ResetPasswordTest(LiveServerTestCase):
    """Class testing the password reset of a Pur Beurre website's user"""

    fixtures = ["dumpy_content_fixtures"]

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
        self.client = Client()       

    def tearDown(self):
        self.browser.quit()

    def test_reset_password(self):
        """Test the reset of a password"""
        
        # Mell visit the Pur Beurre website:

        self.browser.get(self.live_server_url)

        # She decide to signup:

        signup = self.browser.find_element_by_xpath('//a[@href="/signup/"]')

        signup.click()

        time.sleep(1)

        # The system display the signup form. She enters her
        # account information:

        username = self.browser.find_element_by_id("id_username")
        first_name = self.browser.find_element_by_id("id_first_name")
        email = self.browser.find_element_by_id("id_email")
        password1 = self.browser.find_element_by_id("id_password1")
        password2 = self.browser.find_element_by_id("id_password2")

        username.send_keys("Mell2010")
        first_name.send_keys("Mell")
        email.send_keys("mell2010@gmail.com")
        password1.send_keys("monsupermdp1234")
        password2.send_keys("monsupermdp1234")

        signup_title = self.browser.find_element_by_id("signup_title")
        self.assertEqual("Création de compte:", signup_title.text)

        button = self.browser.find_elements_by_tag_name("button")
        button[1].click()

        time.sleep(1)

        # Now she logs out:

        logout = self.browser.find_element_by_xpath('//a[@href="/logout"]')

        logout.click()

        time.sleep(2)

        # She try to log in but with a wrong password:

        login = self.browser.find_element_by_xpath('//a[@href="/login/"]')

        login.click()

        time.sleep(2)

        signup_link = self.browser.find_element_by_id("signup")
        self.assertIn("Créez un compte", signup_link.text)

        username = self.browser.find_element_by_id("id_username")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("mell2010@gmail.com")
        password.send_keys("monsupermdp1235")

        password.send_keys(Keys.ENTER)

        time.sleep(2)

        # She forgot her password and try and ask to reset one:
       
        reset = self.browser.find_element_by_id("reset")
        self.assertIn("Créez un nouveau", reset.text)

        reset.click()

        time.sleep(2)

        email = self.browser.find_element_by_id("id_email")
        email.send_keys("mell2010@gmail.com")
        email.send_keys(Keys.ENTER)

        time.sleep(2)

        self.assertEqual(len(mail.outbox), 1)
        self.assertIn("Réinitialisation du mot de passe sur localhost:", mail.outbox[0].subject)

        response = self.client.post(reverse('password_reset'),{'email':'mell2010@gmail.com'})
        
        self.assertEqual(response.status_code, 302)

        # The port is retrieve thanks to the email subject.

        port = mail.outbox[0].subject[-5:]

        time.sleep(1)

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'Réinitialisation du mot de passe sur testserver')

        # The token and the uid are retrieve from the response context:

        token = response.context[0]['token']
        uid = response.context[0]['uid']
        
        # Mell go to her email account and click on the link of the
        #  message sent by Pur beurre website:

        self.browser.get("http://localhost:"+port+"/reset_password/"+uid+"/"+token)

        time.sleep(3)

        first_p = self.browser.find_elements_by_tag_name("p")
        self.assertIn("Entrez votre mot de passe", first_p[0].text)

        # Then she enters her new password 2 times:

        self.browser.find_element_by_name("new_password1").send_keys("1234monsupermdp")
        new_password = self.browser.find_element_by_name("new_password2")
        new_password.send_keys("1234monsupermdp")
        new_password.send_keys(Keys.ENTER)

        time.sleep(3)

        # Then she connects with her new password:

        login = self.browser.find_element_by_xpath('//a[@href="/login/"]')

        login.click()

        time.sleep(2)

        signup_link = self.browser.find_element_by_id("signup")
        self.assertIn("Créez un compte", signup_link.text)

        username = self.browser.find_element_by_id("id_username")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("mell2010@gmail.com")
        password.send_keys("1234monsupermdp")

        password.send_keys(Keys.ENTER)

        time.sleep(3)

        save_texts = self.browser.find_elements_by_tag_name("h2")
        self.assertEqual("mell2010@gmail.com", save_texts[0].text)

        # Satisfied, she goes back to sleep after logging out:

        logout = self.browser.find_element_by_xpath('//a[@href="/logout"]')

        logout.click()

        time.sleep(2)

        disconnect_texts = self.browser.find_elements_by_tag_name("p")
        self.assertEqual("Vous êtes déconnecté.", disconnect_texts[0].text)

        # self.fail('Finish the test!')
