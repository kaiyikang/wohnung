import json
import os
import glob
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tqdm import tqdm

def get_statistic_info(values:list) -> dict:
    """calculate all statistic value,

    Args:
        values (list): array with full value

    Returns:
        dict: calculated static value
    """
    val_mean = np.mean(values)
    val_var = np.var(values)
    val_std = np.std(values)
    
    return {'mean':val_mean,"var":val_var,"std":val_std}


def dump_time_dist(arg,json_path):

    # Opening JSON file
    f = open(json_path)
    try:
        wohnung_lst = json.load(f)
    except:
        return None
    f.close()

    # set pilot time
    crawl_time = wohnung_lst[0]['crawltime']
    pilot_time = datetime.datetime.strptime(crawl_time, "%Y-%m-%d")

    # read all start time
    time_dist_lst = np.zeros(len(wohnung_lst),dtype=int)
    for idx, wohnung in enumerate(wohnung_lst):
        ok_time = wohnung['zeit'].split('-')
        if len(ok_time) == 1:
            start_time = ok_time[0][2:] # ab00.00.0000
            start_time = datetime.datetime.strptime(start_time, "%d.%m.%Y")
        elif len(ok_time) == 2:
            start_time = ok_time[0]
            end_time = ok_time[1]
            start_time = datetime.datetime.strptime(start_time, "%d.%m.%Y")
            end_time = datetime.datetime.strptime(end_time, "%d.%m.%Y")

        time_dist_lst[idx] = (start_time - pilot_time).days

    # DEBUG
    # calculate the distance
    # for idx, i in enumerate(time_dist_lst):
    #     if i > 0:
    #         print(i, wohnung_lst[idx])

    # Filter the all days bigger than zero
    time_dst_lst = time_dist_lst[time_dist_lst>0]

    # calculate 
    val = get_statistic_info(time_dst_lst)

    time_dst_lst = time_dst_lst[time_dst_lst<3*val['mean']]
    time_bin_count = np.bincount(time_dst_lst) # count based on index
    time_bin_count_sorted = time_bin_count.argsort()[::-1] # index in list

    if arg["is_print"]:
        print(time_dst_lst)
        print(time_bin_count)
        print(time_bin_count_sorted)
    
    return time_bin_count_sorted[:arg["top_n"]]
    
    
# Get all json list from dataset folder
pattern = "dataset/*.json"
json_lst = glob.glob(pattern)

pbar = tqdm(total=len(json_lst))
print_str = []
for json_path in json_lst:    
    time_dist = dump_time_dist({"top_n":10,"is_print":False},json_path)
    print_str.append("{0}: {1}".format(json_path.split("\\")[-1][:-5],time_dist))
    pbar.update(1)
pbar.close()

print("===== date and top-10 time distance =====")
for i in print_str:
    print(i)
