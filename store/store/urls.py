from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path, re_path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('drf-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include('products.urls', namespace='products')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('user_account/', include('user_account.urls', namespace='user_account')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('captcha/', include('captcha.urls')),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password/password_reset_complete.html'),
         name='password_reset_complete'),

    path('accounts/', include('allauth.urls')),

]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



