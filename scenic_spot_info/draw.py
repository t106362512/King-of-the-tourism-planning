# # import gmplot package
# import gmplot

# # Set different latitude and longitude points
# Charminar_top_attraction_lats, Charminar_top_attraction_lons = zip(*[
#     (17.3833, 78.4011), (17.4239, 78.4738), (17.3713, 78.4804), (17.3616, 78.4747),
#     (17.3578, 78.4717), (17.3604, 78.4736), (17.2543, 78.6808), (17.4062, 78.4691),
#     (17.3950, 78.3968), (17.3587, 78.2988), (17.4156, 78.4750)])
# # declare the center of the map, and how much we want the map zoomed in
# gmap3 = gmplot.GoogleMapPlotter(17.3616, 78.4747, 13)
# # Scatter map
# gmap3.scatter(Charminar_top_attraction_lats,
#               Charminar_top_attraction_lons, '#FF0000', size=50, marker=False)
# # Plot method Draw a line in between given coordinates
# gmap3.plot(Charminar_top_attraction_lats,
#            Charminar_top_attraction_lons, 'cornflowerblue', edge_width=3.0)
# # Your Google_API_Key
# gmap3.apikey = 'AIzaSyCcnZRtkbHg4X80RTTQSz60a2SvqmBitp8'
# # save it to html
# gmap3.draw("map.html")


# import gmplot

# # Create the map plotter:
# apikey = 'AIzaSyCcnZRtkbHg4X80RTTQSz60a2SvqmBitp8' # (your API key here)
# gmap = gmplot.GoogleMapPlotter(37.766956, -122.448481, 14, apikey=apikey)

# # Outline the Golden Gate Park:
# golden_gate_park = zip(*[
#     (37.771269, -122.511015),
#     (37.773495, -122.464830),
#     (37.774797, -122.454538),
#     (37.771988, -122.454018),
#     (37.773646, -122.440979),
#     (37.772742, -122.440797),
#     (37.771096, -122.453889),
#     (37.768669, -122.453518),
#     (37.766227, -122.460213),
#     (37.764028, -122.510347)
# ])
# gmap.polygon(*golden_gate_park, color='cornflowerblue', edge_width=10)

# # Highlight some attractions:
# attractions_lats, attractions_lngs = zip(*[
#     (37.769901, -122.498331),
#     (37.768645, -122.475328),
#     (37.771478, -122.468677),
#     (37.769867, -122.466102),
#     (37.767187, -122.467496),
#     (37.770104, -122.470436)
# ])
# gmap.scatter(attractions_lats, attractions_lngs, color='#3B0B39', size=40, marker=False)

# # Mark a hidden gem:
# gmap.marker(37.770776, -122.461689, color='cornflowerblue')

# # Draw the map:
# gmap.draw('map.html')


# import gmplot package
import gmplot

# GoogleMapPlotter return Map object
# Pass the center latitude and
# center longitude
apikey = 'AIzaSyCcnZRtkbHg4X80RTTQSz60a2SvqmBitp8'

# 120.97969/23.973837 台灣中心
gmap = gmplot.GoogleMapPlotter(
    23.973837, 120.97969, 8, apikey=apikey)

latitude_list = [25.28247, 25.10815, 25.19156, 25.27472,
                 25.17181, 25.10372, 25.29054, 25.06498, 24.97271, 25.29261]
longitude_list = [121.60546, 121.84354, 121.52081, 121.55292,
                  121.43855, 121.42752, 121.54404, 121.50055, 121.44421, 121.53531]
# latitude_list = [25.06498, 24.97271, 25.10815]
# longitude_list = [121.50055, 121.44421, 121.84354]

# Id = C1_382000000A_110393, Name = 北海高爾夫球場, Local = [121.60546, 25.28247]
# Id = C1_382000000A_110315, Name = 翁山英故居(九份茶坊), Local = [121.84354, 25.10815]
# Id = C1_382000000A_110323, Name = 反經石, Local = [121.52081, 25.19156]
# Id = C1_382000000A_110380, Name = 聖明宮千年雀榕, Local = [121.55292, 25.27472]
# Id = C1_382000000A_110411, Name = 滬尾馬偕醫館, Local = [121.43855, 25.17181]
# Id = C1_382000000A_110319, Name = 旗竿湖教育農場, Local = [121.42752, 25.10372]
# Id = C1_382000000A_110379, Name = 小梅街道, Local = [121.54404, 25.29054]
# Id = C1_382000000A_110341, Name = 三和夜市, Local = [121.50055, 25.06498]
# Id = C1_382000000A_110360, Name = 土城廣承岩寺, Local = [121.44421, 24.97271]
# Id = C1_382000000A_110371, Name = 富基漁港, Local = [121.53531, 25.29261]


# scatter method of map object
# scatter points on the google map
gmap.scatter(latitude_list, longitude_list, '#FF0000',
             size=300, marker=True)

# 熱點
# heatmap plot heating Type
# points on the Google map
# gmap.heatmap(latitude_list, longitude_list)

# polygon method Draw a polygon with
# the help of coordinates
# 框出 點點點 區域
# gmap.polygon(latitude_list, longitude_list,
#              color='cornflowerblue')

# Plot method Draw a line in
# between given coordinates
gmap.plot(latitude_list, longitude_list,
          'cornflowerblue', edge_width=2.5)


# Pass the absolute path
gmap.draw("map.html")
