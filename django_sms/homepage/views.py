from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from . import forms
from . import models
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView
from .forms import LoginForm

# Create your views here.
class HomePageView(TemplateView):
    template_name = "homepage/homepage.html"






class LoginView(FormView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('home/homepage.html')

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Invalid login credentials')
            return redirect('login')
        
    
  