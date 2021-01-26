from django.contrib import admin
from BlogsBook.models import UserProfileInfo, Category, Blog, Comment
# Register your models here.


admin.site.register(UserProfileInfo)
admin.site.register(Category)
admin.site.register(Blog)
admin.site.register(Comment)
#admin.site.register(Likes)