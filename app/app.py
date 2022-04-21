from fastapi import FastAPI
from fastapi.params import Body
from fastapi.exceptions import HTTPException
import time


app = FastAPI(title="Rbacc.io Backend")


@app.get("/")
async def root() -> dict:
    return {"message": "Hello World"}
