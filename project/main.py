import uvicorn
from api import create_app

app = create_app()

if __name__ == '__main__':
    from database.models import init_db
    from api import register_cron
    # register_cron()
    init_db()
    uvicorn.run(app="main:app", host="0.0.0.0", port=8800, reload=True, debug=True)
