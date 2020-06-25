# import folium package
import folium

# Map method of folium return Map object

# Here we pass coordinates of Gfg
# and starting Zoom level = 12
fmap = folium.Map(location=[25.06498, 121.50055],
                  zoom_start=12)

fmap.add_child(folium.Marker(location=[25.06498, 121.50055],
                             popup='Skytree'))

# save method of Map object will create a map
fmap.save("folium.html")
