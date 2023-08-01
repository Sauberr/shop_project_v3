from django.urls import path

from user_account.views import *

app_name = 'user_account'


urlpatterns = [
    path('check-email/', check_email, name='check-email'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', profile, name='profile'),
    # path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('logout/', logout, name='logout'),
    path('password-reset/', login_required(ResetPasswordView.as_view()), name='password_reset'),
    path('password-change/', login_required(ChangePasswordView.as_view()), name='password_change'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),
    path('delete-account/', delete_account, name='delete-account'),
    path('profile-management/', profile_management, name='profile-management'),
    path('manage-shipping/', manage_shipping, name='manage-shipping'),
]