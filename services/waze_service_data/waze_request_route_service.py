from .waze_route_service import WazeRoute
from models.models import Variable
from services.v1.scan_driver import ScanDriver
from services.v1.insert_driver import InsertDriver

duration = 0
class WazeRequestRoute: 
    route = None
    block_scan_data = []
    api_scan_driver = None
    api_route = None
    models = Variable()
    conditions = models.CONDITION
    full_route = models.ROUTE
    
    def __init__(self, s_lat, s_lng, e_lat, e_lng):
        self.models.setStartLatLng(s_lat, s_lng)
        self.models.setEndLatLng(e_lat, e_lng)

    def serve(self):
        route = WazeRoute(self.conditions["start_point"]["lat"],self.conditions["start_point"]["lng"],self.conditions["end_point"]["lat"],self.conditions["end_point"]["lng"])
        self.full_route["start_point"] = eval('[{},{}]'.format(self.conditions["start_point"]["lat"], self.conditions["start_point"]["lng"]))
        self.full_route["end_point"] = eval('[{},{}]'.format(self.conditions["end_point"]["lat"], self.conditions["end_point"]["lng"]))
        for name in self.conditions:
            while name == "weather":
                if not self.conditions[name] is None:
                    self.full_route["geometries"]["weather"] = self.conditions[name]
                break
        self.full_route["geometries"]["distance"] = route.get_distance()
        self.full_route["geometries"]["route"] = route.get_route()
        self.full_route["geometries"]["options"] = route.get_option()
        self.full_route["geometries"]["duration"] = route.get_duration()
        self.full_route["geometries"]["blocks_scan"] = []
        self.full_route["code"] = route.code
        return self.full_route


    def condition(self, **kwargs):
        edit = kwargs
        for name in edit:
            if edit[name] is not None:
                self.conditions[name] = edit[name]
    
    def scan_route(self):
        global duration
        scan = ScanDriver()
        insert = InsertDriver()
        drivers = insert.fake()
        get = scan.scan_driver(self.api_route,drivers)
        duration = get[0]
        self.block_scan_data = get[1]
        return self.block_scan_data