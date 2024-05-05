from typing import Union

from fastapi import FastAPI # type: ignore

from routes.urls import routeMap

app = FastAPI()

app.include_router(routeMap)

# from fastapi import FastAPI , Query
# from fastapi.responses import HTMLResponse
# import folium
# from folium.plugins import LocateControl, MiniMap
# import networkx as nx

# app = FastAPI()

# @app.get("/map")
# async def display_map():
#     latitude = 11.5730084
#     longitude = 104.9073121
    
#     # Create the map using Folium
#     map = folium.Map(location=[latitude, longitude], zoom_start=15)

#     map.add_child(folium.Marker([latitude, longitude], popup="Marker"))

#     map_html = map.get_root().render()

#     return HTMLResponse(content=map_html)

# @app.get("/current")
# async def display_map(latitude: float = Query(..., description="Latitude"),
#                       longitude: float = Query(..., description="Longitude")):
#     # Create the map using Folium
#     map = folium.Map(location=[latitude, longitude], zoom_start=15)

#     map.add_child(folium.Marker([latitude, longitude], popup="Marker"))

#     map_html = map.get_root().render()

#     return HTMLResponse(content=map_html)

# @app.get("/two_marker")
# async def display_map():

#     latitude = 11.5730084
#     longitude = 104.9073121
#     map = folium.Map(location=[latitude, longitude], zoom_start=15)

#     map.add_child(folium.Marker([latitude, longitude], popup="Marker 1"))
    
#     marker_latitude = 11.5774458
#     marker_longitude = 104.9038455
#     map.add_child(folium.Marker([marker_latitude, marker_longitude], popup="Marker 2"))

#     map_html = map.get_root().render()

#     return HTMLResponse(content=map_html)

# @app.get("/")
# async def display_map():
   
#     latitude = 11.5374458
#     longitude = 104.9538455

#     zoom_level = 15

#     map = folium.Map(location=[latitude, longitude], zoom_start=zoom_level)

#     map.add_child(folium.Marker([latitude, longitude], popup="Marker 1"))

#     map_html = map.get_root().render()

#     return HTMLResponse(content=map_html)

