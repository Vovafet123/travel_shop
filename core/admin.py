from django.contrib import admin
from django.db.models import Sum
from django.forms import Textarea

from core.models.site_models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'balance', 'is_premium', 'is_superuser')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    class CountryCitiesInline(admin.StackedInline):
        model = City
        extra = 1

    def quantity(self, obj):
        return obj.city_set.aggregate(quantity=Sum('quantity'))['quantity']

    list_display = ("name", "image")
    inlines = (CountryCitiesInline,)

    search_fields = ('name',)
    list_filter = ("name",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    class CitiesHostelInline(admin.StackedInline):
        model = Hotel
        extra = 1

    list_display = ("name", "ticket_price", "image")
    inlines = (CitiesHostelInline,)

    search_fields = ('name',)
    list_filter = ("name", "country")


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    class HotelServiceInline(admin.StackedInline):
        model = HotelHotelService
        extra = 1

    class HotelRoomsInline(admin.StackedInline):
        model = HotelRoom
        extra = 1

    list_display = ("name", 'description', "stars", "city", "image")
    inlines = (HotelServiceInline, HotelRoomsInline)

    search_fields = ('name',)
    list_filter = ("name", 'description', "stars", "city")

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 100})},
    }


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("room_number", "price_per_day", "image")


@admin.register(Voucher)
class VoucherAdmin(admin.ModelAdmin):
    list_display = ("hotel", "user", "total_price")

    search_fields = ('hotel',)
    list_filter = ("hotel", "user")


@admin.register(HotelService)
class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ("name",)
