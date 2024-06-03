# from fastapi import FastAPI, BackgroundTasks, Request
# from fastapi.responses import HTMLResponse, JSONResponse
# import requests
# from time import strftime, gmtime

# class CurrentView:
#     @staticmethod
#     def get_route_data():
#         # Define your logic for fetching route data
#         data = {
#             "start_point": {"lat": 11.584637323468067, "lng": 104.90419534099364},
#             "end_point": {"lat": 11.531581, "lng": 104.827453},
#             "scan": True,
#             "traffic": True,
#         }
#         response = requests.get("http://localhost:8000/api/v1/route", json=data).json()
#         return response
    
#     async def index(request: Request):
#         response = requests.get('http://api.ipstack.com/103.216.51.117?access_key=c3ae01b20017a4dc59fa423101f5fe05')
#         geodata = response.json()
#         context = {
#             'ip': geodata['ip'],
#             'country': geodata['country_name'],
#             'latitude': geodata.get('latitude', ''),
#             'longitude': geodata.get('longitude', ''),
#         }
#         return HTMLResponse(content=render_template("fastroute/home.html", context=context), status_code=200)

#     # use but not work with lat long
#     async def google_map():
#         response = CurrentView.get_route_data()
#         gcoor = [{'lat': point[0], 'lng': point[1]} for point in response['geometries']['route']]
#         context = {
#             'model': "Bike",
#             'distance': response['geometries']['distance'] / 1000,
#             'duration': strftime("%Hh:%Mm:%Ss", gmtime(response['geometries']['duration'])),
#             'map': gcoor,
#             'lat_s': response['start_point']['lat'],
#             'lng_s': response['start_point']['lng'],
#             'lat_e': response['end_point']['lat'],
#             'lng_e': response['end_point']['lng'],
#             'data_delay': response['geometries']['blocks_scan'],
#         }
#         return render_template("fastroute/success_drawing.html", context=context)
    
#     async def open_street_map():
#         response = CurrentView.get_route_data()
#         context = {
#             'model': "Bike",
#             'distance': response['geometries']['distance'] / 1000,
#             'duration': strftime("%Hh:%Mm:%Ss", gmtime(response['geometries']['duration'])),
#             'map': response['geometries']['route'],
#             'lat_s': response['start_point']['lat'],
#             'lng_s': response['start_point']['lng'],
#             'lat_e': response['end_point']['lat'],
#             'lng_e': response['end_point']['lng'],
#             'data_delay': response['geometries']['blocks_scan'],
#         }
#         return render_template("fastroute/map.html", context=context)
