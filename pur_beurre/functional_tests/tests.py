"""Functional tests"""
import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.firefox.options import Options


class NewVisitorTest(LiveServerTestCase):
    """Class testing a new user visiting the Pur Beurre website"""
    fixtures = ["dumpy_content_fixtures"]

    def setUp(self):
        options = Options()
        options.add_argument("--headless")

        self.browser = webdriver.Firefox(firefox_options=options)
        self.browser.set_window_position(0, 0)
        self.browser.set_window_size(1267, 950)

    def tearDown(self):
        self.browser.quit()

    def test_user_story(self):
        """Test the story of an user inside Pur Beurre app"""

        # Mell has heard about a website to get healthier products. She goes
        # to check out its homepage

        self.browser.get(self.live_server_url)

        time.sleep(1)

        # She notices the form bar in the header and in the center of the page

        self.assertIn("Pur", self.browser.title)
        bar_text = self.browser.find_element_by_tag_name("a").text
        self.assertIn("Pur", bar_text)

        # She is invited to enter a product item straight away

        inputbox = self.browser.find_element_by_name("query")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Chercher")

        # She types "Nutella" into the text box in the middle of the screen

        inputboxs = self.browser.find_elements_by_name("query")
        inputbox_center = inputboxs[1]
        self.assertEqual(
            inputbox_center.get_attribute("placeholder"), "Produit"
        )
        inputbox_center.send_keys("Nutella")

        # When she hits enter, the page updates, and now the page lists
        # healthier products of the same category.

        inputbox_center.send_keys(Keys.ENTER)
        time.sleep(1)

        prod_text = self.browser.find_element_by_tag_name("h4").text
        self.assertIn("Nocciolata", prod_text)

        # She selects a product and get a new page with the detail
        #  of the product

        link = self.browser.find_element_by_xpath(
            '//a[@href="/product/8001505005592"]'
        )

        link.click()

        time.sleep(1)

        # She enters a new product in the textbox in the top of the screen.

        inputbox = self.browser.find_element_by_name("query")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Chercher")

        inputbox.send_keys("Véritable petit beurre")

        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        # The page updates and show a new list of healthier products.

        # Mell try to save the first product. She click on the
        # save link but as she is not connected, the link send
        # her on the login page:

        save_texts = self.browser.find_elements_by_tag_name("h4")
        self.assertIn("Sauvegarder", save_texts[1].text)

        time.sleep(2)

        save_texts[1].click()

        time.sleep(1)

        # She tries to connect. She enters her email
        # and a wrong password. Then she clicks on the login button.

        signup_link = self.browser.find_element_by_id("signup")
        self.assertIn("un compte!", signup_link.text)

        username = self.browser.find_element_by_id("id_username")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("mell2010@gmail.com")
        password.send_keys("XXXXX")

        password.send_keys(Keys.ENTER)

        time.sleep(1)

        # The system inform her to try again:
        # Then, she click on the signup button because she doesn't
        #  have an account:

        signup = self.browser.find_element_by_id("signup")

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

        # The app display Mell's account page. She is now connected.
        # She search again the product "Véritable petit beurre"
        # in the search bar.

        inputbox = self.browser.find_element_by_name("query")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Chercher")

        inputbox.send_keys("Véritable petit beurre")

        inputbox.send_keys(Keys.ENTER)

        time.sleep(1)

        # She tries now to save the second product ('Biscuit raisin')

        save_texts = self.browser.find_elements_by_tag_name("h4")
        self.assertEqual("Biscuit raisin", save_texts[2].text)

        save_texts[3].click()

        # A page inform her of the recording of the substitute and
        # display a table with her substitutes recorded. The table is
        # empty as it's her first product recorded.

        caption = self.browser.find_element_by_tag_name("h4")
        self.assertIn("Vos substituts enregistrés", caption.text)

        time.sleep(2)

        # She looks for an other substitute of 'Véritable petit beurre':
        inputbox = self.browser.find_element_by_name("query")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Chercher")

        inputbox.send_keys("Véritable petit beurre")

        inputbox.send_keys(Keys.ENTER)

        # She try to save the same substitute than the last recording:

        time.sleep(2)

        save_texts = self.browser.find_elements_by_tag_name("h4")
        self.assertEqual("Biscuit raisin", save_texts[2].text)

        save_texts[3].click()

        # Now the app inform her that the product is already recorded
        # in the database:

        time.sleep(2)

        first_p = self.browser.find_elements_by_tag_name("p")
        self.assertIn("est déjà enregistré pour le produit", first_p[0].text)

        # Now the table display her first recording:

        first_rec = self.browser.find_elements_by_tag_name("td")
        self.assertEqual("Véritable petit beurre", first_rec[0].text)

        # She enters an other product in the search bar:

        inputbox = self.browser.find_element_by_name("query")

        inputbox.send_keys("La paille d’or aux framboises")

        inputbox.send_keys(Keys.ENTER)

        time.sleep(2)

        # She try to save an other substitute:

        save_texts = self.browser.find_elements_by_tag_name("h4")
        self.assertEqual("Belvita petit dejeuner moelleux", save_texts[2].text)

        save_texts[3].click()

        # Now the app inform her that the product has been recorded
        # in the database:

        first_p = self.browser.find_elements_by_tag_name("p")
        self.assertIn("a été enregistré pour le produit", first_p[0].text)

        time.sleep(2)

        # Now she logs out:

        logout = self.browser.find_element_by_xpath('//a[@href="/logout"]')

        logout.click()

        time.sleep(2)

        # Then she logs in:

        login = self.browser.find_element_by_xpath('//a[@href="/login/"]')

        login.click()

        time.sleep(2)

        username = self.browser.find_element_by_id("id_username")
        password = self.browser.find_element_by_id("id_password")

        username.send_keys("mell2010@gmail.com")
        password.send_keys("monsupermdp1234")

        password.send_keys(Keys.ENTER)

        # She checks that her recorded substitutes are still in the database:

        time.sleep(3)

        carrot = self.browser.find_element_by_xpath('//a[@href="/favorites/"]')

        carrot.click()

        first_rec = self.browser.find_elements_by_tag_name("td")
        self.assertEqual("Véritable petit beurre", first_rec[0].text)

        sec_rec = self.browser.find_elements_by_tag_name("td")
        self.assertEqual("Belvita petit dejeuner moelleux", sec_rec[3].text)

        time.sleep(2)

        # self.fail('Finish the test!')

        # Satisfied, she goes back to sleep after logging out:
