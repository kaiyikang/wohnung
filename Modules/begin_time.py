import json
import os
import glob
import time
import datetime
import numpy as np
from Modules.base_utils import dump_time_dist

def dump_latest():
    arg = {"top_n":10,"is_print":False,"wohnung_type":"wg1"}
    # Get all json list from dataset folder
    pattern = "dataset/latest.json"
    json_lst = glob.glob(pattern)[0]
    return dump_time_dist(arg,json_lst)