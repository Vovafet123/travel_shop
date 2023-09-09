from django.urls import path

from core.views import (
    index,
    RegisterUser,
    logout_user,
    LogInView,
    countries_view,
    cities_view,
    hotels_view,
    hotels_room_view,
    date_voucher_view,
)

urlpatterns = [
    path('', index, name='main'),
    path('registration/', RegisterUser.as_view(), name='registration'),
    path('log_in/', LogInView.as_view(), name='log_in'),
    path('logout/', logout_user, name='logout'),
    path('countries/', countries_view, name='countries'),
    path('<str:country>/', cities_view, name='cities'),
    path('<str:country>/<str:city>/', hotels_view, name='hotels'),
    path('<str:country>/<str:city>/<str:hotel>/', hotels_room_view, name='hotels_room'),
    path('<str:country>/<str:city>/<str:hotel>/<str:room>/book/', date_voucher_view, name='date_voucher'),
]