# Generated by Django 3.2.16 on 2024-05-23 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20240523_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imageuser',
            name='image',
            field=models.ImageField(blank=True, default='default/no_image.jpg', upload_to='', verbose_name='Аватар пользователя'),
        ),
        migrations.AlterField(
            model_name='imageuser',
            name='image_medium',
            field=models.ImageField(blank=True, default='default/no_image_medium.jpg', upload_to='', verbose_name='Аватар пользователя m'),
        ),
        migrations.AlterField(
            model_name='imageuser',
            name='image_small',
            field=models.ImageField(blank=True, default='default/no_image_small.jpg', upload_to='', verbose_name='Аватар пользователя s'),
        ),
    ]
