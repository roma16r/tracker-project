from django import forms
from .models import User
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.password_validation import validate_password


class UserCreateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'autocomplete': 'off'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'birth_date', 'position', 'image']


class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'autocomplete': 'off'}), required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'groups', 'birth_date', 'position', 'image']


class ProfileForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), required=False)
    birth_date = forms.DateField(widget=forms.widgets.DateInput(attrs={'autocomplete': 'off'}), required=False)
    field_order = ['first_name', 'last_name', 'email', 'birth_date', 'position', 'old_password', 'password',
                   'confirm_password', 'image']

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'position', 'image', 'password']

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        old_password = cleaned_data.get("old_password")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if old_password != '' or password != '' or confirm_password != '':
            if not check_password(old_password, self.instance.password):
                self.add_error('old_password', "Password is not correct")
            if password != confirm_password:
                self.add_error('confirm_password', "Password does not match")
            validate_password(password, user=User)
            cleaned_data['password'] = make_password(password)
        else:
            del cleaned_data['password']

        return cleaned_data

