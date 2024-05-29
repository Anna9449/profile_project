from drf_spectacular.utils import OpenApiResponse


response_204 = OpenApiResponse(
    response=None,
    description='Объект удален.'
)

response_302 = OpenApiResponse(
    response=None,
    description='Код уже отправлен.'
)

response_400 = OpenApiResponse(
    response=None,
    description='Проверьте корректность введенных данных.'
)

response_401 = OpenApiResponse(
    response=None,
    description='Необходимо авторизоваться.'
)
