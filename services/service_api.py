from urllib import request
from fastapi import Response, Request
from fastapi.responses import JSONResponse # type: ignore
from .v1.requests_route import RequestRoute
from .waze_service_data.waze_request_route_service import WazeRequestRoute
from .waze_service_data.waze_route_service import WazeRoute
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
    
    # Ensure that 'points' is provided and has at least two points
    if 'points' not in data or len(data['points']) < 2:
        return JSONResponse(content={"error": "At least two points are required"})
    
    start_point = data['points'][0]
    end_point = data['points'][-1]
    condition['points'] = data['points']
    
    for name in condition:
        if data.get(name) is not None:
            condition[name] = data.get(name)

    do = RequestRoute(str(start_point[0]), str(start_point[1]), str(end_point[0]), str(end_point[1]))
    do.condition(route=condition['route'])  # osrm(default)
    do.condition(scan=condition['scan'])  # true, false(default)
    do.condition(weather=condition['weather'])  # true, false(default)
    do.condition(points=condition['points'])
    
    return JSONResponse(do.serve_of_multiple_points())

def get_route_waze_for_multiple_point(data):
    models_var = Variable()
    condition = models_var.CONDITION
     # Ensure that 'points' is provided and has at least two points
    if 'points' not in data or len(data['points']) < 2:
        return JSONResponse(content={"error": "At least two points are required"})
    
    start_point = data['points'][0]
    end_point = data['points'][-1]

    condition['points'] = data['points']
    for name in condition:
        if data.get(name) is not None:
            condition[name] = data.get(name)
            
    dov2 = WazeRoute(str(start_point[0]), str(start_point[1]), str(end_point[0]), str(end_point[1]))
    dov2.condition(route=condition['route'])
    dov2.condition(scan=condition['scan'])
    dov2.condition(points=condition['points'])

    response = dov2.serve_of_multiple_points()

    return JSONResponse(content=response)

