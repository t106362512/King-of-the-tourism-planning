from pprint import pprint
import requests
import json
import os

if __name__ == "__main__":
    list1 = [['1','2'], ['3','4']]
    l2 = map((lambda x: [x[1],x[0]]),list1)
    print(list(l2))
