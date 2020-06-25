from collections import defaultdict, OrderedDict
from operator import itemgetter
from pathlib import Path
from pprint import pprint
import json

RAW_DATA_FILE = Path(__file__).parent.joinpath('test.json')
RAW_DATA = json.loads(RAW_DATA_FILE.read_text())

if __name__ == "__main__":
    if RAW_DATA['status'] == 'OK':
        origin_addresses = RAW_DATA['origin_addresses']
        destination_addresses = RAW_DATA['destination_addresses']
        rows = RAW_DATA['rows']
        # ddict = defaultdict(lambda x:0)
        ddict = OrderedDict()
        for row_ind, row in enumerate(rows):
            for el_ind, element in enumerate(row['elements']):
                distance = element['distance']['value']
                ddict[(origin_addresses[row_ind], destination_addresses[el_ind])] = distance
        # fd = {k: v for k,v in sorted(ddict.items(), key=itemgetter(1)) if v != 0}
        fd = OrderedDict(sorted(ddict.items(),key=itemgetter(1)))
        pprint(fd)

