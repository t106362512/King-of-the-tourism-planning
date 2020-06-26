from flask import Blueprint, render_template, g, session
import pydeck as pdk
import os

demo = Blueprint('demo', __name__, template_folder='templates',
                    static_folder='static')

# @demo.url_value_preprocessor
# def get_profile_owner(endpoint, values):
#     query = User.query.filter_by(url_slug=values.pop('user_url_slug'))
#     g.profile_owner = query.first_or_404()

@demo.route('/')
def map():
    UK_ACCIDENTS_DATA = ('https://raw.githubusercontent.com/uber-common/'
                     'deck.gl-data/master/examples/3d-heatmap/heatmap-data.csv')

# Define a layer to display on a map
    layer = pdk.Layer(
        'HexagonLayer',
        UK_ACCIDENTS_DATA,
        get_position=['lng', 'lat'],
        auto_highlight=True,
        elevation_scale=50,
        pickable=True,
        elevation_range=[0, 3000],
        extruded=True,                 
        coverage=1)

    # Set the viewport location
    view_state = pdk.ViewState(
        longitude=-1.415,
        latitude=52.2323,
        # longitude=121.297187,
        # latitude=24.943325,
        zoom=6,
        min_zoom=5,
        max_zoom=15,
        pitch=40.5,
        bearing=-27.36)

    r = pdk.Deck(layers=[layer], initial_view_state=view_state, mapbox_key=os.getenv('MAPBOX_API_KEY'))
    deck_map = r.to_json()
    return render_template('demo.html', deck_json=deck_map)

@demo.route('/scenice')
def scenice():
    DATA_URL = ('https://raw.githubusercontent.com/visgl/deck.gl-data/master/examples/geojson/vancouver-blocks.json')
    LAND_COVER = [[[-123.0, 49.196], [-123.0, 49.324], [-123.306, 49.324], [-123.306, 49.196]]]
    INITIAL_VIEW_STATE = pdk.ViewState(
    latitude=49.254,
    longitude=-123.13,
    zoom=11,
    max_zoom=16,
    pitch=45,
    bearing=0
    )

    polygon = pdk.Layer(
        'PolygonLayer',
        LAND_COVER,
        stroked=False,
        # processes the data as a flat longitude-latitude pair
        get_polygon='-',
        get_fill_color=[0, 0, 0, 20]
    )

    geojson = pdk.Layer(
        'GeoJsonLayer',
        DATA_URL,
        opacity=0.8,
        stroked=False,
        filled=True,
        extruded=True,
        wireframe=True,
        get_elevation='properties.valuePerSqm / 20',
        get_fill_color='[255, 255, properties.growth * 255]',
        get_line_color=[255, 255, 255],
        pickable=True
    )

    r = pdk.Deck(
        layers=[polygon, geojson],
        initial_view_state=INITIAL_VIEW_STATE, mapbox_key=os.getenv('MAPBOX_API_KEY'))
    deck_map = r.to_json()
    return render_template('demo.html', deck_json=deck_map)