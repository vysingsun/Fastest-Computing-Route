from fastapi.responses import JSONResponse # type: ignore
from .v1.requests_route import RequestRoute
from .waze_service_data.waze_request_route_service import WazeRequestRoute
from models.models import Variable

def get_route_osrm_grab(data):
    models_var = Variable()
    condition = models_var.CONDITION
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
    
    return JSONResponse(response)

def get_route_waze(data):
    models_var = Variable()
    condition = models_var.CONDITION
    for name in condition:
        if name == "end_point":
            if not data.get(name):
                return JSONResponse(content=models_var.ROUTE429)
            condition[name] = data.get(name)
        elif data.get(name) is not None:
            condition[name] = data.get(name)
    dov2 = WazeRequestRoute(str(condition['start_point']['lat']),str(condition['start_point']['lng']),str(condition['end_point']['lat']),str(condition['end_point']['lng']))
    dov2.condition(route=condition['route'])
    dov2.condition(scan=condition['scan'])

    response = dov2.serve()

    return JSONResponse(content=response)

def get_route_osrm_grab2(data):
    models_var = Variable()
    condition = models_var.CONDITION
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

def get_route_multiple_points_osrm_grab(data):
    models_var = Variable()
    condition = models_var.CONDITION
    for name in condition:
        if name == "end_point":
            if not data.get(name):
                return JSONResponse(content=models_var.ROUTE429)
            condition[name] = data.get(name)
        elif data.get(name) is not None:
            condition[name] = data.get(name)

    do = RequestRoute(str(condition['start_point']['lat']),str(condition['start_point']['lng']),str(condition['end_point']['lat']),str(condition['end_point']['lng']))
    do.condition(route=condition['route'])# osrm(default)
    do.condition(scan=condition['scan'])# true , false(default)"
    do.condition(weather=condition['weather'])# true , false(default)
    return JSONResponse(do.serve_of_multiple_points())

