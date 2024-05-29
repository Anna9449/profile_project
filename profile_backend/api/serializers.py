from datetime import timedelta

from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.utils.timezone import now
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import Code, ProfileUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = ProfileUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password')

    def validate_password(self, value):
        validate_password(value)
        return make_password(value)


class UserCodeSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, attrs):
        user = authenticate(email=attrs['email'],
                            password=attrs['password'])
        if user is None:
            raise serializers.ValidationError('Проверьте корректность введенных данных.')
        if user.block_time > now():
            raise serializers.ValidationError(f'Доступ заблокирован до {user.block_time}')
        return attrs


class GetFromCodeTokenSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['otp_code'] = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)

        if not Code.objects.filter(user=self.user).exists():
            raise serializers.ValidationError(
                'Необходимо сначала получить код.'
            )
        if self.user.block_time > now():
            raise serializers.ValidationError(
                f'Доступ заблокирован до {self.user.block_time}'
            )
        if self.user.code.created_at < now() - timedelta(minutes=3):
            self.user.code.delete()
            raise serializers.ValidationError(
                'Время действия OTP кода истекло. Запросите новый OTP код.'
            )
        if self.user.code.code == attrs['otp_code']:
            self.user.code.delete()
            return data
        elif self.user.code.count_attempt != 0:
            self.user.code.count_attempt -= 1
            self.user.code.save()
            raise serializers.ValidationError(
                ('Неверный OTP код. Попробуйте еще раз.'
                 f' Осталось попыток - {self.user.code.count_attempt}.')
            )
        else:
            self.user.code.delete()
            self.user.block_time = now() + timedelta(hours=1)
            self.user.save()
            raise serializers.ValidationError('Доступ заблокирован на 1 час.')
