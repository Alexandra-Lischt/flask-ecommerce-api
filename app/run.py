from apiflask import APIFlask

from app import create_app
from app.config import settings

app: APIFlask = create_app()

if __name__ == "__main__":
    app.run(
        host=settings.FLASK_RUN_HOST,
        port=settings.FLASK_RUN_PORT,
        debug=settings.FLASK_DEBUG,
    )
