from fastapi import Request
from fastapi.responses import JSONResponse
from .v1.requests_route import RequestRoute
from models.models import Variable

async def get_route_osrm_grab(request: Request):
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

    # models_var = Variable()
    # condition = models_var.CONDITION
    # data = await request.json()
    
    # for name in condition:
    #     if name == "end_point":
    #         if not data.get(name):
    #             return JSONResponse(content=models_var.ROUTE429)
    #         condition[name] = data.get(name)
    #     elif data.get(name) is not None:
    #         condition[name] = data.get(name)

    # do = RequestRoute(str(condition['start_point']['lat']), str(condition['start_point']['lng']), str(condition['end_point']['lat']), str(condition['end_point']['lng']))
    # do.condition(route=condition['route'])  # osrm(default), graph
    # do.condition(scan=condition['scan'])  # true, false(default)
    # do.condition(weather=condition['weather'])  # true, false(default)

    # response = do.serve()
    # print("res: ",response)
    # return JSONResponse(content=response)

def get_route_osrm_grab2():
    models_var = Variable()
    condition = models_var.CONDITION
    # data = request.json()
    data = {'start_point': {'lat': 11.584637323468067, 'lng': 104.90419534099364}, 'endint': {'lat': 11.531581, 'lng': 104.827453}, 'scan': True, 'traffic': True}
    print(data)
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
    print("res: ",response)
    return JSONResponse(content=response)
