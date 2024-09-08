from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.urls import reverse_lazy
from users.authentication_form import AuthenticationForm
from config.settings import EMAIL_DEFAULT_SENDER
from users.forms import LoginForm, RegisterModelForm, EmailSendForm

from django.contrib.sites.shortcuts import get_current_site
from users.token import account_activation_token
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from users.models import User


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


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                'Welcome to Ecommerce',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False,
            )
            # login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            # return redirect('customers')
            return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)


class RegisterFormView(FormView):
    form_class = RegisterModelForm
    template_name = 'users/register.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        current_site = get_current_site(request)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            message = render_to_string('users/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                'Welcome to Ecommerce',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False,
            )
            return HttpResponse('<h1>Please confirm your e-mail address to complete the registration</h1>')

        # login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('customers')


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


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('<h1>Thank you for your email confirmation. Now you can login your account.</h1>')
    else:
        return HttpResponse('<h1>Activation link is invalid!</h1>')
