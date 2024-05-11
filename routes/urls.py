from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from models.models import Variable
from services.v1.requests_route import RequestRoute
from services.service_api import get_route_osrm_grab, get_route_osrm_grab2
from services.views import CurrentView

routeMap = APIRouter()

# @routeMap.get("/")
# async def index():
#     return await CurrentView.index()

# @routeMap.get("/google_map")
# async def google_map():
#     return await views.CurrentView.google_map()

# @routeMap.get("/open_street_map")
# async def open_street_map():
#     return await CurrentView.open_street_map()

@routeMap.get('/')
def gets():
    request = {'start_point': {'lat': 11.584637323468067, 'lng': 104.90419534099364}, 'endint': {'lat': 11.531581, 'lng': 104.827453}, 'scan': True, 'traffic': True}
    print(request)
    return get_route_osrm_grab2()

# @routeMap.get('/')
# def gets():
#     return getslog()

@routeMap.get("/api/v1/route")
async def open_street_map(request):
    # return await get_route_osrm_grab(request)

    try:
        data = await request.json()
    except ValueError:
        return JSONResponse(content={"error": "Invalid JSON format in request body"}, status_code=400)

    models_var = Variable()
    condition = models_var.CONDITION

    for name in condition:
        if name in data:
            condition[name] = data[name]

    if not condition['end_point']:
        return JSONResponse(content=models_var.ROUTE429)

    try:
        start_lat = str(condition['start_point']['lat'])
        start_lng = str(condition['start_point']['lng'])
        end_lat = str(condition['end_point']['lat'])
        end_lng = str(condition['end_point']['lng'])
    except KeyError:
        return JSONResponse(content={"error": "Required fields 'start_point' or 'end_point' are missing"}, status_code=400)

    do = RequestRoute(start_lat, start_lng, end_lat, end_lng)
    do.condition(route=condition.get('route', 'osrm'), scan=condition.get('scan', False), weather=condition.get('weather', False))

    try:
        response = do.serve()
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content=response)

# routeMap.include_router(
#     get_route_osrm_grab,
#     prefix="/api/v1",
#     tags=["Route"],
# )

