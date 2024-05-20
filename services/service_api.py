from urllib import request
from fastapi import Response, Request
from fastapi.responses import JSONResponse # type: ignore
from .v1.requests_route import RequestRoute
from models.models import Variable

def get_route_osrm_grab(data):
    models_var = Variable()
    condition = models_var.CONDITION
    print("This: ", condition)
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
    print("RES: ", response)
    
    return JSONResponse(response)


def get_route_osrm_grab2():
    models_var = Variable()
    condition = models_var.CONDITION
    data = {'start_point': {'lat': 11.584637323468067, 'lng': 104.90419534099364}, 'endint': {'lat': 11.531581, 'lng': 104.827453}, 'scan': True, 'traffic': True}
    for name in condition:
        if name == "end_point":
            if not data.get(name):
                return JSONResponse(content=models_var.ROUTE429)
            condition[name] = data.get(name)
        elif data.get(name) is not None:
            condition[name] = data.get(name)
    print("My data: ", data)
    do = RequestRoute(str(condition['start_point']['lat']), str(condition['start_point']['lng']), str(condition['end_point']['lat']), str(condition['end_point']['lng']))
    do.condition(route=condition['route'])  # osrm(default), graph
    do.condition(scan=condition['scan'])  # true, false(default)
    do.condition(weather=condition['weather'])  # true, false(default)

    response = do.serve()

    return JSONResponse(content=response)

