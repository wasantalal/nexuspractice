from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_env():
    value = os.getenv("DOCKER_ENV_VALUE", "not set")
    return {"env_value": value}