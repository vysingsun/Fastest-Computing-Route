from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.models import Variable
from services.v1.requests_route import RequestRoute
from services.service_api import get_route_osrm_grab, get_route_osrm_grab2
from services.views import CurrentView

routeMap = APIRouter()

@routeMap.get('/')
def gets():
    return get_route_osrm_grab2()

  

@routeMap.post("/api/v1/route/")
async def open_street_map(request: Request):
    data = await request.json()
    return get_route_osrm_grab(data)

