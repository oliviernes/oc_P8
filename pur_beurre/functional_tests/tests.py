from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_choose_a_product(self):

        # Mell has heard about a website to get healthier products. She goes
        # to check out its homepage

        self.browser.get('http://localhost:8000')

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
        self.assertIn('Protein', prod_text)

        self.fail('Finish the test!')

        # She selects a product and get a new page with the detail of the product

        # She enters a new product in the textbox in the top of the screen.

        # The page updates and show a new list of healthier products.

        # Mell saves a product

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')