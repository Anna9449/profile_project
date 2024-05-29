from django.contrib.auth.models import AbstractUser
from django.db import models

from .const import MAX_COUNT_ATTEMPT, MAX_LENGTH, MAX_LENGTH_CODE


class ProfileUser(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    email = models.EmailField('email', max_length=MAX_LENGTH, unique=True)
    username = models.CharField(max_length=MAX_LENGTH, blank=True)
    block_time = models.DateTimeField(
        'Время окончания блокировки профиля', auto_now_add=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Code(models.Model):
    user = models.OneToOneField(ProfileUser, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    code = models.CharField('Код', max_length=MAX_LENGTH_CODE)
    created_at = models.DateTimeField(
        'Дата и время выдачи кода', auto_now_add=True
    )
    count_attempt = models.SmallIntegerField('Количество попыток',
                                             blank=True,
                                             default=MAX_COUNT_ATTEMPT)

    class Meta:
        verbose_name = 'Код'
        verbose_name_plural = 'Коды'
