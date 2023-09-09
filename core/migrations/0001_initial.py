# Generated by Django 4.2.2 on 2023-09-09 09:13

import core.models.auth
import core.models.site_models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_staff', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('login', models.CharField(max_length=20, unique=True, verbose_name='Логин')),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10, verbose_name='Баланс')),
                ('is_premium', models.BooleanField(default=False, verbose_name='Премиум')),
                ('premium_expiration_date', models.DateField(blank=True, default=None, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
            managers=[
                ('objects', core.models.auth.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, upload_to=core.models.site_models.get_image_path, verbose_name='Картинка')),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена билета')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('image', models.ImageField(blank=True, upload_to=core.models.site_models.get_image_path, verbose_name='Картинка')),
            ],
            options={
                'verbose_name': 'Страна',
                'verbose_name_plural': 'Страны',
            },
        ),
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=150, verbose_name='Название отеля')),
                ('image', models.ImageField(blank=True, upload_to=core.models.site_models.get_image_path, verbose_name='Картинка')),
                ('description', models.TextField(max_length=10000, verbose_name='Описание отеля')),
                ('stars', models.SmallIntegerField(verbose_name='Звезды отеля')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.city')),
            ],
            options={
                'verbose_name': 'Отель',
                'verbose_name_plural': 'Отели',
            },
        ),
        migrations.CreateModel(
            name='HotelService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название услуги')),
            ],
            options={
                'verbose_name': 'Услуги в отеле',
                'verbose_name_plural': 'Услуги в отелях',
            },
        ),
        migrations.CreateModel(
            name='Voucher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Общая стоимость')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hotel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Билет',
                'verbose_name_plural': 'Билеты',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_datetime', models.DateTimeField(auto_now_add=True)),
                ('updated_datetime', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(blank=True, upload_to=core.models.site_models.get_image_path, verbose_name='Картинка')),
                ('room_number', models.PositiveIntegerField(verbose_name='Номер комнаты')),
                ('description', models.TextField(default='', max_length=10000, verbose_name='Описание комнаты')),
                ('price_per_day', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за сутки')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hotel')),
            ],
            options={
                'verbose_name': 'Апартаменты',
                'verbose_name_plural': 'Апартаменты',
            },
        ),
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hotel')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.room')),
            ],
        ),
        migrations.CreateModel(
            name='HotelHotelService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hotel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hotel')),
                ('hotel_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.hotelservice')),
            ],
        ),
        migrations.AddField(
            model_name='hotel',
            name='service',
            field=models.ManyToManyField(through='core.HotelHotelService', to='core.hotelservice'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.country'),
        ),
        migrations.AddConstraint(
            model_name='voucher',
            constraint=models.CheckConstraint(check=models.Q(('total_price__gte', 0)), name='min_total_price_constraint'),
        ),
        migrations.AlterUniqueTogether(
            name='hotelroom',
            unique_together={('hotel', 'room')},
        ),
        migrations.AlterUniqueTogether(
            name='hotelhotelservice',
            unique_together={('hotel', 'hotel_service')},
        ),
        migrations.AddConstraint(
            model_name='hotel',
            constraint=models.CheckConstraint(check=models.Q(('stars__gte', 1), ('stars__lte', 5)), name='stars_constraint'),
        ),
        migrations.AddConstraint(
            model_name='city',
            constraint=models.CheckConstraint(check=models.Q(('ticket_price__gte', 0.0)), name='ticket_price_constraint'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'country')},
        ),
    ]
