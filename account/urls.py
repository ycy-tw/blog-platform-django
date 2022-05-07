from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import (
    CustomPasswordResetForm,
    CustomSetPasswordForm,
)
from .views import (
    login_view,
    logout_view,
    register_view,
)

app_name = 'account'

urlpatterns = [
    path('login', login_view, name='login'),
    path('logout', logout_view, name='logout'),
    path('register', register_view, name='register'),

    # reset password
    path('reset',
         auth_views.PasswordResetView.as_view(
             template_name='account/password_reset.html',
             email_template_name='account/password_reset_email.html',
             form_class=CustomPasswordResetForm,
             success_url=reverse_lazy('account:password_reset_done'),
         ), name='password_reset'),

    path('reset/done',
         auth_views.PasswordResetDoneView.as_view(
             template_name='account/password_reset_sent.html'
         ), name='password_reset_done'),

    path('confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='account/password_reset_confirm.html',
             success_url=reverse_lazy('account:password_reset_complete'),
             form_class=CustomSetPasswordForm,
         ), name='password_reset_confirm'),

    path('complete',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='account/password_reset_complete.html',
         ), name='password_reset_complete'),
]
