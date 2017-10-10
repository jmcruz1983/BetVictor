#! /usr/bin/env python

""" Test that creates an account in BetVictor web page and then logout """

import os
import time
import random
import logging
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# Setting logger
log = logging.getLogger(__name__)
fmt = logging.Formatter(datefmt="%H:%M:%S",
                        fmt='%(asctime)s %(levelname)-8s: %(name)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(fmt)
log.addHandler(sh)
log.setLevel(logging.INFO)

class BetVictor(unittest.TestCase):

    """ Helper functions """

    """ Get the files in a directory """
    def get_files(self, dir, exts):
        list_fs = []
        if dir and exts:
            for root, directories, filenames in os.walk(dir):
                for filename in filenames:
                    for ext in exts:
                        if filename.endswith(ext):
                            list_fs.append(os.path.join(root,
                                                        filename))
                            break
        return list_fs

    """ Search for a file in the given directory """
    def find_file(self, dir=None, filename=None):
        found_files = []
        f_name, f_ext = os.path.splitext(filename)
        for _f in self.get_files(dir, [f_ext]):
            if _f.endswith(filename):
                found_files.append(_f)
        return found_files

    """ Search for the firefox driver """
    def find_firefox_bin(self):
        return self.find_file(
            os.path.join(self.abs_p, os.environ['BIN_DRIVERS']), "geckodriver").pop(0)

    """ Searches an element by id or class name  """
    def get_element_from_id_or_class(self, root=None, id=None):
        elems = []
        if id and isinstance(id, basestring):
            if root == None:
                elems = self.driver.find_elements_by_id(id)
                if len(elems) == 0:
                    elems = self.driver.find_elements_by_class_name(id)
            else:
                elems = root.find_elements_by_id(id)
                if len(elems) == 0:
                    elems = root.find_elements_by_class_name(id)
        return elems

    """ Fills a text input """
    def fill_text_input(self, id=None, value=None, send_tab=True, time_sleep=1):
        fields = self.get_element_from_id_or_class(id=id)
        if len(fields) > 0 and value and isinstance(value, basestring):
            for item in fields:
                item.send_keys(value)
                if send_tab:
                    item.send_keys(Keys.TAB)
                if time_sleep > 0:
                    time.sleep(time_sleep)

    """ Clicks a button """
    def click_button(self, id=None, time_sleep=1):
        fields = self.get_element_from_id_or_class(id=id)
        if len(fields) > 0:
            for item in fields:
                if item.is_displayed():
                    item.click()
                    if time_sleep > 0:
                        time.sleep(time_sleep)

    """ Clicks an option from a menu """
    def click_option_from_menu(self, root=None, option=0, click_root=True, time_sleep=1, send_tab=False):
        if root and isinstance(root, webdriver.remote.webelement.WebElement):
            if root.is_displayed():
                if click_root:
                    root.click()
                if send_tab:
                    root.send_keys(Keys.TAB)

            ul = root.find_element_by_tag_name('ul')
            lis = ul.find_elements_by_tag_name('li')
            if len(lis) > option and lis[option].is_displayed():
                lis[option].click()
                if time_sleep > 0:
                    time.sleep(time_sleep)
            else:
                for opt in lis:
                    if opt.is_displayed():
                        opt.click()
                        if time_sleep > 0:
                            time.sleep(time_sleep)

    """ Set day, month, year of birth """
    def set_birthday(self, div_name='dob_container', class_name='bv-select-select'):
        roots = self.get_element_from_id_or_class(id=div_name)
        if len(roots) > 0:
            divs = self.get_element_from_id_or_class(root=roots.pop(0), id=class_name)
            if len(divs) == 3: # Day, Month and Year
                # Day
                self.click_option_from_menu(divs[0], 1)
                # Month
                self.click_option_from_menu(divs[1], 1)
                # Year
                self.click_option_from_menu(divs[2], 1)

    """ Setup, tests and teardown functions """

    def setUp(self):
        self.abs_p = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
        self.setup_done = True
        self.driver = webdriver.Firefox(executable_path=self.find_firefox_bin())
        self.driver.maximize_window()
        self.url = 'http://www.betvictor.com'
        self.sleep_timeout = 5

        # Generate random info to fill-up account details
        self.rand_int10 = random.randint(1, 10)
        self.rand_int1000 = random.randint(100, 1000)
        self.rand_phone = random.randint(100000, 999999)

        self.phone = '7712%d' % (self.rand_phone)  # Pseudo valid phone in UK
        self.email = 'john.smith.%d@mail.com' % (self.rand_int1000)
        self.username = 'dummy%d' % (self.rand_int1000)
        self.pwd = 'pIonxi%d' % (self.rand_int1000)
        log.info("\n")
        log.info("===============")
        log.info("user: %s" % (self.username))
        log.info("pwd: %s" % (self.pwd))
        log.info("===============")

    def test_create_account(self):
        # Wait a bit until main page is loaded
        self.driver.get(self.url)
        time.sleep(self.sleep_timeout)

        # Input mail address
        self.fill_text_input('email', self.email)
        # Click sign-up buttom
        self.click_button('button_email')

        # Personal Details
        # Input first name
        self.fill_text_input('account_first_name', 'John')
        # Input last name
        self.fill_text_input('account_last_name', 'Smith')
        # Select day, month and year of birth
        self.set_birthday()
        # Input phone number
        self.fill_text_input('account_home_phone', self.phone)

        # Address
        # Select country
        root = self.driver.find_element_by_id('country_id')
        self.click_option_from_menu(root, 1) # United Kingdom
        # Input postcode
        self.fill_text_input('account_postcode_lookup', 'N17 9FL')
        # Input house number
        self.fill_text_input('account_house_number', '1')
        # Input flat number
        self.fill_text_input('account_flat_number', '1')
        # Click find address button
        self.click_button('find_address_button', 3)

        # Select first address option
        root = self.driver.find_element_by_id('addressList')
        self.click_option_from_menu(root, 0, False) # First option

        # Account details
        # Input username
        self.fill_text_input('account_username', self.username)
        # Input password
        self.fill_text_input('account_password', self.pwd)
        self.fill_text_input('account_password_confirmation', self.pwd)
        # Select security question
        root = self.driver.find_element_by_id('security_question_id1')
        self.click_option_from_menu(root, 2, False) # Favourite Team
        # Input security answer
        self.fill_text_input('account_security_question_answer1', 'Barcelona FC')

        # Deposit Limit
        # Select currency
        root = self.driver.find_element_by_id('currency_id')
        self.click_option_from_menu(root, 1, False, send_tab=True)  # Pounds Sterling

        # Select deposit limit
        root = self.driver.find_element_by_id('deposit_container')
        self.click_option_from_menu(root, 1, False, send_tab=True)  # No Limit

        # Terms and conditions
        # Click terms checkbox
        self.click_button('checkbox')
        # Click create account button
        self.click_button('button')

        # Wait a bit to logout
        time.sleep(self.sleep_timeout)
        self.click_button('logout')

        # Now login and logout
        # Wait a bit until login and logout
        time.sleep(self.sleep_timeout)
        # Input username
        self.fill_text_input('username', self.username)
        # Input username
        self.fill_text_input('password', self.pwd)
        # Click login button
        self.click_button('submit')
        # Wait a bit to logout
        time.sleep(self.sleep_timeout)
        self.click_button('logout')

    def tearDown(self):
        # Wait a bit to teardown
        time.sleep(self.sleep_timeout)
        self.driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)