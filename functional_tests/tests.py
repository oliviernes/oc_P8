from selenium import webdriver
import unittest

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
        self.fail('Finish the test!')

        # She is invited to enter a product item straight away

        # She types "Nutella" into the text box in the middle of the screen

        # When she hits enter, the page updates, and now the page lists
        # healthier products of the same category.

        # She selects a product and get a new page with the detail of the product

        # She enters a new product in the textbox in the top of the screen.

        # The page updates and show a new list of healthier products.

        # Mell saves a product

        # Satisfied, she goes back to sleep

if __name__ == '__main__':
    unittest.main(warnings='ignore')