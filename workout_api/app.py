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
        'name': 'reports',
        'description': 'Импорт и экспорт CSV-отчетов',
    },
]

app = FastAPI(
    title='Workout service',
    description='Сервис учета тренеровок',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(api.router)
