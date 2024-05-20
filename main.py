from typing import Union
from fastapi import FastAPI # type: ignore
import uvicorn
import os

from routes.urls import routeMap

app = FastAPI()

app.include_router(routeMap)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


