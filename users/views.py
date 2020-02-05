import os
import requests
from django.views import View
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.core.files.base import ContentFile
from . import forms, models


class LoginView(FormView):

    template_name = "users/login.html"
    form_class = forms.LoginForm
    success_url = reverse_lazy("core:home")

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


def github_login(request):
    client_id = os.environ.get("GH_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


class GithubException(Exception):
    pass


# When user accepts application, go to our callback url.
def github_callback(request):
    try:
        client_id = os.environ.get("GH_ID")
        client_secret = os.environ.get("GH_SECRET")
        code = request.GET.get("code", None)  # Get the code
        if code is not None:
            token_request = requests.post(  # with the code, make another request to get access_token
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            # the code is valid for 10 mins, and can be used once.
            if error is not None:  # if there is an error in response,
                raise GithubException()
            else:  # if no error,
                access_token = token_json.get("access_token")  # get access_token
                profile_request = requests.get(  # request gibhib api with the access_token
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",  # put the access token in headers,
                        "Accept": "application/json",
                    },
                )
                # get the response from profile_request
                profile_json = profile_request.json()
                username = profile_json.get("login", None)

                # if user exists(if an user is in the profile response),
                if username is not None:
                    name = profile_json.get("name")  # get these info from the response,
                    email = profile_json.get("email")
                    bio = profile_json.get("bio")
                    try:
                        # if there is a user with this email, it means that the user already has an acount, or already logged in
                        user = models.User.objects.get(email=email)

                        # if, the user is logged in with their password, or kakao, raise an exception.
                        if user.login_method != models.User.LOGIN_GITHUB:
                            print(user.login_method)
                            raise GithubException()
                            # login(request, user)
                        # if a user is trying to log in(already went through the account creation process), make the user login.
                    except models.User.DoesNotExist:  # if the user doesn't exist with that email, create a new user came from Github.
                        user = models.User.objects.create(
                            email=email,
                            first_name=name,
                            username=email,
                            bio=bio,
                            login_method=models.User.LOGIN_GITHUB,
                            email_verified=True,
                        )

                        user.set_unusable_password()
                        user.save()
                    login(request, user)
                    return redirect(reverse("core:home"))
                else:
                    raise GithubException()
        else:
            raise GithubException()
    except GithubException:  # whatever error happens, take users to here. # Instedad of return redirect everytime, just raise an exception.
        # Send error message
        return redirect(reverse("users:login"))


class KakaoException(Exception):
    pass


def kakao_login(request):
    client_id = os.environ.get("KAKAO_ID")
    redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
    )


def kakao_callback(request):
    try:
        code = request.GET.get("code")
        client_id = os.environ.get("KAKAO_ID")
        redirect_uri = "http://127.0.0.1:8000/users/login/kakao/callback"
        token_request = requests.get(
            f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={client_id}&redirect_uri={redirect_uri}&code={code}"
        )
        token_json = token_request.json()
        error = token_json.get("error", None)
        if error is not None:
            raise KakaoException()
        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        kakao_account = profile_json.get("kakao_account")
        email = kakao_account.get("email", None)
        if email is None:
            raise KakaoException()
        profile = kakao_account.get("profile")
        nickname = profile.get("nickname")
        profile_image_url = profile.get("profile_image_url")
        try:
            user = models.User.objects.get(email=email)
            if user.login_method != models.User.LOGIN_KAKAO:
                raise KakaoException()
        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                username=email,
                first_name=nickname,
                login_method=models.User.LOGIN_KAKAO,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()
            if profile_image_url is not None:  # if an image exists,
                photo_request = requests.get(profile_image_url)
                user.avatar.save(
                    f"{nickname}-avatar", ContentFile(photo_request.content)
                )
        login(request, user)
        return redirect(reverse("core:home"))
    except KakaoException:
        return redirect(reverse("users:login"))
