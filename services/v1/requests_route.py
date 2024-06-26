from fastapi import APIRouter, HTTPException
from .scan_driver import ScanDriver
from .insert_driver import InsertDriver
from models.models import Variable
import threading
import requests

URLOSRM = "https://routing.openstreetmap.de/routed-car/route/v1/driving/{lng_start_point},{lat_start_point};{lng_end_point},{lat_end_point}?overview=full&geometries=geojson&steps=true&generate_hints=false"

duration = 0

class RequestRoute:
    route = None
    block_scan_data = []
    coordinates = None
    insert_times = None
    steps = None
    api_scan_driver = None
    api_route = None
    distance = 0
    old_time = 0
    options = None
    models = Variable()
    conditions = models.CONDITION
    full_route = models.ROUTE
    
    routes = []
    start_route = 0
    
    points = [
        (11.584637323468067, 104.90419534099364),  # start_point
        (11.567172, 104.900340),  # nd_point
        (11.583854, 104.909404), # rd_point
        (11.553859, 104.895052),   # th_point
        (11.579015, 104.917060)
    ]

    def __init__(self, s_lat, s_lng, e_lat, e_lng):
        self.models.setStartLatLng(s_lat, s_lng)
        self.models.setEndLatLng(e_lat, e_lng)

    def serve(self):
        for name in self.conditions:
            if name == "route":
                if self.conditions[name] == "osrm":
                    self.dynamic_route("osrm")
                else:
                    self.dynamic_route("graph")
                self.full_route["geometries"]["duration"] = duration  
            elif name == "scan":
                if self.conditions[name]:
                    self.scan_route()
                    self.full_route["geometries"]["duration"] = duration
                    self.full_route["geometries"]["blocks_scan"] = self.block_scan_data
                else:
                    self.full_route["geometries"]["blocks_scan"] = []
        
        self.full_route["geometries"]["distance"] = self.distance  
        self.full_route["geometries"]["route"] = self.route  
        self.full_route["geometries"]["options"] = self.options  
        self.full_route["start_point"] = [self.route[0][0], self.route[0][1]]
        self.full_route["end_point"] = [self.route[-1][0], self.route[-1][1]]
        # print("Full_route: ", self.full_route)
        return self.full_route

    def condition(self, **kwargs):
        edit = kwargs
        for name in edit:
            if edit[name] is not None:
                self.conditions[name] = edit[name]

    def dynamic_route(self, types):
        global duration
        if types is None or types == "osrm" or types != "graph":
            url = URLOSRM.format(lng_start_point=self.conditions["start_point"]["lng"], lat_start_point=self.conditions["start_point"]["lat"], lng_end_point=self.conditions["end_point"]["lng"], lat_end_point=self.conditions["end_point"]["lat"])
            osrm_bike = requests.get(url)
            osrm_bike = osrm_bike.json()
            duration = osrm_bike['routes'][0]['duration']
            self.distance = osrm_bike['routes'][0]['distance']
            self.old_time = osrm_bike['routes'][0]['duration']
            self.json_data = osrm_bike
            self.steps = osrm_bike['routes']
            self.coordinates = osrm_bike['routes'][0]['geometry']['coordinates']
           
            self.options_osrm()
        elif types == "graph":
            key = settings.KEY_GRAPH
            rand_key = random.choice(key)
            graph_bike = requests.get(
                'https://graphhopper.com/api/1//route?point={}%2C{}&point={}%2C{}&type=json&locale=en-US&vehicle=car&weighting=fastest&elevation=true&key={}&points_encoded=false'.format(
                    self.conditions["start_point"]["lat"], self.conditions["start_point"]["lng"], self.conditions["end_point"]["lat"], self.conditions["end_point"]["lng"], rand_key)).json()
            duration = graph_bike['paths'][0]['time']
            self.json_data = graph_bike
            self.distance = graph_bike['paths'][0]['distance']
            self.old_time = graph_bike['paths'][0]['time']
            self.steps = graph_bike['paths']
            self.coordinates = graph_bike['paths'][0]['points']['coordinates']
            self.options_graph()

        # print(['dynamic_route',self.conditions,osrm_bike])
        
        if not self.coordinates is None:
            return self.get_single_map()
        else:
            return self.dynamic_route(types)

    def scan_route(self):
        global duration
        scan = ScanDriver()
        insert = InsertDriver()
        drivers = insert.fake()
        get = scan.scan_driver(self.api_route, drivers)
        duration = get[0]
        self.block_scan_data = get[1]
        return self.block_scan_data

    def get_single_map(self):
        final_route = []
        coordinate_route = []
        lat = None
        lng = None
        for coordinate in self.coordinates:
            lng = coordinate[0]
            lat = coordinate[1]
            coordinate_route.append([lat, lng])
        final_route.append({"point1": [self.coordinates[0][1], self.coordinates[0][0]], "point2": [lat, lng], "route": coordinate_route, "duration": duration, "distance": self.distance})
        self.api_route = final_route[0]
        self.route = coordinate_route
        return self.route

    def get_multi_map(self):
        index_route = []
        final_route = []
        route = self.coordinates
        for i in range(0, len(self.steps)):
            road = []
            for co in route:
                coor = [co[1], co[0]]
                road.append(coor)
            index_route.append({"route": road, "duration": duration, "distance": self.distance})
        self.co_route = {"point1": [self.coordinates[0][1], self.coordinates[0][0]], "point2": [self.coordinates[len(self.coordinates) - 1][1], self.coordinates[len(self.coordinates) - 1][0]], "route": index_route}
        return self.co_route

    def options_osrm(self):
        options = []
        step = self.json_data['routes'][0]['legs'][0]['steps']
        for steps in step:
            point = [steps['maneuver']['location'][1], steps['maneuver']['location'][0]]
            distance = steps['distance']
            streetName = steps.get('name', "None")
            if "modifier" in steps['maneuver']:
                direction = "TURN_" + steps['maneuver']['modifier'].upper()
            else:
                direction = "NONE"
            options.append({"point": point, "distance": distance, "direction": direction, "streetName": streetName})
        self.options = options
        return self.options

    def options_graph(self):
        options = []
        step = self.json_data['paths'][0]['instructions']
        for instructions in step:
            distance = instructions['distance']
            direction = instructions['text']
            streetName = instructions['street_name']
            if not streetName:
                streetName = "None"
            options.append({"point": None, "distance": distance, "direction": direction, "streetName": streetName})
        self.options = options
        return self.options
    
    def serve_of_multiple_points(self):
        print("Use test!!")
        for name in self.conditions:     
            while name == "route":
                if self.conditions[name] == "osrm":
                    route = self.dynamic_route_of_multiple_points("osrm")
                break
            while name == "scan":
                if self.conditions[name] == True:
                    self.scan_route()
                    self.full_route["geometries"]["blocks_scan"] = self.block_scan_data
                else:
                    self.full_route["geometries"]["blocks_scan"] = []
                break
        re_route = [[i[1],i[0]] for i in route]
        self.full_route["geometries"]["route"] = re_route
        return self.full_route
    
    def dynamic_route_of_multiple_points(self, types=None):
        # print("CALL multi")
        if types is None or types == "osrm" or types != "graph":
            # Fixed starting point
            start_point = self.points[0]
            other_points = self.points[1:]
            
            return self.get_short_dis_and_route(start_point, other_points)
        
    def get_short_dis_and_route(self, start, points):

        points = [i for i in points if i != start]
        short_point = []
        shortest_distance = float('inf')

        self.conditions["start_point"] = {
            "lat": start[0],
            "lng": start[1],
        }
        
        #Add threading
        
        threads = []
        results = []
        results_lock = threading.Lock()
        
        def worker(data, index):
            self.conditions["end_point"] = {
                "lat": data[0],
                "lng": data[1],
            }
            self.dynamic_route(types='osrm')
            with results_lock:
                results.append((self.distance, data, index, self.coordinates))
        for i, data in enumerate(points):
            thread = threading.Thread(target=worker, args=(data, i))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

        # Test Sort results by distance
        results.sort(key=lambda x: x[0])
        
        for distance, data, index, coords in results:
            print("==>: ",distance, index)
            if distance < shortest_distance:
                shortest_distance = distance
                short_point = data
                
                self.conditions["start_point"] = {
                    "lat": data[0],
                    "lng": data[1],
                }
                if self.routes != self.coordinates:
                    self.routes = self.routes+coords
      
        if len(points) > 0 :
            self.get_short_dis_and_route(short_point, points)
        return self.routes

