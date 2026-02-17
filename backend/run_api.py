from app.api import init_api
from app.database import init_db

app = init_api()
init_db()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
