from django.shortcuts import render, get_object_or_404
from BlogsBook.forms import UserForm, PersonalForm, BlogForm, CategoryForm, PasswordReset
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Blog, Comment, Category, UserProfileInfo
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.contrib.auth import logout
from django.core.paginator import Paginator

# Create your views here.


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        personal_form = PersonalForm(data=request.POST)
        if user_form.is_valid() and personal_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            personal = personal_form.save(commit=False)
            personal.user = user
            personal_form.save()
            registered = True
            return HttpResponseRedirect(reverse('BlogsBook:user-login'))
        else:
            print(user_form.errors)
            print(personal_form.errors)
    else:
        user_form = UserForm()
        personal_form = PersonalForm()
    return render(request, 'BlogsBook/registration.html', {'user_form': user_form, 'personal_form': personal_form,
                                                           'registered': registered})


@login_required
def home(request):
    blogs = Blog.objects.order_by('-DatePosted')
    blogs = Paginator(blogs, 2)
    print(blogs.num_pages)
    return render(request, 'BlogsBook/home.html', {'blogs': blogs})


@login_required
def add_blog(request):
    if request.method == 'POST':
        blog_form = BlogForm(data=request.POST)
        category_form = CategoryForm(data=request.POST)
        if blog_form.is_valid() and category_form.is_valid():
            categories = request.POST['name'].split(", ")
            blog = blog_form.save(commit=False)
            blog.Creator = User.objects.get(username=request.user)
            blog.save()
            for category in categories:
                c = Category(name=category)
                c.save()
                blog.Category.add(c)
            return HttpResponseRedirect(reverse('BlogsBook:home'))
        else:
            print(blog_form.errors)
            print(category_form.errors)
    else:
        blog_form = BlogForm()
        category_form = CategoryForm()
    return render(request, 'BlogsBook/Add_blog.html', {'blog': blog_form, 'category': category_form})


@login_required
def viewblog(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except(KeyError, Blog.DoesNotExist):
        return render(request, 'BlogsBook/viewblog.html', {'error': "Sorry! Blog not found"})
    else:
        if request.method == 'POST':
            user = get_object_or_404(User, username=request.user)
            blog.comment_set.create(content=request.POST['comment'], user=user)
            return HttpResponseRedirect(reverse('BlogsBook:view-blog', kwargs={'blog_id': blog.id}))
        return render(request, 'BlogsBook/viewblog.html', {'blog': blog})


@login_required
def deleteblog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    user = User.objects.get(username=request.user)
    if blog.Creator == user:
        if request.method == 'POST':
            blog.delete()
            return HttpResponseRedirect(reverse('BlogsBook:home'))
        else:
            return render(request, 'BlogsBook/confirm_delete_blog.html', {'blog': blog})
    else:
        raise PermissionDenied('You are forbidden to delete this Blog')


@login_required
def updateblog(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    category = ", ".join(c.name for c in blog.Category.all())
    user = User.objects.get(username=request.user)
    if blog.Creator == user:
        if request.method == 'POST':
            blog.Title = request.POST['Title']
            print(blog.Title)
            blog.Content = request.POST['Content']
            blog.save()
            categories = request.POST['category'].split(", ")
            for category in categories:
                blog.Category.get_or_create(name=category)
            return HttpResponseRedirect(reverse('BlogsBook:view-blog', kwargs={'blog_id': blog.id}))
        else:
            return render(request, 'BlogsBook/update_blog.html', {'blog': blog, 'category': category})
    else:
        raise PermissionDenied('You are forbidden to delete this Blog')


@login_required
def viewuser(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        info = UserProfileInfo.objects.get(user__pk=user_id)
    except (KeyError, UserProfileInfo.DoesNotExist):
        info = {}
    return render(request, 'BlogsBook/view_user.html', {'current_user': user, 'info': info})


@login_required
def edituser(request):
    error = ''
    user = User.objects.get(username=request.user)
    try:
        info = UserProfileInfo.objects.get(user__pk=user.id)
    except(KeyError, UserProfileInfo.DoesNotExist):
        info = {}
    if request.method == 'POST':
        user.username = request.POST['username']
        info.city = request.POST['city']
        info.profession = request.POST['profession']
        try:
            user.save()
            info.save()
        except:
            error = 'Other user already exists'
        else:
            return HttpResponseRedirect(reverse('BlogsBook:view-user', kwargs={'user_id': user.id}))
    return render(request, 'BlogsBook/edit_user.html', {'info': info, 'error': error})


def passwordrest(request):
    if request.method == 'POST':
        password_form = PasswordReset(data=request.POST)
        try:
            user = User.objects.get(username=request.POST['username'])
        except(KeyError, User.DoesNotExist):
            pass
        else:
            if password_form.is_valid():
                print(password_form['password'])
                user.password = password_form['password']
                print(user.password)
                user.set_password(user.password)
                print(user.password)
                user.save()
                return HttpResponseRedirect(reverse('BlogsBook:user-login'))
    else:
        password_form = PasswordReset()
    return render(request, 'BlogsBook/resetPassword.html', {'form': password_form})


@login_required
def commentdelete(request, blog_id, comment_id):
    try:
        comment = Comment.objects.get(pk=comment_id)
        print(comment)
    except(KeyError, Comment.DoesNotExist):
        raise ObjectDoesNotExist
    else:
        comment.delete()
        return HttpResponseRedirect(reverse('BlogsBook:view-blog', kwargs={'blog_id': blog_id}))

        
@login_required
def delete_user(request):
    if request.method == 'POST':
        user = get_object_or_404(User, username=request.user)
        logout(request)
        user.delete()
        return HttpResponseRedirect(reverse('BlogsBook:user-login'))
    else:
        return render(request, 'BlogsBook/delete_user.html')


@login_required
def searchcategory(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('BlogsBook:category-query', kwargs={'query': request.POST['search']}))
    else:
        list = Category.objects.all()
        return render(request, 'BlogsBook/searchcategory.html', {'list': list})


@login_required
def searchcatname(request, query):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('BlogsBook:category-query', kwargs={'query': request.POST['search']}))
    else:
        error = ''
        try:
            c = Category.objects.get(name=query)
        except(KeyError, Category.DoesNotExist):
            error = 'No blog exists related to above category'
            list2 = []
        else:
            list2 = c.blog_set.all()
        return render(request, 'BlogsBook/searchcategory.html', {'list2': list2, 'error': error})


@login_required
def searchuser(request):
    if request.method == "POST":
        return HttpResponseRedirect(reverse('BlogsBook:user-query', kwargs={'query': request.POST['search']}))
    else:
        return render(request, 'BlogsBook/usersearch.html')


@login_required
def userquery(request, query):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('BlogsBook:user-query', kwargs={'query': request.POST['search']}))
    else:
        try:
            user = User.objects.get(username=query)
        except(KeyError, User.DoesNotExist):
            return render(request, 'BlogsBook/usersearch.html', {'error': 'user not exist'})
        else:
            try:
                blogs = Blog.objects.filter(Creator=user)
            except(KeyError, Blog.DoesNotExist):
                pass
            return render(request, 'BlogsBook/usersearch.html', {'list': blogs, 'user1': user})




