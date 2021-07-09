from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec, ui
from selenium.webdriver.support.wait import WebDriverWait


class AdminE2EBaseTestCase(StaticLiveServerTestCase):
    superuser_name = "testsuperuser"
    superuser_password = "75ncfjhkehu4ur"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.wait = WebDriverWait(cls.selenium, 10)

    @classmethod
    def tearDownClass(cls):
        # noinspection PyUnresolvedReferences
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self) -> None:
        super().setUp()

        self.superuser = User.objects.create_superuser(self.superuser_name, password=self.superuser_password)
        self.login()

    def login(self):
        self.open_page("/admin/login")

        username = self.selenium.find_element_by_id("id_username")
        username.send_keys(self.superuser_name)

        password = self.selenium.find_element_by_id("id_password")
        password.send_keys(self.superuser_password)

        submit = self.selenium.find_element_by_css_selector("[type=submit]")
        submit.click()

    def open_page(self, url: str):
        if url.startswith("http"):
            self.selenium.get(url)
        elif url.startswith("/"):
            self.selenium.get(f"{self.live_server_url}{url}")
        else:
            self.selenium.get(f"{self.live_server_url}/{url}")

    def assertVisible(self, locator):
        if len(locator) <= 2:
            self.wait.until(ec.visibility_of_element_located(locator))
        else:
            self.wait.until(ec.visibility_of_element_located(locator[:2]),
                            f"{locator[2]} isn't presented or not visible.")

    def assertInvisible(self, locator):
        if len(locator) <= 2:
            self.wait.until_not(ec.visibility_of_element_located(locator))
        else:
            self.wait.until_not(ec.visibility_of_element_located(locator[:2]),
                                f"{locator[2]} should be invisible or not presented.")

    def assertRequired(self, locator):
        element = self.find_element(locator)
        required = element.get_property("required")

        self.assertTrue(required)

    def assertOptional(self, locator):
        element = self.find_element(locator)
        required = element.get_property("required")

        self.assertFalse(required)

    def assertLabelForFieldMarkedRequired(self, for_component_id):
        self.assertHasClass(f"label[for={for_component_id}]", "required")

    def assertLabelForFieldMarkedOptional(self, for_component_id):
        self.assertDoesNotHaveClass(f"label[for={for_component_id}]", "required")

    def assertHasClass(self, locator, css_class):
        element = self.find_element(locator)
        element_classes = element.get_attribute("class")

        self.assertTrue(css_class in element_classes)

    def assertDoesNotHaveClass(self, locator, css_class):
        element = self.find_element(locator)
        element_classes = element.get_attribute("class")

        self.assertFalse(css_class in element_classes)

    def assertAttributeEqual(self, locator, attr, value):
        element = self.find_element(locator)
        attr_value = element.get_attribute(attr)

        self.assertEqual(value, attr_value)

    def find_element(self, locator):
        if isinstance(locator, tuple):
            return self.selenium.find_element(*locator[:2])
        elif isinstance(locator, WebElement):
            return locator
        elif isinstance(locator, str):
            return self.selenium.find_element_by_css_selector(locator)
        else:
            raise ValueError("locator should be an instance of tuple, string or WebElement types.")

    def assertSelectTag(self, locator):
        element = self.find_element(locator)
        tag_name = element.tag_name.lower()

        self.assertEqual("select", tag_name)

    def assertTextareaTag(self, locator):
        element = self.find_element(locator)
        tag_name = element.tag_name.lower()

        self.assertEqual("textarea", tag_name)

    def assertNumberInputTag(self, locator):
        element = self.find_element(locator)
        tag_name = element.tag_name.lower()
        type_name = element.get_attribute("type")

        self.assertEqual("input", tag_name)
        self.assertEqual("number", type_name)

    def assertValueEqual(self, locator, value):
        element = self.find_element(locator)
        element_value = element.get_attribute("value")

        self.assertEqual(value, element_value)

    def assertValueEmpty(self, locator):
        self.assertValueEqual(locator, "")

    def assertTextEqual(self, locator, text):
        element = self.find_element(locator)

        self.assertEqual(text, element.text)

    def assertTextEmpty(self, locator):
        self.assertTextEqual(locator, "")

    def assertHasValidationErrors(self, locator, error_message=None, error_class="error"):
        element = self.find_element(locator)
        inner_validation_errors = self.find_inner_validation_errors(element, error_message)

        if error_class:
            self.assertHasClass(element, error_class)

        self.assertTrue(len(inner_validation_errors) > 0)

    def assertHasNoValidationErrors(self, locator, error_message=None):
        element = self.find_element(locator)
        inner_validation_errors = self.find_inner_validation_errors(element, error_message)

        self.assertDoesNotHaveClass(element, "error")
        self.assertEqual(0, len(inner_validation_errors))

    def assertHasRequiredValidationError(self, locator):
        self.assertHasValidationErrors(locator, "This field is required.")

    def find_options(self, locator):
        element = self.find_element(locator)

        if element.tag_name.lower() == "select":
            return [(option.get_attribute("value"), option.get_attribute("innerText")) for option in
                    ui.Select(element).options]

        raise ValueError(f"Element corresponding to locator is {element.tag_name} but should be select.")

    def find_inner_validation_errors(self, element, error_message=None):
        inner_validation_errors = [
            li for li in element.find_elements_by_css_selector("ul.errorlist li")
            if not error_message or li.get_attribute("innerText").strip() == error_message
        ]

        return inner_validation_errors
