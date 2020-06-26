# from GraphModel import Graph, GraphAlgorithm
from TravelGraph import TSP
from pathlib import Path
from pprint import pprint
import json

if __name__ == "__main__":
    
    RAW_DATA_FILE = Path(__file__).parent.joinpath('test.json')
    RAW_DATA = json.loads(RAW_DATA_FILE.read_text())

    r = TSP().from_gmaps_matrix(RAW_DATA).normal_ans()
    pprint(r)
