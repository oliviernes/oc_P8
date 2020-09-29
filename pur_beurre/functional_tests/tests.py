from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import pdb

import unittest
import time

class NewVisitorTest(LiveServerTestCase):
    # fixtures = ['dumpy_content_reduced_exclude']
    fixtures = ['dumpy_content_exclude']

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_choose_a_product(self):

        # Mell has heard about a website to get healthier products. She goes
        # to check out its homepage

        self.browser.get(self.live_server_url)

        time.sleep(4)

        # She notices the form bar in the header and in the center of the page

        self.assertIn('Pur', self.browser.title)
        bar_text = self.browser.find_element_by_tag_name('a').text
        self.assertIn('Pur', bar_text)

        # She is invited to enter a product item straight away

        inputbox = self.browser.find_element_by_name('query') 
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Chercher'
        )

        # She types "Nutella" into the text box in the middle of the screen

        inputboxs = self.browser.find_elements_by_name('query') 
        inputbox_center = inputboxs[1]
        self.assertEqual(
            inputbox_center.get_attribute('placeholder'),
            'Produit'
        )
        inputbox_center.send_keys('Nutella')

        # When she hits enter, the page updates, and now the page lists
        # healthier products of the same category.

        inputbox_center.send_keys(Keys.ENTER)
        time.sleep(5)

        prod_text = self.browser.find_element_by_tag_name('h4').text
        self.assertIn('Nocciolata', prod_text)

        # She selects a product and get a new page with the detail of the product

        link = self.browser.find_element_by_xpath('//a[@href="/product/8001505005592"]')
        
        link.click()

        time.sleep(5)

        # She enters a new product in the textbox in the top of the screen.


        inputbox = self.browser.find_element_by_name('query')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Chercher'
        )

        inputbox.send_keys("Véritable petit beurre")

        inputbox.send_keys(Keys.ENTER)
 
        time.sleep(5)

        # The page updates and show a new list of healthier products.

        # Mell saves a product (she click in the save link):

        savelink = self.browser.find_element_by_xpath('//a[@href="signup/link"]')

        savelink.click()

        self.fail('Finish the test!')


        # Satisfied, she goes back to sleep