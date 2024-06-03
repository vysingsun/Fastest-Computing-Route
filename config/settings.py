from typing import ClassVar, Dict, List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    CONDITION: ClassVar[Dict[str, Dict[str, int or str]]] = {
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
        "scan": "false"
    }

    ROUTE: ClassVar[Dict[str, int or List or Dict[str, int or str]]] = {
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
        }
    }

    SET_NUM_DRIVER_TO_SCAN: int = 6
    SET_NUM_DRIVER_TO_GET_MAX_SPEED: int = 3
    DEFAULT_SPEED: int = 60
    KEY_GRAPH: list[str] = [
        "0dc4f299-a491-452f-97e0-515c296c9453",
        "LijBPDQGfu7Iiq80w3HzwB4RUDJbMbhs6BU0dEnn",
        "a948c182-388d-48eb-889f-01131bbce681",
        "8fcdb3be-5de1-46db-b97f-a76370ca35b8",
        "a3d9f382-aa47-49b2-bcc2-fda39e4c1dcc"
    ]

    VERSION_WAZE: str = "4.0.0"

    start_point: str = "x%3A{}%20y%3A{}".format(CONDITION["start_point"]["lng"], CONDITION["start_point"]["lat"])
    end_point: str = "x%3A{}%20y%3A{}".format(CONDITION["end_point"]["lng"], CONDITION["end_point"]["lat"])
    URLROUTE: str = "https://www.waze.com/row-RoutingManager/routingRequest?at=0&clientVersion={}&from={}&nPaths=3&options=AVOID_TRAILS%3At%2CALLOW_UTURNS%3At&returnGeometries=true&returnInstructions=true&returnJSON=true&timeout=60000&to={}".format(VERSION_WAZE, start_point, end_point)
    URLTRAFFIC: str = "https://www.waze.com/row-rtserver/web/TGeoRSS?bottom={}&left={}&ma=200&mj=100&mu=20&right={}&top={}types=alerts%2Ctraffic%2Cusers".format(CONDITION["start_point"]["lng"], CONDITION["start_point"]["lat"], CONDITION["end_point"]["lng"], CONDITION["end_point"]["lng"])
    HEADER: Dict[str, str] = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
        "referer": "https://www.waze.com/livemap/directions?q=66%20Acacia%20Avenue&navigate=yes&latlng={}%2C-{}".format(CONDITION["start_point"]["lng"], CONDITION["start_point"]["lat"])
    }

    class Config:
        env_file = ".env"
