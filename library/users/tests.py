from django.test import TestCase
from django.test import LiveServerTestCase
from django.test.client import Client
from django.test.client import RequestFactory
from selenium.webdriver.firefox.webdriver import WebDriver

from users.models import User
from users.views import ListUserView

class UserTest(TestCase):
    """ User model tests """
    def test_str(self):
        user =  User(first_name = "Vivek", last_name = "Agarwal")
        self.assertEquals(
                str(user),
                'Vivek Agarwal'
        )


class UserListViewTest(TestCase):
    def test_contacts_in_the_context(self):
        client = Client()
        response = client.get('/')
        self.assertEquals(list(response.context['object_list']), [])
        User.objects.create(first_name = 'Vivek', last_name = 'Agarwal')
        response = client.get('/')
        self.assertEquals(response.context['object_list'].count(), 1)

    def test_contacts_in_the_context_request_factory(self):
        factory = RequestFactory()
        request = factory.get('/')
        response = ListUserView.as_view() (request)
        self.assertEquals(list(response.context_data['object_list']), [])
        User.objects.create(first_name = 'Vivek', last_name = 'Agarwal')
        response = ListUserView.as_view() (request)
        self.assertEquals (response.context_data['object_list'].count(), 1)

class UserListIntegrationTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.selenium= WebDriver()
        super(UserListIntegrationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(UserListIntegrationTests, cls).tearDownClass()

    def test_user_listed(self):
        User.objects.create(first_name = "Vivek", last_name = "Agarwal")
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assertEqual(
                self.selenium.find_elements_by_css_selector('.user')[0].text, 'Vivek Agarwal')
    def test_add_contact_linked(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.assert_(
                self.selenium.find_element_by_link_text('add user'))
    def test_add_contact(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        self.selenium.find_element_by_link_text('add user').click()

        self.selenium.find_element_by_id('id_first_name').send_keys('test')
        self.selenium.find_element_by_id('id_last_name').send_keys('test')
        self.selenium.find_element_by_id('id_email').send_keys('test@gmail.com')

        self.selenium.find_element_by_id('save_user').click()
        self.assertEqual(
                self.selenium.find_elements_by_css_selector('.user')[-1].text,
                'test test')
