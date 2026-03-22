"""
Student Feedback Registration Form — Selenium Test Suite (Sub-Task 4)

Test cases:
    1. Page loads successfully
    2. Valid submission shows success toast
    3. Empty fields trigger all error messages
    4. Invalid email triggers email error
    5. Invalid mobile triggers mobile error
    6. Dropdown selection works correctly
    7. Submit and Reset buttons work correctly
"""

import os
import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

# ── Helpers ──────────────────────────────────────────────────────

# Resolve the path to index.html relative to this test file
FORM_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'index.html'))
FORM_URL  = f'file:///{FORM_PATH.replace(os.sep, "/")}'

VALID_DATA = {
    'studentName':      'Aarav Sharma',
    'emailId':          'aarav.sharma@university.ac.in',
    'mobileNumber':     '9876543210',
    'department':       'CSE',
    'gender':           'Male',
    'feedbackComments':  (
        'The teaching methodology is excellent and the faculty members '
        'are very supportive and responsive to student queries and concerns.'
    ),
}


@pytest.fixture(scope='module')
def driver():
    """Create a Chrome WebDriver instance for the test module."""
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1280,900')

    # Try using webdriver-manager if available, otherwise fall back to PATH
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        service = ChromeService(ChromeDriverManager().install())
    except ImportError:
        service = ChromeService()

    browser = webdriver.Chrome(service=service, options=opts)
    browser.implicitly_wait(3)
    yield browser
    browser.quit()


def fill_form(driver, data: dict):
    """Helper to fill in the form with the supplied data dict."""
    driver.get(FORM_URL)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'feedbackForm')))

    # Text / email / tel inputs
    for field_id in ('studentName', 'emailId', 'mobileNumber'):
        el = driver.find_element(By.ID, field_id)
        el.clear()
        el.send_keys(data.get(field_id, ''))

    # Department dropdown
    dept = data.get('department')
    if dept:
        Select(driver.find_element(By.ID, 'department')).select_by_value(dept)

    # Gender radio
    gender = data.get('gender')
    if gender:
        driver.find_element(By.CSS_SELECTOR, f'input[name="gender"][value="{gender}"]').click()

    # Feedback textarea
    ta = driver.find_element(By.ID, 'feedbackComments')
    ta.clear()
    ta.send_keys(data.get('feedbackComments', ''))


# ── Test Cases ───────────────────────────────────────────────────

class TestFeedbackForm:
    """Selenium test suite for the Student Feedback Registration Form."""

    # TC-1: Check whether the form page opens successfully
    def test_page_loads(self, driver):
        driver.get(FORM_URL)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'feedbackForm')))
        assert 'Student Feedback' in driver.title
        heading = driver.find_element(By.CSS_SELECTOR, '.form-header h1')
        assert 'Feedback' in heading.text

    # TC-2: Enter valid data and verify successful submission
    def test_valid_submission(self, driver):
        fill_form(driver, VALID_DATA)
        driver.find_element(By.ID, 'submitBtn').click()
        toast = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'successToast'))
        )
        assert 'Thank you' in toast.text

    # TC-3: Leave mandatory fields blank and check error messages
    def test_empty_fields(self, driver):
        driver.get(FORM_URL)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'feedbackForm')))
        driver.find_element(By.ID, 'submitBtn').click()
        time.sleep(0.5)

        error_ids = ['nameError', 'emailError', 'mobileError', 'deptError', 'genderError', 'feedbackError']
        for eid in error_ids:
            el = driver.find_element(By.ID, eid)
            assert el.text != '', f'Expected error message for {eid}'

    # TC-4: Enter invalid email format and verify validation
    def test_invalid_email(self, driver):
        data = {**VALID_DATA, 'emailId': 'not-an-email'}
        fill_form(driver, data)
        driver.find_element(By.ID, 'submitBtn').click()
        time.sleep(0.5)
        err = driver.find_element(By.ID, 'emailError')
        assert 'valid email' in err.text.lower()

    # TC-5: Enter invalid mobile number and verify validation
    def test_invalid_mobile(self, driver):
        data = {**VALID_DATA, 'mobileNumber': 'abcde12345'}
        fill_form(driver, data)
        driver.find_element(By.ID, 'submitBtn').click()
        time.sleep(0.5)
        err = driver.find_element(By.ID, 'mobileError')
        assert 'valid' in err.text.lower() or 'digit' in err.text.lower()

    # TC-6: Check whether dropdown selection works properly
    def test_dropdown_selection(self, driver):
        driver.get(FORM_URL)
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'department')))
        select = Select(driver.find_element(By.ID, 'department'))

        departments = ['CSE', 'IT', 'ECE', 'EEE', 'ME', 'CE', 'AIDS', 'MBA']
        for dept in departments:
            select.select_by_value(dept)
            assert select.first_selected_option.get_attribute('value') == dept

    # TC-7: Check whether Submit and Reset buttons work correctly
    def test_submit_and_reset_buttons(self, driver):
        fill_form(driver, VALID_DATA)

        # Verify Submit triggers validation (form should validate)
        driver.find_element(By.ID, 'submitBtn').click()
        toast = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.ID, 'successToast'))
        )
        assert toast is not None

        # Wait for toast to hide, refill, then test Reset
        time.sleep(1)
        fill_form(driver, VALID_DATA)
        driver.find_element(By.ID, 'resetBtn').click()
        time.sleep(0.5)

        # After reset, fields should be empty
        assert driver.find_element(By.ID, 'studentName').get_attribute('value') == ''
        assert driver.find_element(By.ID, 'emailId').get_attribute('value') == ''
        assert driver.find_element(By.ID, 'mobileNumber').get_attribute('value') == ''
        assert driver.find_element(By.ID, 'feedbackComments').get_attribute('value') == ''
