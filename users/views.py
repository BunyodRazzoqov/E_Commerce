from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from users.authentication_form import AuthenticationForm
from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginForm, RegisterModelForm, EmailSendForm


# def login_page(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             email: str = form.cleaned_data['email']
#             password: str = form.cleaned_data['password']
#             user = authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('project_management')
#             else:
#                 messages.error(request, 'Invalid Username or Password')
#     else:
#         form = LoginForm()
#     return render(request, 'users/login.html', {'form': form})


class LoginPageView(LoginView):
    redirect_authenticated = True
    form_class = AuthenticationForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('project_management')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Email or Password')
        return self.render_to_response(self.get_context_data(form=form))


# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterModelForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.save()
#             login(request, user)
#             return redirect('customers')
#     else:
#         form = RegisterModelForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


class RegisterFormView(FormView):
    form_class = RegisterModelForm
    template_name = 'users/register.html'

    def form_valid(self, form):
        form.send_email()
        user = form.save(commit=False)
        user.save()
        login(self.request, user)
        return redirect('customers')


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('customers')


# class LogoutPageView(LogoutView):
#     template_name = 'my_web/base/base.html'
#     get_success_url = reverse_lazy('customers')


class SendEmailView(FormView):
    template_name = 'users/sending_mail.html'
    form_class = EmailSendForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def success(request):
    return render(request, 'users/success.html')
