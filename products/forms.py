from django import forms
from django.contrib.auth import authenticate, get_user_model
from .models import Profile, Comment


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'name': 'username'})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'name': 'password'})

    def clean(self, *args, **keyargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            elif not user.check_password(password):
                raise forms.ValidationError('Incorrect Password')

        return super(UserLoginForm, self).clean(*args, **keyargs)


User = get_user_model()


class UsersRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "confirm_password",
        ]

    username = forms.CharField()
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(UsersRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            "name": "username"})
        self.fields['email'].widget.attrs.update({
            'class': 'form-control',
            "name": "email"})
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            "name": "password"})
        self.fields['confirm_password'].widget.attrs.update({
            'class': 'form-control',
            "name": "confirm_password"})

    def clean(self, *args, **keyargs):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("Email is already registered")

        username_qs = User.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("User with this username already registered")

        if len(password) < 8:
            raise forms.ValidationError("Password must have at least 8 characters")

        if password != confirm_password:
            raise forms.ValidationError("Passwords are not matching")

        return super(UsersRegisterForm, self).clean(*args, **keyargs)


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'gender', 'phone_number')


class UserForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'phone_number')


class ProfilePicForm(forms.ModelForm):
    dp = forms.ImageField(widget=forms.FileInput(attrs=None))

    class Meta:
        model = Profile
        fields = ('dp',)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('city', 'country', 'street_address', 'postcode', 'state')


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone_number', 'city', 'country', 'street_address', 'postcode', 'state')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
