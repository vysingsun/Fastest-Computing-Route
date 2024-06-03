from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.models import Variable
from services.v1.requests_route import RequestRoute
from services.service_api import get_route_osrm_grab, get_route_osrm_grab2, get_route_waze

routeMap = APIRouter()

@routeMap.get('/')
async def gets(request: Request):
    data = await request.json()
    print("Data: ", data)
    return get_route_osrm_grab2(data)

@routeMap.post("/api/v1/route/")
async def open_street_map(request: Request):
    data = await request.json()
    return get_route_osrm_grab(data)

@routeMap.post("/api/v2/route/")
async def waze_route(request: Request):
    data = await request.json()
    return get_route_waze(data)

@routeMap.get("/api/v3/route/")
async def waze_route(request: Request):
    data = await request.json()
    return get_route_waze(data)

