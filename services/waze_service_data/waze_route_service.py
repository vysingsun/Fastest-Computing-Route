import requests
from config.settings import Settings
from models.models import Variable
import threading
class WazeRoute:
    
    routes = []
    start_route = 0

    settings = Settings()
    coordinates = None
    steps = None
    options = []
    # value
    distance = 0
    old_time = 0
    #setting
    models = Variable()
    conditions = models.CONDITION
    full_route = models.ROUTE
    VERSION_WAZE = settings.VERSION_WAZE
    def __init__(self,s_lat, s_lng, e_lat, e_lng):
        self.set_request(s_lat, s_lng, e_lat, e_lng)

    def set_request(self,s_lat, s_lng, e_lat, e_lng):
        # get data not have traffic include
        hosts = self.models.getWazData(s_lat, s_lng, e_lat, e_lng)
        if hosts == {"error": "Internal Error"}:
            self.full_route = {"code":400,"error":"Waze can not handle"}
            self.duration = 0
            self.options = []
            self.distance = 0
            self.code = 419
        else:
            self.code = 200
            self.duration = hosts['response']['totalRouteTime']
            coord = hosts['coords']
            response = hosts['response']['results']
            street = hosts['response']['streetNames']
            route = []
            for latlng in coord:
                coor = eval('['+'{},{}'.format(latlng['y'], latlng['x'])+']')
                route.append(coor)
            dis = 0
            for path in response:
                distance = path['distance']
                old = distance-dis
                dis = dis + old
                while not path['instruction'] is None:
                    direction = path['instruction']['opcode']
                    roadType = path['street']
                    streetNames = street[roadType]
                    self.options.append(eval("{" + '"point":[{},{}],"distance":{},"direction":"{}","streetName":"{}"'.format( path['path']['y'], path['path']['x'], distance, direction, streetNames) + '}'))
                    break
            self.distance = dis
            self.full_route = route

    def condition(self,**kwargs):
        edit = kwargs
        # for name in edit:
        for name in edit:
            while not edit[name] is None:
                self.conditions[name]=edit[name]
                break
        print("me",self.conditions)

    def get_route(self):
        return self.full_route

    def get_option(self):
        return self.options

    def get_distance(self):
        return self.distance

    def get_duration(self):
        return self.duration
    
    def serve_of_multiple_points(self):
        route = None
        for name in self.conditions:
            if name == "route":
                if self.conditions[name] == "osrm":
                    route = self.dynamic_route_of_multiple_points("osrm")
                break

        if route is not None:
            self.full_route = route

        return self.full_route

    def dynamic_route_of_multiple_points(self, types=None):
        if types is None or types == "osrm" or types != "graph":
            # Fixed starting point
            start_point = self.conditions["points"][0]
            other_points = self.conditions["points"][1:]

            return self.get_short_dis_and_route(start_point, other_points)

    def get_short_dis_and_route(self, start, points):
        points = [i for i in points if i != start]
        short_point = []
        shortest_distance = float('inf')

        self.conditions["start_point"] = {
            "lat": start[0],
            "lng": start[1],
        }

        # Add threading
        threads = []
        results = []
        results_lock = threading.Lock()

        def worker(data, index):
            try:
                s_lat = self.conditions["start_point"]["lat"]
                s_lng = self.conditions["start_point"]["lng"]
                e_lat = data[0]
                e_lng = data[1]
                hosts = self.models.getWazData(s_lat, s_lng, e_lat, e_lng)
                if hosts != {"error": "Internal Error"}:
                    distance = hosts['response']['totalRouteTime']
                    coords = [[latlng['y'], latlng['x']] for latlng in hosts['coords']]
                    with results_lock:
                        results.append((distance, data, index, coords))
            except Exception as e:
                print(f"Error in worker thread: {e}")

        
        for i, data in enumerate(points):
            thread = threading.Thread(target=worker, args=(data, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Sort results by distance
        results.sort(key=lambda x: x[0])

        for distance, data, index, coords in results:
            if distance < shortest_distance:
                shortest_distance = distance
                short_point = data

                self.conditions["start_point"] = {
                    "lat": data[0],
                    "lng": data[1],
                }
                if self.routes != self.coordinates:
                    self.routes = self.routes + coords

        if len(points) > 0:
            self.get_short_dis_and_route(short_point, points)

        return self.routes