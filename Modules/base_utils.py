import json
import os
import glob
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

pattern = "dataset/*.json"
json_lst = glob.glob(pattern)


sample = json_lst[2]

# Opening JSON file
f = open(sample)
try:
    wohnung_lst = json.load(f)
except:
    raise sample + " 文件出现问题。"
f.close()

crawl_time = wohnung_lst[0]['crawltime']
pilot_time = datetime.datetime.strptime(crawl_time, "%Y-%m-%d")

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

# calculate the distance
# for idx, i in enumerate(time_dist_lst):
#     if i > 0:
#         print(i, wohnung_lst[idx])

time_dst_lst = time_dist_lst[time_dist_lst>0]

dst_mean = np.mean(time_dst_lst)
dst_var = np.var(time_dst_lst)
dst_std = np.std(time_dst_lst)

time_dst_lst = time_dst_lst[time_dst_lst<3*dst_mean]

print(time_dst_lst)

time_bin_count = np.bincount(time_dst_lst) # count based on index
print(time_bin_count)
time_bin_count_sorted = time_bin_count.argsort()[::-1] # index in list
print(time_bin_count_sorted)