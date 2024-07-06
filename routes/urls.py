from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.models import Variable
from services.v1.requests_route import RequestRoute
from services.service_api import get_route_osrm_grab, get_route_waze, get_route_multiple_points_osrm_grab
from fastapi.templating import Jinja2Templates
import httpx
import requests

routeMap = APIRouter()
templates = Jinja2Templates(directory="templates")

# Google Map
@routeMap.get('/google_map')
async def index(request: Request):
    data = {
        "start_point": {
            "lat": 11.584637323468067,
            "lng": 104.90419534099364
        },
        "end_point": {
            "lat": 11.598114,
            "lng": 104.875190
        },
        "scan": True,
        "traffic": True,
    }
    print(data)
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/route", json=data)
        response_data = response.json()
    gcoor = []
    for i in range(len(response_data['geometries']['route'])):
        gcoor.append('{lat:'+str(response_data['geometries']['route'][i][0])+',lng:'+str(response_data['geometries']['route'][i][1])+'}')
    gcoor=','.join(gcoor)
    
    #mapping Data for block traffic
    bcoor = []
    for block_scan in response_data['geometries']['blocks_scan']:
        for coordinate in block_scan['block']:
            bcoor.append(f'{{lat:{coordinate[0]},lng:{coordinate[1]}}}')
    bcoor = ','.join(bcoor)

    context = {
        'model': "Car",
        'distance': response_data['geometries']['distance'] / 1000,
        # 'duration': strftime("%Hh:%Mm:%Ss", gmtime(response_data['geometries']['duration'])),
        'map': gcoor,
        'lat_s': data['start_point']['lat'],
        'lng_s': data['start_point']['lng'],
        'lat_e': data['end_point']['lat'],
        'lng_e': data['end_point']['lng'],
        'delay_map': bcoor,
    }
    return templates.TemplateResponse(name="googleMap.html", request=request, context=context)

@routeMap.get('/google_map/multiple')
async def index(request: Request):
    data = {
        "start_point": {
            "lat": 11.584637323468067,
            "lng": 104.90419534099364
        },
        "end_point": {
            "lat": 11.579015,
            "lng": 104.917060
        },
        "scan": True,
        "traffic": True,
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/route/multiplepoints", json=data)
        response_data = response.json()
        
    gcoor = []
    for i in range(len(response_data['geometries']['route'])):
        gcoor.append('{lat:'+str(response_data['geometries']['route'][i][0])+',lng:'+str(response_data['geometries']['route'][i][1])+'}')
    gcoor=','.join(gcoor)
    
    #mapping Data for block traffic
    bcoor = []
    for block_scan in response_data['geometries']['blocks_scan']:
        for coordinate in block_scan['block']:
            bcoor.append(f'{{lat:{coordinate[0]},lng:{coordinate[1]}}}')
    bcoor = ','.join(bcoor)

    context = {
        'model': "Car",
        # 'distance': response_data['geometries']['distance'] / 1000,
        # 'duration': strftime("%Hh:%Mm:%Ss", gmtime(response_data['geometries']['duration'])),
        'map': gcoor,
        'lat_s': data['start_point']['lat'],
        'lng_s': data['start_point']['lng'],
        'lat_e': data['end_point']['lat'],
        'lng_e': data['end_point']['lng'],
        'delay_map': bcoor,
    }
    return templates.TemplateResponse(name="googleMap.html", request=request, context=context)

# # Open Street Map
@routeMap.get('/open_street_map')
async def index(request: Request):
    data = {
        "start_point": {
            "lat": 11.584637323468067,
            "lng": 104.90419534099364
        },
        "end_point": {
            "lat": 11.598114,
            "lng": 104.875190
        },
        "scan": True,
        "traffic": True,
    }
    print(data)
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8000/api/v1/route", json=data)
        response_data = response.json()
    context = {
        'model': "Car",
        'distance': response_data['geometries']['distance'] / 1000,
        # 'duration': strftime("%Hh:%Mm:%Ss", gmtime(response_data['geometries']['duration'])),
        'map': response_data['geometries']['route'],
        'lat_s': data['start_point']['lat'],
        'lng_s': data['start_point']['lng'],
        'lat_e': data['end_point']['lat'],
        'lng_e': data['end_point']['lng'],
        'data_delay': response_data['geometries']['blocks_scan'],
    }
    return templates.TemplateResponse(name="osrm.html", request=request, context=context)

@routeMap.get('/')
async def index(request: Request):
    data = {
        "start_point": {
            "lat": 11.584637323468067,
            "lng": 104.90419534099364
        },
        "end_point": {
            "lat": 11.598114,
            "lng": 104.875190
        },
        "scan": True,
        "traffic": True,
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post("https://fastest-computing-route-dev.onrender.com/api/v2/route/waze", json=data)
        response_data = response.json()
    context = {
        'model': "Car",
        'distance': response_data['geometries']['distance'] / 1000,
        # 'duration': strftime("%Hh:%Mm:%Ss", gmtime(response_data['geometries']['duration'])),
        'map': response_data['geometries']['route'],
        'lat_s': data['start_point']['lat'],
        'lng_s': data['start_point']['lng'],
        'lat_e': data['end_point']['lat'],
        'lng_e': data['end_point']['lng'],
        'data_delay': response_data['geometries']['blocks_scan'],
    }
    return templates.TemplateResponse(name="osrm.html", request=request, context=context)

@routeMap.get('/multiple')
async def index(request: Request):
    data = {
        "start_point": {
            "lat": 11.584637323468067,
            "lng": 104.90419534099364
        },
        "end_point": {
            "lat": 11.553859,
            "lng": 104.895052
        },
        "scan": True,
        "traffic": True,
    }
    async with httpx.AsyncClient(timeout=20.0) as client:
        response = await client.post("https://fastest-computing-route-dev.onrender.com/api/v1/route/multiplepoints", json=data)
        response_data = response.json()
        
    print('Traffic',response_data['geometries']['blocks_scan'])
    context = {
        'model': "Car",
        # 'distance': response_data['geometries']['distance'] / 1000,
        # 'duration': strftime("%Hh:%Mm:%Ss", gmtime(response_data['geometries']['duration'])),
        'map': response_data['geometries']['route'],
        'lat_s': data['start_point']['lat'],
        'lng_s': data['start_point']['lng'],
        'lat_e': data['end_point']['lat'],
        'lng_e': data['end_point']['lng'],
        'data_delay': response_data['geometries']['blocks_scan'],
    }
    return templates.TemplateResponse(name="osrm.html", request=request, context=context)


@routeMap.post("/api/v1/route")
async def open_street_map(request: Request):
    data = await request.json()
    print(data)
    return get_route_osrm_grab(data)

@routeMap.post("/api/v2/route/waze")
async def waze_route(request: Request):
    data = await request.json()
    return get_route_waze(data)

@routeMap.post("/api/v1/route/multiplepoints")
async def multiple_points(request: Request):
    data = await request.json()
    return get_route_multiple_points_osrm_grab(data)

