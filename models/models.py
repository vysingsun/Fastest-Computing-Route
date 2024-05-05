from pydantic import BaseModel
import requests

class RouteTest(BaseModel):
    start: str
    end: str

class Variable:
    CONDITION = None
    ROUTE = None
    ROUTE429 = {
        "code": 429,
        "start_point": [],
        "end_point": [],
        "geometries": {
            "route": []
        },
    }

    def __init__(self):
        self.CONDITION = {
            "start_point": {
                "lat": 0,
                "lng": 0
            },
            "end_point": {
                "lat": 0,
                "lng": 0
            },
            "route": "osrm",
            "weather": "normal",
            "scan": "false",
            "traffic": "false"
        }

        self.ROUTE = {
            "code": 200,
            "start_point": [],
            "end_point": [],
            "geometries": {
                "route": [],
                "options": [],
                "blocks_scan": [],
                "duration": 0,
                "distance": 0,
                "weather": "normal"
            },
        }

    def setStartLatLng(self, lat, lng):
        self.CONDITION['start_point']['lat'] = lat
        self.CONDITION['start_point']['lng'] = lng

    def setEndLatLng(self, lat, lng):
        self.CONDITION['end_point']['lat'] = lat
        self.CONDITION['end_point']['lng'] = lng

    def getWazData(self, s_lat, s_lng, e_lat, e_lng):
        start_point = "x%3A{}%20y%3A{}".format(s_lng, s_lat)
        end_point = "x%3A{}%20y%3A{}".format(e_lng, e_lat)
        URLROUTE = f"https://www.waze.com/row-RoutingManager/routingRequest?at=0&clientVersion={settings.VERSION_WAZE}&from={start_point}&nPaths=1&options=AVOID_TRAILS%3At%2CALLOW_UTURNS%3At&returnGeometries=true&returnInstructions=true&returnJSON=true&timeout=60000&to={end_point}"
        URLTRAFFIC = f"https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={s_lng}&left={s_lat}&ma=200&mj=100&mu=20&right={e_lng}&top={e_lat}types=alerts%2Ctraffic%2Cusers"
        HEADER = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "referer": f"https://www.waze.com/livemap/directions?q=66%20Acacia%20Avenue&navigate=yes&latlng={s_lng}%2C-{s_lat}",
        }
        return requests.get(URLROUTE, headers=HEADER).json()

    def getTraffic(self):
        return requests.get(self.URLTRAFFIC, headers=self.HEADER).json()
