from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from . import forms
from . import models
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseRedirect

# Create your views here.
class SignUp(UserPassesTestMixin, CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'

    permission_denied_message = "You are already registered!"

    def test_func(self):
        return self.request.user.is_anonymous

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("home"))
