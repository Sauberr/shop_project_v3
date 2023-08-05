from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (LoginView, PasswordChangeView,
                                       PasswordResetView)
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.views.generic.base import TemplateView

from common.views import TitleMixin
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from user_account.forms import (PasswordChangingPassword, UserLoginForm,
                                UserProfileForm, UserRegistrationForm,
                                UserUpdateForm)
from user_account.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    model = User
    template_name = 'accounts/login.html'
    form_class = UserLoginForm
    title = 'Login'


# def login(request):
#     form = UserLoginForm
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return redirect('products:home')
#     context = {'form': form, 'title': 'Login'}
#     return render(request, 'accounts/login.html', context)


class UserRegistrationView(TitleMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/registration/registration.html'
    success_url = reverse_lazy('user_account:login')
    title = 'Registration'


# def registration(request):
#     form = UserRegistrationForm()
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('user_account:login')
#     context = {'form': form, 'title': 'Registration'}
#     return render(request, "accounts/registration/registration.html", context)


def logout(request):
    try:
        for key in list(request.session.keys()):
            if key == 'session_key':
                continue
            else:
                del request.session[key]
    except KeyError:
        pass
    messages.success(request, 'Logout Success')
    auth.logout(request)
    return redirect('products:home')

# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse('home'))


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'accounts/password/password_reset.html'
    email_template_name = 'accounts/password/password_reset_email.txt'
    subject_template_name = 'accounts/password/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('user_account:login')


def check_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({}, status=400)


# class UserProfileView(TitleMixin, UpdateView):
#     model = User
#     form_class = UserProfileForm
#     template_name = 'accounts/profile.html'
#     title = 'Profile'
#
#     def get_success_url(self):
#         return reverse_lazy('user_account:profile', args=(self.object.id,))


# action="{% url 'user_account:profile' user.id  %}" add when you use this class


@login_required
def profile(request):
    form = UserProfileForm(instance=request.user)
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user_account:profile'))
        else:
            print(form.errors)
    context = {'title': 'Profile', 'form': form}
    return render(request, 'accounts/profile.html', context)


@login_required
def profile_management(request):
    # Updating our user's username and email
    user_form = UserUpdateForm(instance=request.user)
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('user_account:profile')
    context = {'title': 'Update profile management', 'user_form': user_form}
    return render(request, 'accounts/profile_management.html', context)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = PasswordChangingPassword
    success_message = 'Your password was changed'
    success_url = reverse_lazy('user_account:login')


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Email confirmation'
    template_name = 'accounts/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('products:home'))


@login_required
def delete_account(request):
    user = User.objects.get(id=request.user.id)
    if request.method == 'POST':
        messages.success(request, 'Account delete successfully')
        user.delete()
        return redirect('products:home')
    context = {'title': 'Delete Account'}
    return render(request, 'accounts/delete_account.html', context)


@login_required
def manage_shipping(request):
    try:
        # Account user with shipment information
        shipping = ShippingAddress.objects.get(user=request.user.id)
    except ShippingAddress.DoesNotExist:
        # Account user with no  shipment information
        shipping = None
    form = ShippingForm(instance=shipping)
    if request.method == 'POST':
        form = ShippingForm(request.POST, instance=shipping)
        if form.is_valid():
            # Assign the user FK on the object
            shipping_user = form.save(commit=False)
            # Adding the FK itself
            shipping_user.user = request.user
            shipping_user.save()
            return redirect('user_account:profile')
    context = {'title': 'Manage Shipping', 'form': form}
    return render(request, 'accounts/manage_shipping.html', context)


