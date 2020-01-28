from django import forms
from . import models


class LoginForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    # def clean_email(self):  # add error, and format the data
    #     email = self.cleaned_data.get("email")
    #     try:
    #         models.User.objects.get(username=email)
    #         return email
    #     except models.User.DoesNotExist:  # if try not working, run this.
    #         raise forms.ValidationError("User does not exist")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            user = models.User.objects.get(email=email)  # if a user exists,
            if user.check_password(password):  # and password is matching
                return self.cleaned_data  # then, return cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:  # if failed at getting user from db, user not exist.
            self.add_error("email", forms.ValidationError("User does not exist"))
