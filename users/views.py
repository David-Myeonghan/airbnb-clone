from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")
    initial = {"email": "myeonghan12@gmail.com"}

    def form_valid(self, form):
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(self.request, username=email, password=password)
            if user is not None:
                login(self.request, user)
            return super().form_valid(form)

    # def get(self, request):
    #     form = forms.LoginForm(initial={"email": "myeonghan12@gmail.com"})

    #     return render(request, "users/login.html", {"form": form})

    # def post(self, request):
    #     form = forms.LoginForm(request.POST)
    #     if form.is_valid():
    #         email = form.cleaned_data.get("email")
    #         password = form.cleaned_data.get("password")
    #         user = authenticate(request, username=email, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect(reverse("core:home"))
    #     return render(request, "users/login.html", {"form": form})


# function based class
# def login_view(request):
#     if request.method == "GET":
#         pass

#     elif request.method == "POST":


def log_out(request):
    logout(request)
    return redirect(reverse("core:home"))


class SignUpView(FormView):
    template_name = "users/signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")
    initial = {
        "first_name": "David",
        "last_name": "Ryu",
        "email": "mydav@gmail.com",
    }

    def form_valid(self, form):  # if the form is valid, which is validated in forms.py,
        form.save()  # then, save the form(create an user)
        email = form.cleaned_data.get("email")  # then, login process from here
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        if user is not None:  # if the user login,
            login(self.request, user)
        user.verify_email()  # then, send the verification email.
        return super().form_valid(form)


def complete_verification(request, key):
    try:
        user = models.User.objects.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # todo: add a success message
    except models.User.DoesNotExist:
        # todo: Add error message
        pass
    return redirect(reverse("core:home"))
