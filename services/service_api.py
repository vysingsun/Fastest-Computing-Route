from fastapi import Request
from fastapi.responses import JSONResponse
from .v1.requests_route import RequestRoute
from models.models import Variable

async def get_route_osrm_grab(request: Request):
    models_var = Variable()
    condition = models_var.CONDITION
    data = await request.json()
    
    for name in condition:
        if name == "end_point":
            if not data.get(name):
                return JSONResponse(content=models_var.ROUTE429)
            condition[name] = data.get(name)
        elif data.get(name) is not None:
            condition[name] = data.get(name)

    do = RequestRoute(str(condition['start_point']['lat']), str(condition['start_point']['lng']), str(condition['end_point']['lat']), str(condition['end_point']['lng']))
    do.condition(route=condition['route'])  # osrm(default), graph
    do.condition(scan=condition['scan'])  # true, false(default)
    do.condition(weather=condition['weather'])  # true, false(default)

    response = do.serve()
    return JSONResponse(content=response)
