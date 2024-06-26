# Generated by Django 3.2.16 on 2024-05-23 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20240523_1038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='imageuser',
            old_name='pofile_image',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='profileuser',
            name='avatar',
        ),
        migrations.AddField(
            model_name='imageuser',
            name='image',
            field=models.ImageField(blank=True, upload_to='', verbose_name='Аватар пользователя'),
        ),
    ]
