"""
Selenium tests to test frontend and api functionality.
Runs via .travis.yml. To run locally...
pip install selenium
py.test tests.functional_tests.py
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from django.test import override_settings
from pytest import fixture, mark
import logging
import json

logger = logging.getLogger('pdp.' + __name__)


def test_cascade_page(browser, live_server, settings):
    """
    Check that the logged in user is 'studemp' and they get a page with
    the title 'Profile information'.
    """
    settings.MOCK_LOGIN_USER = 'studemp@washington.edu'
    # if ever we want to switch users:
    # browser.get(live_server + settings.LOGOUT_URL)
    browser.get(live_server + '/id/cascade/')
    wait_for_title(browser)
    WebDriverWait(browser, 5).until(EC.text_to_be_present_in_element(
        (By.CLASS_NAME, 'netid-navbar'), 'UW NetID: studemp'))


def wait_for_title(browser, title_substring="Profile information"):
    try:
        WebDriverWait(browser, 5).until(EC.title_contains(title_substring))
    finally:
        logger.debug('Your title was: {}'.format(browser.title))


@fixture(scope='session')
def browser(request):
    driver = webdriver.Firefox()
    driver.set_window_size(1120, 550)

    def fin():
        driver.close()
    request.addfinalizer(fin)
    return driver


@fixture
def settings(settings, request):
    settings_context = override_settings(DEBUG=True)
    settings_context.__enter__()
    settings.MOCK_LOGIN_USER = 'studemp@washington.edu'
    if ('idbase.middleware.MockLoginMiddleware' not in
            settings.MIDDLEWARE_CLASSES):
        settings.MIDDLEWARE_CLASSES = (
            ['idbase.middleware.MockLoginMiddleware'] +
            settings.MIDDLEWARE_CLASSES)

    def fin():
        settings_context.__exit__(None, None, None)
    request.addfinalizer(fin)

    return settings
