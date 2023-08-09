from django.urls import path

from core.views import index, SignInView, logout_user, LogInView

urlpatterns = [
    path('', index, name='main'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('logout/', logout_user, name='logout'),
]