from pathlib import Path
import os
from random import randint

from faker import Faker
from dotenv import load_dotenv
from django.contrib.auth import get_user_model

from core.models import Country, City, Hotel
from travel_shop.settings import BASE_DIR


fake = Faker("ru_RU")
load_dotenv(Path(BASE_DIR, '.env'))


def insert_superuser(apps, schema_editor):
    User = get_user_model()
    login = os.getenv('login')
    password = os.getenv('password')
    User.objects.create_superuser(login, password)


def insert_countries(apps, schema_editor):
    Country = apps.get_model('core', 'Country')
    objs = (Country(name=fake.unique.country(), image='countries/1.jpg') for _ in range(6))
    Country.objects.bulk_create(objs=objs)


def insert_cities(apps, schema_editor):
    City = apps.get_model('core', 'City')
    for country in Country.objects.all():
        objs = (City(
            name=fake.unique.city(),
            image='cities/random_city.jpg',
            ticket_price=randint(1000, 10000),
            country_id=country.pk
        )
            for _ in range(6))
        City.objects.bulk_create(objs=objs, batch_size=100)


def insert_hotels(apps, schema_editor):
    Hotel = apps.get_model('core', 'Hotel')
    for city in City.objects.all():
        objs = (Hotel(
            name=fake.unique.company(),
            image='hotels/random_hotel.jpg',
            description=fake.text(),
            stars=randint(1, 5),
            city_id=city.pk
        )
            for _ in range(6))
        Hotel.objects.bulk_create(objs=objs, batch_size=100)


def insert_rooms(apps, schema_editor):
    Room = apps.get_model('core', 'Room')
    for hotel in Hotel.objects.all():
        objs = (Room(
            room_number=fake.unique.randomNumber(5, 50),
            image='rooms/random_room.jpg',
            description=fake.text(2000),
            price_per_day=randint(1000, 12000),
            hotel_id=hotel.pk
        )
            for _ in range(6))
        Room.objects.bulk_create(objs=objs, batch_size=100)


