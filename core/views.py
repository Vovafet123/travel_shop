from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from core.forms import AuthRegForm
from core.models import Country, City, Hotel, HotelRoom, Room


def index(request):
    return render(request, 'core/index.html',)


class RegisterUser(CreateView):
    form_class = AuthRegForm
    template_name = 'core/registration.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        form.save()
        username = self.request.POST['login']
        password = self.request.POST['password1']
        print(username, password)
        user = authenticate(username=username, password=password)
        login(self.request, user)
        return redirect(self.success_url)


def logout_user(request):
    logout(request)
    return redirect('main')


class LogInView(LoginView):
    form_class = AuthenticationForm
    template_name = 'core/login.html'
    context = {'form': form_class}

    def get_success_url(self):
        return reverse_lazy('main')  # TODO привести к однообразию вход и регистрацию через django


def countries_view(request):
    countries = Country.objects.all()
    context = {'countries': countries}
    return render(request, 'core/countries.html', context=context)


def cities_view(request, country):
    cities = City.objects.filter(country__name=country)
    context = {'cities': cities, 'country': country}
    return render(request, 'core/cities.html', context=context)


def hotels_view(request, country, city):
    hotels = Hotel.objects.filter(city__name=city)
    context = {'hotels': hotels, 'city': city, 'country': country}
    return render(request, 'core/hotels.html', context=context)


def hotels_room_view(request, country, city, hotel):
    hotel_id = Hotel.objects.get(name=hotel).pk
    rooms = Room.objects.filter(hotel_id=hotel_id)
    context = {'rooms': rooms, 'hotel': hotel, 'city': city, 'country': country}
    return render(request, 'core/rooms.html', context=context)


def date_voucher_view(request, country, city, hotel, room):
    room = Room.objects.filter(hotel__name=hotel).get(room_number=room)
    hotel = Hotel.objects.get(name=hotel)
    context = {'room': room, 'hotel': hotel, 'city': city, 'country': country}
    return render(request, 'core/date_voucher.html', context=context)
