from django.db import models
from django.db.models import Q


class DateTimeMixin(models.Model):
    create_datetime = models.DateTimeField(auto_now_add=True)
    update_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(DateTimeMixin):
    name = models.CharField("Страна", max_length=100, unique=True)

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class City(DateTimeMixin):
    name = models.CharField("Город", max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True, blank=True)
    ticket_price = models.DecimalField("Цена билета", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        unique_together = ('name', 'country',)

        constraints = [
            models.CheckConstraint(check=Q(ticket_price__gte=0.00), name='ticket_price_constraint')

            # TODO Страна и город вместе должны быть уникальны, минимальная цена > 0
        ]

    def __str__(self):
        return self.name


class HotelService(DateTimeMixin):
    name = models.CharField("Название услуги", max_length=100, unique=True)

    class Meta:
        verbose_name = "Услуги в отеле"
        verbose_name_plural = "Услуги в отелях"

    def __str__(self):
        return self.name


class Room(DateTimeMixin):
    room_type = models.CharField("Тип номера", max_length=100)  # чойсез


    class Meta:
        verbose_name = "Апартаменты"
        verbose_name_plural = "Апартаменты"

    def __str__(self):
        return self.room_type


class Hotel(DateTimeMixin):
    name = models.CharField("Название отеля", max_length=150)
    description = models.TextField("Описание отеля", max_length=10000)
    stars = models.SmallIntegerField("Звезды отеля")
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    service = models.ManyToManyField(HotelService, through='HotelHotelService')
    rooms = models.ManyToManyField(Room, through='HotelRoom')

    class Meta:
        verbose_name = "Отель"
        verbose_name_plural = "Отели"
        constraints = [
            models.CheckConstraint(check=models.Q(stars__gte=1) & models.Q(stars__lte=5), name='stars_constraint')

            # TODO сделать ограничения для stars от 1 до 5
        ]

    def __str__(self):
        return self.name


class Voucher(DateTimeMixin):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, blank=True, null=True)
    days = models.PositiveSmallIntegerField("Количество дней в путевке")
    departure_date = models.DateTimeField("Даты вылета")

    class Meta:
        verbose_name = "Билет"
        verbose_name_plural = "Билеты"

    def __str__(self):
        return self.hotel.name

    # TODO исправить на мэнитумэни----


class HotelHotelService(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    hotel_service = models.ForeignKey(HotelService, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('hotel', 'hotel_service',)

        constraints = [
            # TODO Добавить уникальность в паре
        ]


class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    price_per_day = models.DecimalField('Цена за сутки', max_digits=10, decimal_places=2)
    count = models.PositiveSmallIntegerField('Кол-во комнат')

    class Meta:
        unique_together = ('hotel', 'room',)
        constraints = [
            models.CheckConstraint(check=models.Q(price_per_day__gt=0), name='price_per_day_constraint')

            # TODO Добавить уникальность в паре отель-комната, минимальная цена > 0
        ]

