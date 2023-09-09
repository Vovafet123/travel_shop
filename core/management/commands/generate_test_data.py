import os
from random import randint

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from core.models import Country, City, Hotel, Room


class Command(BaseCommand):
    help = 'Генерация тестовых записей'
    fake = Faker('ru_RU')

    def handle(self, *args, **kwargs):
        # self.insert_superuser()
        self.insert_countries()
        self.insert_cities()
        self.insert_hotels()
        self.insert_rooms()

    def insert_superuser(self):
        User = get_user_model()
        login = os.getenv('ADMIN_LOGIN')
        password = os.getenv('ADMIN_PASSWORD')
        User.objects.create_superuser(login, password)

    def insert_countries(self):
        objs = (Country(name=self.fake.unique.country(), image='countries/1.jpg') for _ in range(6))
        Country.objects.bulk_create(objs=objs)

    def insert_cities(self):
        for country in Country.objects.all():
            objs = (City(
                name=self.fake.unique.city(),
                image='cities/random_city.jpg',
                ticket_price=randint(1000, 10000),
                country_id=country.pk
            )
                for _ in range(6))
            City.objects.bulk_create(objs=objs, batch_size=100)

    def insert_hotels(self):
        for city in City.objects.all():
            objs = (Hotel(
                name=self.fake.unique.company(),
                image='hotels/random_hotel.jpg',
                description=self.fake.text(),
                stars=randint(1, 5),
                city_id=city.pk
            )
                for _ in range(6))
            Hotel.objects.bulk_create(objs=objs, batch_size=100)

    def insert_rooms(self):
        for hotel in Hotel.objects.all():
            objs = (Room(
                room_number=self.fake.random_number(),
                image='rooms/random_room.jpg',
                description=self.fake.text(2000),
                price_per_day=randint(1000, 12000),
                hotel_id=hotel.pk
            )
                for _ in range(6))
            Room.objects.bulk_create(objs=objs, batch_size=100)
