# import gmplot package
import gmplot

# GoogleMapPlotter return Map object
# Pass the center latitude and
# center longitude
apikey = 'AIzaSyCcnZRtkbHg4X80RTTQSz60a2SvqmBitp8'

# 120.97969/23.973837 台灣中心
gmap = gmplot.GoogleMapPlotter(
    23.973837, 120.97969, 8, apikey=apikey)

result_list = [
    [121.60546, 25.28247],
    [121.55292, 25.27472],
    [121.54404, 25.29054],
    [121.53531, 25.29261],
    [121.52081, 25.19156],
    [121.43855, 25.17181],
    [121.42752, 25.10372],
    [121.44421, 24.97271],
    [121.50055, 25.06498],
    [121.84354, 25.10815]
  ]

result_list_g = list(map(lambda x: (x[1],x[0]), result_list))

latitude_list, longitude_list = zip(*result_list_g)

# scatter method of map object
# scatter points on the google map
gmap.scatter(latitude_list, longitude_list, '#FF0000',
             size=300, marker=True)

gmap.plot(latitude_list, longitude_list,
          'cornflowerblue', edge_width=2.5)

# Pass the absolute path
gmap.draw("map.html")
