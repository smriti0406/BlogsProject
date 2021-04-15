from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from BlogsBook.models import UserProfileInfo, Blog, Comment, Category
import json


class TestViews(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='smriti@99', first_name='Smriti', last_name='Agrawal', email='smriti99@gmail.com')
        self.blog = Blog.objects.create(Title='Smriti-test', Content='test-content', Creator=self.user)
        self.blog.Category.add(Category.objects.create(name='smriti'))
        self.user.set_password('Minuri@98')
        self.user.save()
        self.client = Client()
        self.addblog = reverse('BlogsBook:add-blog')
        self.login = reverse('BlogsBook:user-login')
        self.register = reverse('BlogsBook:register')
        self.home = reverse('BlogsBook:home')
        self.viewblog = reverse('BlogsBook:view-blog', kwargs={'blog_id': self.blog.id})

    def test_register(self):
        response = self.client.get(self.register)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'BlogsBook/registration.html')
        response = self.client.post(self.register, {
            'username': 'smriti0456',
            'first_name': 'Smriti',
            'last_name': 'Agrawal',
            'email': 'smriti0406@gmail.com',
            'password': 'Minuri@98',
            'confirm_password': 'Minuri@98',
            'Gender': 'F',
            'DOB': '10/9/98',
            'city': 'Allahabad',
            'profession': 'Software Developement',

        })
        self.assertEquals(response.status_code, 302)

    def test_login(self):
        response = self.client.get(self.login)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'BlogsBook/login.html')
        response = self.client.post(self.login, {
            'username': 'smriti@99',
            'password': 'Minuri@98'
        })
        assert self.user.is_authenticated
        self.assertEquals(response.status_code, 302)
    def test_home(self):
        self.client.login(username='smriti@99', password='Minuri@98')
        response = self.client.get(self.home)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'BlogsBook/home.html')

    def test_addblog(self):
        self.client.login(username='smriti@99', password='Minuri@98')
        response = self.client.post(self.addblog, {
            'Title': 'test-blog',
            'Content': 'test-blog content abcdefgh',
            'name': 'test, test1'
        })
        print(response)
        blog = Blog.objects.get(Title='test-blog')
        self.assertEquals(blog.Creator.username, 'smriti@99')
        self.assertEquals(response.status_code, 302)

    def test_viewblogs(self):
        self.client.login(username='smriti@99', password='Minuri@98')
        response = self.client.get(self.viewblog)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'BlogsBook/viewblog.html')













