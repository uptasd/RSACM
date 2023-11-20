import os
import time

import numpy as np
from matplotlib import pyplot as plt


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "已创建")

    else:
        print(path + "已存在")


def read_hit_rate_data(file_path, hit_rate_file_name):
    hit_rate_data = []
    cnt = 0
    with open(file_path + hit_rate_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            y1 = int(y.split("/")[0])
            y2 = float(y.split("/")[1])
            if y1 == int(y2):
                # print(x)
                cnt += 1
            hit_rate_data.append(y1 / y2)
        print("success:" + str(cnt))
    return hit_rate_data


def read_update_num_data(file_path, state_update_regular_file_name):
    state_update_regular = []
    with open(file_path + state_update_regular_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            state_update_regular.append(int(y))
    return state_update_regular


def read_propagation_time_data(file_path, state_propagation_time_file_name):
    state_propagation_time = []
    with open(file_path + state_propagation_time_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            state_propagation_time.append(int(y))
    return state_propagation_time


def read_retrieve_time_data(file_path, res_retrieve_time_file_name):
    res_retrieve_time = []
    with open(file_path + res_retrieve_time_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            res_retrieve_time.append(int(y))
    return res_retrieve_time


def read_error_rate_data(file_path):
    error_rate_of_resource_right = "功能agent容量-正确.txt"
    error_rate_of_resource_wrong = "功能agent容量-错误.txt"
    right_data = dict()
    wrong_data = dict()
    with open(file_path + error_rate_of_resource_right, 'r') as e:
        data = e.readlines()
        pre_period = "1-1"
        period_dict = dict()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            period = x
            agent_name = y.split(",")[0]
            service_num = int(y.split(",")[1])
            if pre_period != period:
                right_data[pre_period] = period_dict.copy()
                period_dict.clear()
                pre_period = period
            period_dict[agent_name] = service_num
        right_data[period] = period_dict.copy()
    with open(file_path + error_rate_of_resource_wrong, 'r') as e:
        data = e.readlines()
        pre_period = "1-1"
        period_dict = dict()
        for d in data:
            x = str(d.split(":")[0])
            y = str(d.split(":")[1].replace("\n", ""))
            period = x
            agent_name = y.split(",")[0]
            service_num = int(y.split(",")[1])
            if pre_period != period:
                wrong_data[pre_period] = period_dict.copy()
                period_dict.clear()
                pre_period = period
            period_dict[agent_name] = service_num
        wrong_data[period] = period_dict.copy()
    error_rate = []
    for p, w_data in wrong_data.items():
        r_data = right_data[p]
        error_num = 0
        for agent_name, w_status in w_data.items():
            if agent_name not in r_data:
                print(p + ":" + agent_name + "不存在")
                continue
            r_status = r_data[agent_name]
            if w_status != r_status:
                error_num += 1
        e_rate = error_num / len(w_data)
        error_rate.append(e_rate)
    return error_rate


class PltUtil:
    fontsize = 15
    font2 = {
        'weight': 'normal',
        'size': 15,
    }

    def __init__(self, noise_rate):
        self.id = int(noise_rate / 10) + 1
        noise_rate = str(noise_rate)
        self.noise_rate = noise_rate
        self.asset_dir = "../asset/"
        self.small_dataset = self.asset_dir + "single-small/single" + noise_rate + "/"
        self.mid_dataset = self.asset_dir + "single-mid/single" + noise_rate + "/"
        self.large_dataset = self.asset_dir + "single-large/single" + noise_rate + "/"
        self.large_num = 2103
        self.mid_num = 1423
        self.small_num = 718
        today = time.strftime("%Y-%m-%d", time.localtime())
        self.save_path = "../output/" + str(today) + "/"

        mkdir(self.save_path)
        self.number_of_state_updates_filename = "状态更新次数-周期性-" + noise_rate + ".txt"
        # self.state_propagation_time_filename = "状态传播时间-" + noise_rate + ".txt"
        # self.resource_retrieve_time_filename = "检索资源时间-" + noise_rate + ".txt"
        self.hit_rate_of_resource_filename = "命中率-" + noise_rate + ".txt"
        self.plt_all()

    def plt_all(self):
        self.plt_number_of_state_update()

    def plt_number_of_state_update(self):
        large_single_data = read_update_num_data(self.large_dataset, self.number_of_state_updates_filename)
        mid_single_data = read_update_num_data(self.mid_dataset, self.number_of_state_updates_filename)
        small_single_data = read_update_num_data(self.small_dataset, self.number_of_state_updates_filename)
        period = range(1, len(large_single_data) + 1)
        fig = plt.figure(figsize=(850 / 72, 350 / 72))
        plt.plot(period, large_single_data, linewidth=1, color="royalblue", marker="o",
                 label="RSACM with " + str(self.large_num) + " nodes")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Number of State Updates", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.plot(period, mid_single_data, linewidth=1, color="green", marker="o",
                 label="RSACM with " + str(self.mid_num) + " nodes")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Number of State Updates", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.plot(period, small_single_data, linewidth=1, color="darkgoldenrod", marker="o",
                 label="RSACM with " + str(self.small_num) + " nodes")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Number of State Updates", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.title("Number of State Updates in Environment " + str(self.id-1))
        plt.savefig(self.save_path + "Number of state updates-" + self.noise_rate + ".png")
        plt.close()

    def get_mean_hit_rate(self):
        large_single_data = read_hit_rate_data(self.large_dataset, self.hit_rate_of_resource_filename)
        mid_single_data = read_hit_rate_data(self.mid_dataset, self.hit_rate_of_resource_filename)
        small_single_data = read_hit_rate_data(self.small_dataset, self.hit_rate_of_resource_filename)
        large_single_data = np.mean(large_single_data)
        mid_single_data = np.mean(mid_single_data)
        small_single_data = np.mean(small_single_data)
        return large_single_data, mid_single_data, small_single_data
