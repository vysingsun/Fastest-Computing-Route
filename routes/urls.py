from fastapi import APIRouter
from services.service_api import get_route_osrm_grab
from services.views import CurrentView

routeMap = APIRouter()

# @routeMap.get("/")
# async def index():
#     return await CurrentView.index()

# @routeMap.get("/google_map")
# async def google_map():
#     return await views.CurrentView.google_map()

@routeMap.get("/open_street_map")
async def open_street_map():
    return await CurrentView.open_street_map()

@routeMap.get("/api/v1/route")
async def open_street_map(request):
    return await get_route_osrm_grab(request)

# routeMap.include_router(
#     get_route_osrm_grab,
#     prefix="/api/v1",
#     tags=["Route"],
# )

