from django.test import SimpleTestCase
from django.urls import reverse, resolve
from BlogsBook.views import register, home, add_blog, viewblog, deleteblog, updateblog, \
    viewuser, edituser, passwordrest, delete_user, searchuser, searchcategory
from django.contrib.auth.views import LoginView, LogoutView


class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse('BlogsBook:register')
        self.assertEquals(resolve(url).func, register)

    def test_login_url(self):
        url = reverse('BlogsBook:user-login')
        self.assertEquals(resolve(url).func.view_class, LoginView)

    def test_logout_url(self):
        url = reverse('BlogsBook:user-logout')
        self.assertEquals(resolve(url).func.view_class, LogoutView)

    def test_home_url(self):
        url = reverse('BlogsBook:home')
        self.assertEquals(resolve(url).func, home)

    def test_addblog_url(self):
        url = reverse('BlogsBook:add-blog')
        self.assertEquals(resolve(url).func, add_blog)

    def test_viewblog_url(self):
        url = reverse('BlogsBook:view-blog', kwargs={'blog_id': 10})
        self.assertEquals(resolve(url).func, viewblog)

    def test_deleteblog_url(self):
        url = reverse('BlogsBook:delete-blog', kwargs={'blog_id': 10})
        self.assertEquals(resolve(url).func, deleteblog)

    def test_updateblog_url(self):
        url = reverse('BlogsBook:update-blog', kwargs={'blog_id': 10})
        self.assertEquals(resolve(url).func, updateblog)

    def test_viewuser_url(self):
        url = reverse('BlogsBook:view-user', kwargs={'user_id': 10})
        self.assertEquals(resolve(url).func, viewuser)

    def test_edituser_url(self):
        url = reverse('BlogsBook:edit-user', kwargs={'user_id': 14})
        self.assertEquals(resolve(url).func, edituser)

    def test_passwordreset_url(self):
        url = reverse('BlogsBook:reset-password')
        self.assertEquals(resolve(url).func, passwordrest)

    def test_deleteuser_url(self):
        url = reverse('BlogsBook:delete-user', kwargs={'user_id': 14})
        self.assertEquals(resolve(url).func, delete_user)

    def test_categorysearch_url(self):
        url = reverse('BlogsBook:category-search')
        self.assertEquals(resolve(url).func, searchcategory)

    def test_usersearch_url(self):
        url = reverse('BlogsBook:user-search')
        self.assertEquals(resolve(url).func, searchuser)
