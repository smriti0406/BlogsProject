from djongo import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    DOB = models.DateField(blank=False)
    Gender = models.CharField(max_length=1)
    city = models.CharField(max_length=50)
    profession = models.CharField(max_length=50)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    Title = models.CharField(max_length=100)
    Content = models.TextField()
    Category = models.ManyToManyField(Category)
    DatePosted = models.DateTimeField(default=timezone.now)
    Creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    content = models.TextField()
    DatePosted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

