import uvicorn
import os


if __name__ == '__main__':
    del os.environ['GOOGLE_CREDENTIALS']
    os.environ['DATABASE_URL'] = "https://rbacioo-default-rtdb.firebaseio.com/"
    uvicorn.run("app.app:app", port=8000, reload=True)