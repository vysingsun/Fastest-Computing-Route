from typing import Union
from fastapi import FastAPI # type: ignore
import uvicorn
import os
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes.urls import routeMap

app = FastAPI()

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the route map
app.include_router(routeMap)

templates = Jinja2Templates(directory="templates")
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


