from fastapi import FastAPI

from . import api

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Авторизация и регистрация',
    },
    {
        'name': 'users',
        'description': 'Создание, редактирование, удаление и просмотр пользователей',
    },
    {
        'name': 'not_registered_users',
        'description': 'Создание, редактирование, удаление и просмотр пользователей,'
                       'созданных тренерами, но еще не зарегистрированных самостоятельно',
    },
    {
        'name': 'trainers',
        'description': 'Создание, редактирование, удаление и просмотр тренеров/организаторов',
    },
    {
        'name': 'groups',
        'description': 'Создание, редактирование, удаление и просмотр групп',
    },
]

app = FastAPI(
    title='Workout service',
    description='Сервис учета тренеровок',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)
