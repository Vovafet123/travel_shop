import os

from django.db import models
from django.db.models import Q, Max

from core.models import User


def get_image_path(instance, filename):
    current_index = None
    if isinstance(instance, Country):
        directory = 'countries'
        current_index = Country.objects.aggregate(max_pk=Max('pk'))['max_pk']
    elif isinstance(instance, City):
        directory = 'cities'
        current_index = City.objects.aggregate(max_pk=Max('pk'))['max_pk']
    elif isinstance(instance, Hotel):
        directory = 'hotels'
        current_index = Hotel.objects.aggregate(max_pk=Max('pk'))['max_pk']
    elif isinstance(instance, Room):
        directory = 'rooms'
        current_index = Room.objects.aggregate(max_pk=Max('pk'))['max_pk']
    else:
        directory = ''

    current_index = current_index + 1 if current_index else 1
    file_extension = filename.split('.')[-1]
    return os.path.join(directory, f'{current_index}.{file_extension}')


class DateTimeMixin(models.Model):
    created_datetime = models.DateTimeField(auto_now_add=True)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(DateTimeMixin):
    name = models.CharField(verbose_name="Наименование", max_length=100, unique=True)
    image = models.ImageField(verbose_name="Картинка", upload_to=get_image_path, blank=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class City(DateTimeMixin):
    name = models.CharField(verbose_name="Наименование", max_length=100)
    image = models.ImageField(verbose_name="Картинка", upload_to=get_image_path, blank=True)
    ticket_price = models.DecimalField(verbose_name="Цена билета", max_digits=10, decimal_places=2)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        unique_together = ('name', 'country')

        constraints = [
            models.CheckConstraint(check=Q(ticket_price__gte=0.00), name='ticket_price_constraint'),
        ]

    def __str__(self):
        return self.name


class HotelService(DateTimeMixin):
    name = models.CharField(verbose_name="Название услуги", max_length=100, unique=True)

    class Meta:
        verbose_name = "Услуги в отеле"
        verbose_name_plural = "Услуги в отелях"

    def __str__(self):
        return self.name


class Hotel(DateTimeMixin):
    name = models.CharField(verbose_name="Название отеля", max_length=150)
    image = models.ImageField(verbose_name="Картинка", upload_to=get_image_path, blank=True)
    description = models.TextField(verbose_name="Описание отеля", max_length=10000)
    stars = models.SmallIntegerField(verbose_name="Звезды отеля")
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    service = models.ManyToManyField(HotelService, through='HotelHotelService')

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        constraints = [
            models.CheckConstraint(check=models.Q(stars__gte=1) & models.Q(stars__lte=5), name='stars_constraint'),
        ]

    def __str__(self):
        return self.name


class Room(DateTimeMixin):
    image = models.ImageField(verbose_name="Картинка", upload_to=get_image_path, blank=True)
    room_number = models.PositiveIntegerField(verbose_name="Номер комнаты")
    description = models.TextField(verbose_name="Описание комнаты", max_length=10000, default="")
    price_per_day = models.DecimalField('Цена за сутки', max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Апартаменты"
        verbose_name_plural = "Апартаменты"

    def __str__(self):
        return self.room_number


class Voucher(DateTimeMixin):
    total_price = models.DecimalField(verbose_name='Общая стоимость', max_digits=10, decimal_places=2)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"
        constraints = [
            models.CheckConstraint(check=models.Q(total_price__gte=0), name='min_total_price_constraint'),
        ]

    def __str__(self):
        return self.hotel.name


class HotelHotelService(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hotel', 'hotel_service')


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hotel', 'room')
