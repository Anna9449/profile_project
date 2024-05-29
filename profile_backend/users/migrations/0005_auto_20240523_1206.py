# Generated by Django 3.2.16 on 2024-05-23 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20240523_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageuser',
            name='image',
            field=models.ImageField(default='default/no_image.jpg', upload_to='', verbose_name='Аватар пользователя'),
        ),
        migrations.AlterField(
            model_name='imageuser',
            name='image_medium',
            field=models.ImageField(default='default/no_image_medium.jpg', upload_to='', verbose_name='Аватар пользователя m'),
        ),
        migrations.AlterField(
            model_name='imageuser',
            name='image_small',
            field=models.ImageField(default='default/no_image_small.jpg', upload_to='', verbose_name='Аватар пользователя s'),
        ),
        migrations.AlterField(
            model_name='imageuser',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]