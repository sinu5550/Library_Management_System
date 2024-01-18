from django.shortcuts import render,redirect
from . import forms
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from book.models import userBorrowed
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# Create your views here.

def register(request):
    if request.method == 'POST':
        register_form = forms.RegistrationForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, 'Account Created Successfully')
            return redirect('login')
    
    else:
        register_form = forms.RegistrationForm()
    return render(request, 'register.html', {'form' : register_form, 'type' : 'Signup'})


class UserLoginView(LoginView):
    template_name = 'register.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self, form):
        messages.success(self.request, 'Logged in Successful')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Logged in information incorrect')
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Login'
        return context
    

class UserLogoutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home')
    
@login_required
def profile(request):
    data = userBorrowed.objects.filter(author = request.user)
    return render(request, 'profile.html',{'data':data})

@login_required
def return_book(request, id):
    borrowed_book = get_object_or_404(userBorrowed, id=id, author=request.user)
    print(id)
    request.user.account.balance += borrowed_book.price
    request.user.account.save()

    
    borrowed_book.delete()

    messages.success(request, f'You have successfully returned {borrowed_book.book.title}.')
    return redirect('profile')