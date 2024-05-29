import random
from http import HTTPStatus

from drf_spectacular.utils import OpenApiParameter, extend_schema
from django.contrib.auth import authenticate
from django.utils.timezone import now
from rest_framework import generics, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .serializers import (GetFromCodeTokenSerializer,
                          UserCodeSerializer, UserSerializer)
from .schema import response_204, response_302, response_400, response_401
from .tasks import send_feedback_email_task
from users.models import ProfileUser, Code


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    '''Профиль пользователя.'''
    queryset = ProfileUser.objects.all()
    serializer_class = UserSerializer
    http_method_names = ('get', 'post', 'patch', 'delete')

    def get_permissions(self):
        if self.action == 'create':
            return (AllowAny(),)
        return super().get_permissions()

    def get_object(self):
        return self.request.user

    @extend_schema(responses={201: UserSerializer,
                              400: response_400})
    def create(self, request, *args, **kwargs):
        return super().create(*args, **kwargs)

    @extend_schema(
            methods=('GET',),
            responses={200: UserSerializer,
                       401: response_401}
    )
    @extend_schema(
            methods=('PATCH',),
            responses={200: UserSerializer,
                       400: response_400,
                       401: response_401}
    )
    @extend_schema(
            methods=('DELETE',),
            responses={204: response_204,
                       401: response_401}
    )
    @action(methods=('GET', 'PATCH', 'DELETE'),
            detail=False, url_path='profile')
    def profile(self, request):
        user = self.get_object()
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                context=self.get_serializer_context(),
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        if user:
            user.delete()
            return Response(status=HTTPStatus.NO_CONTENT)
        return Response(status=HTTPStatus.BAD_REQUEST)


@extend_schema(responses={200: TokenObtainPairSerializer,
                          400: response_400})
class TokenView(TokenObtainPairView):
    '''Получение токена.'''
    serializer_class = GetFromCodeTokenSerializer


@extend_schema(responses={201: UserCodeSerializer,
                          302: response_302,
                          400: response_400})
class GetCodeView(generics.CreateAPIView):
    '''Получение кода подтверждение.'''
    permission_classes = (AllowAny,)
    serializer_class = UserCodeSerializer

    def code_generation(self):
        list_random_numbers = random.sample([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], 6)
        return "".join(map(str, list_random_numbers))

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(email=request.data['email'],
                            password=request.data['password'])
        if Code.objects.filter(user=user).exists():
            return Response(
                data={'detail': f'Код уже отправлен. Проверьте почту {user.email}'},
                status=HTTPStatus.FOUND
            )
        code = self.code_generation()
        send_feedback_email_task.delay(user.email,
                                       f'Ваш код подтверждения: {code}')
        Code.objects.create(user=user, code=code, created_at=now())
        return Response(
            data={'detail': f'Код подтверждения отправлен на {user.email}'},
            status=HTTPStatus.CREATED
        )
