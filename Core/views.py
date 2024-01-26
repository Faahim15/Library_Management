from django.shortcuts import render,redirect 
from django.views.generic import CreateView,ListView
from . forms import RegistrationForm 
from django.contrib.auth.models import User 
from django.urls import reverse_lazy  
from django.contrib import messages 
from django.contrib.auth.views import LoginView 
from django.contrib.auth import logout 
from django.views import View 
from  BookApp.models import BooksModel,CategoryModel

# Create your views here.
class RegistrationView(CreateView):
    model = User 
    form_class = RegistrationForm 
    template_name = 'signup.html' 
    success_url = reverse_lazy('login') 
    context_object_name = 'form' 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Register'
        return context

class UserLoginView(LoginView):
    template_name = 'signup.html'
    # success_url = reverse_lazy('profile')
    def get_success_url(self):
        return reverse_lazy('homepage')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.success(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['title'] = 'Login'
        return context  
    
class Home(ListView):
    model = BooksModel
    template_name = 'home.html' 
    context_object_name = 'books' 
    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
         category = CategoryModel.objects.get(slug=category_slug)
         return BooksModel.objects.filter(books=category) 
        else:
         return BooksModel.objects.all() 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = CategoryModel.objects.all()
        return context

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request) 
        messages.success(self.request, 'Successfully Logged Out ')
        return redirect('homepage')  

# class Transaction_report(ListView):

    