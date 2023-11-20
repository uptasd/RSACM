import math

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame

from pltUTL import read_update_num_data, read_retrieve_time_data, read_propagation_time_data, PltUtil, mkdir, \
    read_error_rate_data, read_hit_rate_data, read_state_capacity_data


def plt_heatmap(dic, heatmap_file_path, heatmap_file_name):
    df = DataFrame(dic)
    data_corr = df.corr()
    plt.figure(figsize=(900 / 72, 350 / 72))
    fig = sns.heatmap(data_corr, annot=True, vmax=1, square=True, cmap="Blues", fmt='.2g')
    fig.get_figure().savefig(heatmap_file_path + heatmap_file_name, bbox_inches='tight',
                             transparent=True)


def plt_mean_data(mean_data_list, data_type, file_path, file_name):
    y = mean_data_list
    x = range(len(mean_data_list))
    plt.figure(figsize=(850 / 72, 350 / 72))
    plt.plot(x, y, linewidth=1, color="orange", marker="o",
             label=data_type)
    plt.savefig(file_path + file_name)
    plt.close()


def get_data_threshold(env_name):
    RSACM_mutil_dir = "../e2/asset/mutil/"
    RSACM_single_dir = "../e2/asset/single/"
    half_RSACM_mutil_dir = "../e3/asset/mutil/"
    half_RSACM_single_dir = "../e3/asset/single/"
    k_v = dict()
    noise_rate = 0
    if env_name == "规则":
        noise_rate = 0
    elif env_name == "弱噪声":
        noise_rate = 20
    elif env_name == "强噪声":
        noise_rate = 80
    noise_rate = str(noise_rate)
    RSACM_mutil_dir += "mutil" + str(noise_rate) + "/"
    RSACM_single_dir += "single" + str(noise_rate) + "/"
    half_RSACM_mutil_dir += "mutil" + str(noise_rate) + "/"
    half_RSACM_single_dir += "single" + str(noise_rate) + "/"
    number_of_state_updates_filename = "状态更新次数-周期性-" + noise_rate + ".txt"
    state_propagation_time_filename = "状态传播时间-" + noise_rate + ".txt"
    resource_retrieve_time_filename = "检索资源时间-" + noise_rate + ".txt"
    hit_rate_of_resource_filename = "命中率-" + noise_rate + ".txt"
    # RSACM_mutil_data = read_update_num_data(RSACM_mutil_dir, number_of_state_updates_filename)
    # half_RSACM_mutil_data = read_update_num_data(half_RSACM_mutil_dir, number_of_state_updates_filename)
    # RSACM_single_data = read_update_num_data(RSACM_single_dir, number_of_state_updates_filename)
    # half_RSACM_single_data = read_update_num_data(half_RSACM_single_dir, number_of_state_updates_filename)
    # max1 = max(RSACM_mutil_data)
    # max2 = max(half_RSACM_mutil_data)
    # max3 = max(RSACM_single_data)
    # max4 = max(half_RSACM_single_data)
    paths = [RSACM_mutil_dir, half_RSACM_mutil_dir, RSACM_single_dir, half_RSACM_single_dir]
    m = get_max(read_update_num_data, paths, number_of_state_updates_filename)
    n = get_num(50, m)
    k_v["Number of state updates"] = n
    m = get_max(read_retrieve_time_data, paths, resource_retrieve_time_filename)
    n = get_num(50, m)
    k_v["Resource retrieve time"] = n
    m = get_max(read_propagation_time_data, paths, state_propagation_time_filename)
    n = get_num(50, m)
    k_v["State propagation time"] = n
    print("[info]" + env_name + "环境阈值计算结束")
    return k_v


def get_max(fun, file_paths, file_name):
    RSACM_mutil_data = fun(file_paths[0], file_name)
    half_RSACM_mutil_data = fun(file_paths[1], file_name)
    RSACM_single_data = fun(file_paths[2], file_name)
    half_RSACM_single_data = fun(file_paths[3], file_name)
    max1 = max(RSACM_mutil_data)
    max2 = max(half_RSACM_mutil_data)
    max3 = max(RSACM_single_data)
    max4 = max(half_RSACM_single_data)

    return max(max1, max2, max3, max4)


def get_num(limit_num, num):
    if num % limit_num == 0:
        return num
    else:
        num = math.ceil(num / limit_num) * limit_num
        return num


def get_corr(file_name):
    pass
    # RSACM_mutil_dir = "../e3/asset/mutil/"
    # RSACM_single_dir = "../e3/asset/single/"
    # half_RSACM_mutil_dir = "../e2/asset/mutil/"
    # half_RSACM_single_dir = "../e2/asset/single/"
    # RSACM_mutil_dir += "mutil" + str(noise_rate) + "/"
def cal_():
    half_RSACM_output = "output/half_RSACM/"
    RSACM_output = "output/RSACM/"
    mkdir(half_RSACM_output)
    mkdir(RSACM_output)
    noise_list = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]

    error_rate_dict = dict()
    error_rate_mean_list = []
    hit_rate_dict = dict()
    hit_rate_mean_list = []
    Num_updates_dict = dict()
    Num_updates_mean_list = []
    retrieve_time_dict = dict()
    retrieve_time_mean_list = []
    propagation_time_dict = dict()
    propagation_time_mean_list = []
    capacity_dict = dict()

    h_error_rate_dict = dict()
    h_error_rate_mean_list = []
    h_hit_rate_dict = dict()
    h_hit_rate_mean_list = []
    h_Num_updates_dict = dict()
    h_Num_updates_mean_list = []
    h_retrieve_time_dict = dict()
    h_retrieve_time_mean_list = []
    h_propagation_time_dict = dict()
    h_propagation_time_mean_list = []
    h_capacity_dict = dict()

    corr_list = []
    h_corr_list = []
    for noise_rate in noise_list:
        noise_rate = str(noise_rate)
        RSACM_mutil_dir = "../e2/asset/mutil/mutil"
        half_RSACM_mutil_dir = "../e3/asset/mutil/mutil"
        RSACM_mutil_dir += noise_rate + "/"
        half_RSACM_mutil_dir += noise_rate + "/"
        number_of_state_updates_filename = "状态更新次数-周期性-" + noise_rate + ".txt"
        state_propagation_time_filename = "状态传播时间-" + noise_rate + ".txt"
        resource_retrieve_time_filename = "检索资源时间-" + noise_rate + ".txt"
        hit_rate_of_resource_filename = "命中率-" + noise_rate + ".txt"
        State_availability_filename = "中山大学第三附属医院-服务大厅功能-" + noise_rate + ".txt"
        # x = PltUtil(regular_env, mutil_process, noise_rate)
        half_RSACM_error_rate = read_error_rate_data(half_RSACM_mutil_dir, RSACM_mutil_dir)
        RSACM_error_rate = [0] * 240
        h_error_rate_dict[noise_rate] = half_RSACM_error_rate
        error_rate_dict[noise_rate] = RSACM_error_rate

        RSACM_hit_rate_data = read_hit_rate_data(RSACM_mutil_dir, hit_rate_of_resource_filename)
        half_RSACM_hit_rate_data = read_hit_rate_data(half_RSACM_mutil_dir, hit_rate_of_resource_filename)
        hit_rate_dict[noise_rate] = RSACM_hit_rate_data
        h_hit_rate_dict[noise_rate] = half_RSACM_hit_rate_data

        RSACM_update_num_data = read_update_num_data(RSACM_mutil_dir, number_of_state_updates_filename)
        half_RSACM_update_num_data = read_update_num_data(half_RSACM_mutil_dir, number_of_state_updates_filename)
        Num_updates_dict[noise_rate] = RSACM_update_num_data
        h_Num_updates_dict[noise_rate] = half_RSACM_update_num_data

        RSACM_retrieve_time_data = read_retrieve_time_data(RSACM_mutil_dir, resource_retrieve_time_filename)
        half_RSACM_retrieve_time_data = read_retrieve_time_data(half_RSACM_mutil_dir, resource_retrieve_time_filename)
        retrieve_time_dict[noise_rate] = RSACM_retrieve_time_data
        h_retrieve_time_dict[noise_rate] = half_RSACM_retrieve_time_data

        RSACM_propagation_time_data = read_propagation_time_data(RSACM_mutil_dir, state_propagation_time_filename)
        half_RSACM_propagation_time_data = read_propagation_time_data(half_RSACM_mutil_dir,
                                                                      state_propagation_time_filename)
        propagation_time_dict[noise_rate] = RSACM_propagation_time_data
        h_propagation_time_dict[noise_rate] = half_RSACM_propagation_time_data

        RSACM_State_capacity = read_state_capacity_data(RSACM_mutil_dir, State_availability_filename)
        half_RSACM_State_capacity = read_state_capacity_data(half_RSACM_mutil_dir,
                                                             State_availability_filename)
        capacity_dict[noise_rate] = RSACM_State_capacity
        h_capacity_dict[noise_rate] = half_RSACM_State_capacity
        RSACM_dict = {
            "State Capacity": RSACM_State_capacity,
            "Number of State Updates": RSACM_update_num_data,
            "State Propagation Time": RSACM_propagation_time_data,
            "Hit Rate of Resource": RSACM_hit_rate_data,
            "Error Rate of Resource": RSACM_error_rate,
            "Resource Retrieval Time": RSACM_retrieve_time_data
        }
        half_RSACM_dict = {
            "State Capacity": half_RSACM_State_capacity,
            "Number of State Updates": half_RSACM_update_num_data,
            "State Propagation Time": half_RSACM_propagation_time_data,
            "Hit Rate of Resource": half_RSACM_hit_rate_data,
            "Error Rate of Resource": half_RSACM_error_rate,
            "Resource Retrieval Time": half_RSACM_retrieve_time_data
        }
        RSACM_df = DataFrame(RSACM_dict)
        half_RSACM_df = DataFrame(half_RSACM_dict)
        RSACM_corr = RSACM_df.corr()
        half_RSACM_corr = half_RSACM_df.corr()
        corr_list.append(RSACM_corr)
        h_corr_list.append(half_RSACM_corr)
    # # 计算错误率的在不同噪声下的相关率
    plt_heatmap(error_rate_dict, RSACM_output, "RSACM_error_rate.png")
    plt_heatmap(h_error_rate_dict, half_RSACM_output, "half_RSACM_error_rate.png")
    # #
    # # # 计算命中率的在不同噪声下的相关率
    plt_heatmap(hit_rate_dict, RSACM_output, "RSACM_hit_rate_dict.png")
    plt_heatmap(h_hit_rate_dict, half_RSACM_output, "half_RSACM_hit_rate.png")
    # # 计算状态变化数的在不同噪声下的相关率
    plt_heatmap(Num_updates_dict, RSACM_output, "RSACM_num_updates.png")
    plt_heatmap(h_Num_updates_dict, half_RSACM_output, "half_RSACM_num_updates.png")
    # # 计算检索时间的在不同噪声下的相关率
    plt_heatmap(retrieve_time_dict, RSACM_output, "RSACM_retrieve_time.png")
    plt_heatmap(h_retrieve_time_dict, half_RSACM_output, "half_RSACM_retrieve_time.png")
    # # 计算传播时间在不同噪声下的相关率
    plt_heatmap(propagation_time_dict, RSACM_output, "RSACM_propagation_time.png")
    plt_heatmap(h_propagation_time_dict, half_RSACM_output, "half_RSACM_propagation_time.png")
    # # 计算容量在不同噪声下的相关率
    plt_heatmap(capacity_dict, RSACM_output, "RSACM_capacity_dict.png")
    plt_heatmap(h_capacity_dict, half_RSACM_output, "half_RSACM_capacity_dict.png")
    plt.close()
    plt.clf()
    # 将每个关联性提取出来
    data_arrays = np.zeros((10, 6, 6))
    h_data_arrays = np.zeros((10, 6, 6))
    for i, df in enumerate(corr_list):
        data_arrays[i] = df.values
    for i, df in enumerate(h_corr_list):
        h_data_arrays[i] = df.values
    plt.figure(figsize=(850 / 72, 350 / 72))
    label_names = ["num_capacity",
                   "propa_avail", "propa_num",
                   "hit_avail", "hit_num", "hit_propa",
                   "error_avail", "error_num", "error_propa", "error_hit",
                   "retrie_avail", "retrie_num", "retrie_propa", "retrie_hit", "retrie_error"]
    _label_names = ["num_capacity",
                    "propa_avail", "propa_num",
                    "hit_avail", "hit_num", "hit_propa",
                    "error_avail", "error_num", "error_propa", "error_hit",
                    "retrie_avail", "retrie_num", "retrie_propa", "retrie_hit", "retrie_error"]
    labels_dic = dict()
    _labels_dict = dict()
    k = 0
    for i in range(1, 6):
        for j in range(0, i):
            labels_dic[label_names[k]] = str(i) + "," + str(j)
            _labels_dict[_label_names[k]] = str(i) + "," + str(j)
            k += 1
    corr_dir = RSACM_output + "corr/"
    mkdir(corr_dir)
    for label, index in labels_dic.items():
        x = int(index.split(",")[0])
        y = int(index.split(",")[1])
        data = data_arrays[:, x, y].tolist()
        data = np.nan_to_num(data)
        if label == "error_avail":
            print("he")
        plt.plot(range(10), data, linewidth=1, color="orange", marker="o", label=label)
        # print(label+":"+str(data))
        # plt.show()
        plt.savefig(corr_dir + label + ".png")
        # plt.cla()
        plt.clf()

    corr_dir = half_RSACM_output + "corr/"
    mkdir(corr_dir)
    plt.cla()
    plt.close()
    for label, index in _labels_dict.items():
        x = int(index.split(",")[0])
        y = int(index.split(",")[1])
        data = np.nan_to_num(0)
        data = h_data_arrays[:, x, y].tolist()
        if label == "error_avail":
            print("he")
        plt.plot(range(10), data, linewidth=1, color="orange", marker="o", label=label)
        plt.savefig(corr_dir + label + ".png")
        plt.cla()
        plt.close()

if __name__ == '__main__':
    regular_env = "规则"
    weak_env = "弱噪声"
    strong_env = "强噪声"
    mutil_process = "mutil"
    single_process = "single"
    # x = PltUtil(regular_env, mutil_process, 0)
    # x = PltUtil(regular_env, mutil_process, 10)
    # x = PltUtil(regular_env, mutil_process, 20)
    # x = PltUtil(regular_env, mutil_process, 30)
    # x = PltUtil(regular_env, mutil_process, 40)
    # x = PltUtil(regular_env, mutil_process, 50)
    # x = PltUtil(regular_env, mutil_process, 60)
    # x = PltUtil(regular_env, mutil_process, 70)
    # x = PltUtil(regular_env, mutil_process, 80)
    # x = PltUtil(regular_env, mutil_process, 90)
    # k_v = get_data_threshold(regular_env)
    # x = PltUtil(regular_env, mutil_process, k_v)
    x = PltUtil(regular_env, mutil_process)
    # x = PltUtil(regular_env, single_process)
    # x = PltUtil(regular_env, single_process, k_v)
    # k_v = get_data_threshold(weak_env)
    # x = PltUtil(weak_env, mutil_process, k_v)
    x = PltUtil(weak_env, mutil_process)
    # x = PltUtil(weak_env, single_process)
    # x = PltUtil(weak_env, single_process, k_v)
    # k_v = get_data_threshold(strong_env)
    # x = PltUtil(strong_env, mutil_process, k_v)
    x = PltUtil(strong_env, mutil_process)
    # x = PltUtil(strong_env, single_process)
    # x = PltUtil(strong_env, single_process, k_v)



