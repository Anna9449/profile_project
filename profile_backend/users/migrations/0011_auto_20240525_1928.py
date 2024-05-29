# Generated by Django 3.2.16 on 2024-05-25 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_auto_20240525_1808'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='count_attempt',
            field=models.SmallIntegerField(blank=True, default=3),
        ),
        migrations.AlterField(
            model_name='code',
            name='code',
            field=models.CharField(default='000000', max_length=6, verbose_name='Код'),
        ),
    ]