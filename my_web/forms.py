from django import forms
from django.contrib.auth.models import User

from my_web.models import Customer


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)


class CustomerModelForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class RegisterModelForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_username(self):
        username = self.data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'This {username} is already registered.')
        return username

    def clean_password(self):
        password: str = self.data.get('password')
        confirm_password: str = self.data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Please enter the same password')
        return self.cleaned_data['password']

    def save(self, commit=True):
        user = super(RegisterModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True

        if commit:
            user.save()

        return user
