import time

import numpy as np
from matplotlib import pyplot as plt

from pltUTL import PltUtil

if __name__ == '__main__':
    today = time.strftime("%Y-%m-%d", time.localtime())
    save_path = "../output/" + str(today) + "/"
    x_list = []
    large_single_data_list = []
    mid_single_data_list = []
    small_single_data_list = []
    large_num = 2103
    mid_num = 1423
    small_num = 718
    for i in range(0, 100, 10):
        x_list.append(int(i/10))
        large_single_data, mid_single_data, small_single_data = PltUtil(i).get_mean_hit_rate()
        large_single_data_list.append(large_single_data)
        mid_single_data_list.append(mid_single_data)
        small_single_data_list.append(small_single_data)
    x=np.arange(len(large_single_data_list))
    bar_width = 0.25
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_color('none')
    plt.bar(x-bar_width, large_single_data_list, bar_width, color='orange', label=str(small_num)+"nodes")
    plt.bar(x, mid_single_data_list, bar_width, color='cornflowerblue', label=str(mid_num) + "nodes")
    plt.bar(x+bar_width, large_single_data_list, bar_width, color='blue', label=str(large_num) + "nodes")
    plt.legend()
    plt.xticks(x, x_list)
    plt.ylim(0,0.9)
    plt.legend(bbox_to_anchor=(0.5,1.05),loc=10,ncol=3)
    plt.ylabel("Mean Hit Rate of Resource")
    plt.xlabel("Environment")

    plt.savefig(save_path + "Mean hit rate of resource.png")

