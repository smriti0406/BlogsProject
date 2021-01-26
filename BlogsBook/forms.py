from django import forms
from BlogsBook.models import UserProfileInfo, Blog, Category
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    username = forms.CharField(help_text="")
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def clean(self):

        super(UserForm, self).clean()

        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if not any(char.isupper() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 UpperCase'])
        if not any(char.islower() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 LowerCase'])
        if not any(char.isdigit() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 digit'])
        if password1 != password2:
            self._errors['confirm_password'] = self.error_class(['Not Matching'])

        return self.cleaned_data


class PersonalForm(forms.ModelForm):
    GENDER_MALE = 'M'
    GENDER_FEMALE = 'F'
    GENDER_CHOICES = (
        (GENDER_MALE, 'Male',),
        (GENDER_FEMALE, 'Female',),
    )
    Gender = forms.ChoiceField(choices=GENDER_CHOICES)
    DOB = forms.DateField(required=True)
    city = forms.CharField(max_length=50)
    profession = forms.CharField(max_length=50)

    class Meta:
        model = UserProfileInfo
        fields = ['Gender', 'DOB', 'city', 'profession']


class BlogForm(forms.ModelForm):
    Title = forms.CharField(max_length=100)
    Content = forms.Textarea()

    class Meta:
        model = Blog
        fields = ['Title', 'Content']


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=50)

    class Meta:
        model = Category
        fields = ['name']


class PasswordReset(forms.ModelForm):
    username = forms.CharField(help_text="")
    password = forms.CharField(min_length=8, widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['password']

    def clean(self):

        super(PasswordReset, self).clean()

        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('confirm_password')
        if not any(char.isupper() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 UpperCase'])
        if not any(char.islower() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 LowerCase'])
        if not any(char.isdigit() for char in password1):
            self._errors['password'] = self.error_class(['Most contain atleast 1 digit'])
        if password1 != password2:
            self._errors['confirm_password'] = self.error_class(['Not Matching'])

        return self.cleaned_data

