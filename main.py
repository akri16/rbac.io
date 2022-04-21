import uvicorn
import os


if __name__ == '__main__':
    os.environ['DATABASE_URL'] = "https://rbacioo-default-rtdb.firebaseio.com/"
    uvicorn.run("app.app:app", port=8000, reload=True)