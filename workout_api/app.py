from fastapi import FastAPI

from . import api
from .database import database

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


@app.on_event('startup')
async def startup():
    await database.connect()
    print("!!!  DB CONNECTED   !!!!")


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
    print('!!!   DB DISCONNECTED   !!!')

app.include_router(api.router)
