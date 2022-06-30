import uvicorn

from .settings import settings


uvicorn.run(
    'workout_api.app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)

# in terminal:
#  uvicorn workout_api.app:app --host 127.0.0.1 --port 5000