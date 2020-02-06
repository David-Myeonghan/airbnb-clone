from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

# users logged in only with email can see this view.
# Kakao users cannot see the view.
class EmailLoginOnlyView(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.login_method == "email"

    def handle_no_permission(self):
        messages.error(self.request, "Unauthorised!")
        return redirect("core:home")


# Only loggedout users can see this.
class LoggedOutOnlyView(UserPassesTestMixin):

    permission_denied_message = "Page Not Found"

    # If test_func returns true, you can move on to the next page.
    def test_func(self):
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        messages.error(self.request, "Unauthorised!")
        return redirect("core:home")


# Checks If users logged in, or not. If not logged in, take them to login_url.
# After going to login_url, address has 'next' query, which means that they have a place to go after login.
# therefore, in 'LoginView', instead of getting 'success_url', use 'get_success_url'
class LoggedInOnlyView(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")
