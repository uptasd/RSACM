import os
import time

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from pandas import DataFrame


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
        print("[" + file_path + hit_rate_file_name + "]" + "success:" + str(cnt))
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
            y = int(d.split(":")[1].replace("\n", ""))
            # if y >= 200:
            #     y = int(sum(state_propagation_time) / len(state_propagation_time))
            state_propagation_time.append(y)
        wash_data(state_propagation_time)
    return state_propagation_time


def read_retrieve_time_data(file_path, res_retrieve_time_file_name):
    res_retrieve_time = []
    with open(file_path + res_retrieve_time_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = str(d.split(":")[0])
            y = int(d.split(":")[1].replace("\n", ""))
            # if y >= 200:
            #     if len(res_retrieve_time)==0:
            #         print(file_path+res_retrieve_time_file_name+":"+x)
            #     y = int(sum(res_retrieve_time)/len(res_retrieve_time))
            # if np.isnan(y):
            #     print(x)
            #     print(y)
            res_retrieve_time.append(y)
        wash_data(res_retrieve_time)
    return res_retrieve_time


def wash_data(data):
    mean_value = np.mean(data)
    for i in range(len(data)):
        if data[i] > mean_value * 2:
            data[i] = mean_value
    return data


def read_error_rate_data(half_file_path, file_path):
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
    with open(half_file_path + error_rate_of_resource_wrong, 'r') as e:
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


def read_state_availability_data(file_path, state_availability_file_name):
    state_availability = []
    with open(file_path + state_availability_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = int(d.split(":")[0])
            if x == 0:
                continue
            y = int(d.split(":")[1].replace("\n", ""))
            if y > 0:
                y = 1
            state_availability.append(int(y))
    return state_availability


def read_state_capacity_data(file_path, state_availability_file_name):
    state_capacity = []
    with open(file_path + state_availability_file_name, 'r') as e:
        data = e.readlines()
        for d in data:
            x = int(d.split(":")[0])
            if x == 0:
                continue
            y = int(d.split(":")[1].replace("\n", ""))
            state_capacity.append(int(y))
    return state_capacity


class PltUtil:
    fontsize = 15
    font2 = {
        'weight': 'normal',
        'size': 15,
    }

    def __init__(self, env_type, require_type,k_v=dict()):
        self.half_RSACM_path = "../e3/asset/"
        self.RSACM_path = "../e2/asset/"
        toHour = time.strftime("%Y-%m-%d", time.localtime())
        self.save_path = "../output/" + str(toHour) + "/"
        self.noise_rate = 0
        self.env_name = "Weak Noise Environment"
        self.k_v = k_v
        if require_type == "mutil":
            prefix = "Multi Requirements in "
        else:
            prefix = "Single Requirement in "
        prefix=""
        if env_type == "规则":
            self.env_name = "Regular Environment"
            self.noise_rate = 0
        elif env_type == "弱噪声":
            self.env_name = "Weak Noise Environment"
            self.noise_rate = 40
        elif env_type == "强噪声":
            self.env_name = "Strong Noise Environment"
            self.noise_rate = 80
        self.env_name = prefix + self.env_name
        noise_rate = str(self.noise_rate)
        self.save_path += noise_rate + "/" + require_type + "/"
        mkdir(self.save_path)
        self.half_RSACM_path += require_type + "/" + require_type + noise_rate + "/"
        self.RSACM_path += require_type + "/" + require_type + noise_rate + "/"
        self.number_of_state_updates_filename = "状态更新次数-周期性-" + noise_rate + ".txt"
        self.state_propagation_time_filename = "状态传播时间-" + noise_rate + ".txt"
        self.resource_retrieve_time_filename = "检索资源时间-" + noise_rate + ".txt"
        self.hit_rate_of_resource_filename = "命中率-" + noise_rate + ".txt"
        self.State_availability_filename = "中山大学第三附属医院-服务大厅功能-" + noise_rate + ".txt"
        self.RSACM_hit_rate = None
        self.half_RSACM_hit_rate = None

        self.RSACM_update_num = None
        self.half_RSACM_update_num = None

        self.RSACM_retrieve_time = None
        self.half_RSACM_retrieve_time = None

        self.RSACM_propagation_time = None
        self.half_RSACM_propagation_time = None

        self.RSACM_error_rate = None
        self.half_RSACM_error_rate = None

        self.RSACM_corr = None
        self.half_RSACM_corr = None
        self.plt_all()

    def plt_all(self):
        self.RSACM_hit_rate, self.half_RSACM_corr = self.plt_hit_rate()
        self.RSACM_update_num, self.half_RSACM_update_num = self.plt_update_num()
        self.RSACM_retrieve_time, self.half_RSACM_retrieve_time = self.plt_retrieve_time()
        self.RSACM_propagation_time, self.half_RSACM_propagation_time = self.plt_propagation_time()
        self.plt_error_rate()
        self.RSACM_corr, half_RSACM_corr = self.plt_heatmap()
        plt.close()

    def plt_hit_rate(self):
        RSACM_hit_rate_data = read_hit_rate_data(self.RSACM_path, self.hit_rate_of_resource_filename)
        half_RSACM_hit_rate_data = read_hit_rate_data(self.half_RSACM_path, self.hit_rate_of_resource_filename)

        period = range(1, 240 + 1)
        half_RSACM_hit_rate = half_RSACM_hit_rate_data
        RSACM_hit_rate = RSACM_hit_rate_data
        # fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.figure(figsize=(850 / 72, 350 / 72))
        plt.ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.plot(period, RSACM_hit_rate, linewidth=1, color="darkorange", marker="o", label="Hit Rate of Resource "
                                                                                            "- RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Hit Rate of Resource", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.axhline(y=np.nanmean(RSACM_hit_rate), color="darkorange")
        plt.text(period[-1], np.nanmean(RSACM_hit_rate), str(np.round(np.nanmean(RSACM_hit_rate), 3)))
        plt.plot(period, half_RSACM_hit_rate, linewidth=1, color="royalblue", marker="|", label="Hit Rate of Resource "
                                                                                                "- Half-RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Hit Rate of Resource", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.axhline(y=np.nanmean(half_RSACM_hit_rate), color="royalblue")
        plt.text(period[-1], np.nanmean(half_RSACM_hit_rate), str(np.round(np.nanmean(half_RSACM_hit_rate), 3)))
        plt.title(self.env_name)
        # plt.figure(figsize=(900 / 72, 330/ 72))
        plt.savefig(self.save_path + "hit-rate.png")
        plt.close()
        return RSACM_hit_rate, half_RSACM_hit_rate_data

    def plt_update_num(self):
        RSACM_update_num_data = read_update_num_data(self.RSACM_path, self.number_of_state_updates_filename)
        half_RSACM_update_num_data = read_update_num_data(self.half_RSACM_path, self.number_of_state_updates_filename)
        period = range(1, len(RSACM_update_num_data) + 1)
        half_RSACM_update_num = half_RSACM_update_num_data
        RSACM_update_num = RSACM_update_num_data

        plt.figure(figsize=(850 / 72, 350 / 72))
        plt.plot(period, RSACM_update_num_data, linewidth=1, color="orange", marker="o", label="Number of State "
                                                                                               "Updates- RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Number of State Updates", self.font2)
        plt.axhline(y=np.nanmean(RSACM_update_num_data), color="orange")
        plt.text(period[-1], np.nanmean(RSACM_update_num_data), str(np.round(np.nanmean(RSACM_update_num_data), 3)))
        if "Number of state updates" in self.k_v:
            y_max = self.k_v["Number of state updates"]
            plt.ylim(0, y_max + 10)
            plt.yticks(range(0, y_max + 10, 50))
        plt.plot(period, half_RSACM_update_num_data, linewidth=1, color="green", marker="|", label="Number of State "
                                                                                                   "Updates- Half-RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Number of State Updates", self.font2)
        # print(max(update_num))
        my_y_ticks = np.arange(0, max(max(half_RSACM_update_num), max(RSACM_update_num)) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.axhline(y=np.nanmean(half_RSACM_update_num), color="green")
        plt.text(period[-1], np.nanmean(half_RSACM_update_num), str(np.round(np.nanmean(half_RSACM_update_num), 3)))
        plt.title(self.env_name)
        # plt.figure(figsize=(900 / 72, 330/ 72))
        if "Number of state updates" in self.k_v:
            y_max = self.k_v["Number of state updates"]
            plt.ylim(0, y_max + 10)
            plt.yticks(range(0, y_max + 10, 50))
        plt.savefig(self.save_path + "Number of state updates.png")
        plt.close()
        return RSACM_update_num, half_RSACM_update_num

    def plt_retrieve_time(self):
        RSACM_retrieve_time_data = read_retrieve_time_data(self.RSACM_path, self.resource_retrieve_time_filename)
        half_RSACM_retrieve_time_data = read_retrieve_time_data(self.half_RSACM_path,
                                                                self.resource_retrieve_time_filename)
        period = range(1, len(RSACM_retrieve_time_data) + 1)
        RSACM_retrieve_time = RSACM_retrieve_time_data
        half_RSACM_retrieve_time = half_RSACM_retrieve_time_data

        plt.figure(figsize=(850 / 72, 350 / 72))
        plt.plot(period, RSACM_retrieve_time, linewidth=1, color="darkgoldenrod", marker="o",
                 label="Resource Retrieve Time "
                       "- RSACM")
        plt.legend(["Resource Retrieve Time"], loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Resource Retrieve Time (ms)", self.font2)
        plt.axhline(y=np.nanmean(RSACM_retrieve_time), color="darkgoldenrod")
        plt.text(period[-1], np.nanmean(RSACM_retrieve_time), str(np.round(np.nanmean(RSACM_retrieve_time), 3)))
        if "Resource retrieve time" in self.k_v:
            y_max = self.k_v["Resource retrieve time"]
            plt.ylim(0, y_max)
            plt.yticks(range(0, y_max + 10, 50))
        plt.plot(period, half_RSACM_retrieve_time, linewidth=1, color="royalblue", marker="|",
                 label="Resource Retrieve Time -Half RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Resource Retrieve Time (ms)", self.font2)
        # print(max(retrieve_time))
        my_y_ticks = np.arange(0, max(max(RSACM_retrieve_time), max(half_RSACM_retrieve_time)) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.axhline(y=np.nanmean(half_RSACM_retrieve_time), color="royalblue")
        plt.text(period[-1], np.nanmean(half_RSACM_retrieve_time),
                 str(np.round(np.nanmean(half_RSACM_retrieve_time), 3)))
        plt.title(self.env_name)
        # plt.figure(figsize=(900 / 72, 330/ 72))
        if "Resource retrieve time" in self.k_v:
            y_max = self.k_v["Resource retrieve time"]
            plt.ylim(0, y_max)
            plt.yticks(range(0, y_max + 10, 50))
        plt.savefig(self.save_path + "Resource retrieve time.png")
        plt.close()
        return RSACM_retrieve_time, half_RSACM_retrieve_time

    def plt_propagation_time(self):
        RSACM_propagation_time_data = read_propagation_time_data(self.RSACM_path, self.state_propagation_time_filename)
        half_RSACM_propagation_time_data = read_propagation_time_data(self.half_RSACM_path,
                                                                      self.state_propagation_time_filename)
        period = range(1, len(RSACM_propagation_time_data) + 1)
        RSACM_propagation_time = RSACM_propagation_time_data
        half_RSACM_propagation_time = half_RSACM_propagation_time_data

        plt.figure(figsize=(850 / 72, 350 / 72))
        plt.plot(period, RSACM_propagation_time, linewidth=1, color="orange", marker="o",
                 label="State Propagation Time - RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("State Propagation Time (ms)", self.font2)
        plt.axhline(y=np.nanmean(RSACM_propagation_time), color="orange")
        plt.text(period[-1], np.nanmean(RSACM_propagation_time), str(np.round(np.nanmean(RSACM_propagation_time), 3)))

        if "State propagation time" in self.k_v:
            y_max = self.k_v["State propagation time"]
            plt.ylim(0, y_max)
            plt.yticks(range(0, y_max + 10, 50))
        plt.plot(period, half_RSACM_propagation_time, linewidth=1, color="green", marker="|",
                 label="State Propagation Time - Half-RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("State Propagation Time (ms)", self.font2)
        # print(max(RSACM_propagation_time))
        my_y_ticks = np.arange(0, max(max(RSACM_propagation_time), max(half_RSACM_propagation_time)) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.axhline(y=np.nanmean(half_RSACM_propagation_time), color="green")
        plt.text(period[-1], np.nanmean(half_RSACM_propagation_time),
                 str(np.round(np.nanmean(half_RSACM_propagation_time), 3)))
        plt.title(self.env_name)
        # plt.figure(figsize=(900 / 72, 330/ 72))
        if "State propagation time" in self.k_v:
            y_max = self.k_v["State propagation time"]
            plt.ylim(0, y_max)
            plt.yticks(range(0, y_max + 10, 50))
        plt.savefig(self.save_path + "State propagation time.png")
        plt.close()
        return RSACM_propagation_time, half_RSACM_propagation_time

    def plt_error_rate(self):
        error_rate_data = read_error_rate_data(self.half_RSACM_path, self.RSACM_path)
        period = range(1, len(error_rate_data) + 1)
        half_RSACM_error_rate = error_rate_data
        RSACM_error_rate = [0] * len(error_rate_data)

        plt.figure(figsize=(850 / 72, 350 / 72))
        plt.plot(period, RSACM_error_rate, linewidth=1, color="darkgoldenrod", marker="o", label="Error Rate of "
                                                                                                 "Resource - RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Error Rate of Resource", self.font2)
        # print(max(error_rate))
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.plot(period, half_RSACM_error_rate, linewidth=1, color="royalblue", marker="|",
                 label="Error Rate of Resource - Half RSACM")
        plt.legend(loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel("Error Rate of Resource", self.font2)
        # print(max(error_rate))
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.axhline(y=np.nanmean(half_RSACM_error_rate), color="royalblue")
        plt.text(period[-1], np.nanmean(half_RSACM_error_rate), str(np.round(np.nanmean(half_RSACM_error_rate), 3)))
        plt.title(self.env_name)
        # plt.figure(figsize=(900 / 72, 330/ 72))
        plt.ylim(0, 1)
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.savefig(self.save_path + "error-rate.png")
        plt.close()

    def plt_heatmap(self):
        RSACM_update_num_data = read_update_num_data(self.RSACM_path, self.number_of_state_updates_filename)
        half_RSACM_update_num_data = read_update_num_data(self.half_RSACM_path, self.number_of_state_updates_filename)
        half_RSACM_error_rate = read_error_rate_data(self.half_RSACM_path, self.RSACM_path)
        RSACM_error_rate = [0] * 240
        RSACM_propagation_time_data = read_propagation_time_data(self.RSACM_path, self.state_propagation_time_filename)
        half_RSACM_propagation_time_data = read_propagation_time_data(self.half_RSACM_path,
                                                                      self.state_propagation_time_filename)
        RSACM_retrieve_time_data = read_retrieve_time_data(self.RSACM_path, self.resource_retrieve_time_filename)
        half_RSACM_retrieve_time_data = read_retrieve_time_data(self.half_RSACM_path,
                                                                self.resource_retrieve_time_filename)
        RSACM_hit_rate_data = read_hit_rate_data(self.RSACM_path, self.hit_rate_of_resource_filename)
        half_RSACM_hit_rate_data = read_hit_rate_data(self.half_RSACM_path, self.hit_rate_of_resource_filename)
        RSACM_State_capacity = read_state_capacity_data(self.RSACM_path, self.State_availability_filename)
        half_RSACM_State_capacity = read_state_capacity_data(self.half_RSACM_path,
                                                             self.State_availability_filename)
        # RSACM_dict = {
        #     "Service Capacity": RSACM_State_capacity,
        #     "Number of State Updates": RSACM_update_num_data,
        #     "State Propagation Time": RSACM_propagation_time_data,
        #     "Hit Rate of Resource": RSACM_hit_rate_data,
        #     "Error Rate of Resource": RSACM_error_rate,
        #     "Resource Retrieval Time": RSACM_retrieve_time_data
        # }
        # half_RSACM_dict = {
        #     "Service Capacity": half_RSACM_State_capacity,
        #     "Number of State Updates": half_RSACM_update_num_data,
        #     "State Propagation Time": half_RSACM_propagation_time_data,
        #     "Hit Rate of Resource": half_RSACM_hit_rate_data,
        #     "Error Rate of Resource": half_RSACM_error_rate,
        #     "Resource Retrieval Time": half_RSACM_retrieve_time_data
        # }
        RSACM_dict = {
            "SC": RSACM_State_capacity,
            "NSU": RSACM_update_num_data,
            "SPT": RSACM_propagation_time_data,
            "HR": RSACM_hit_rate_data,
            "ER": RSACM_error_rate,
            "RT": RSACM_retrieve_time_data
        }
        half_RSACM_dict = {
            "SC": half_RSACM_State_capacity,
            "NSU": half_RSACM_update_num_data,
            "SPT": half_RSACM_propagation_time_data,
            "HR": half_RSACM_hit_rate_data,
            "ER": half_RSACM_error_rate,
            "RT": half_RSACM_retrieve_time_data
        }
        RSACM_df = DataFrame(RSACM_dict)
        half_RSACM_df = DataFrame(half_RSACM_dict)
        RSACM_corr = RSACM_df.corr()
        half_RSACM_corr = half_RSACM_df.corr()
        # plt.subplots(figsize=(9, 9), facecolor='w')
        plt.figure(figsize=(900 / 72, 350 / 72))
        fig = sns.heatmap(RSACM_corr, annot=True, vmax=1, square=True, cmap="Blues", fmt='.2g')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.title("RSACM in the " + self.env_name+"\n", fontsize=20, fontweight="light")

        fig.get_figure().savefig(self.save_path + 'RSACM_corr' + str(self.noise_rate) + '.png', bbox_inches='tight',
                                 transparent=True)
        plt.cla()
        plt.close()
        plt.figure(figsize=(900 / 72, 350 / 72))
        fig = sns.heatmap(half_RSACM_corr, annot=True, vmax=1, square=True, cmap="Blues", fmt='.2g')
        plt.xticks(fontsize=20)
        plt.yticks(fontsize=20)
        plt.title("Half-RSACM in the " + self.env_name+"\n", fontsize=20, fontweight="light")

        fig.get_figure().savefig(self.save_path + 'half_RSACM_corr' + str(self.noise_rate) + '.png',
                                 bbox_inches='tight', transparent=True)
        plt.close()
        return RSACM_corr, half_RSACM_corr

    def get_corr(self):
        return self.half_RSACM_corr, self.RSACM_corr

    def get_hit_rate(self):
        return self.half_RSACM_corr, self.RSACM_hit_rate

    def get_update_num(self):
        return self.RSACM_update_num, self.half_RSACM_update_num

    def get_retrieve_time(self):
        return self.RSACM_retrieve_time, self.half_RSACM_retrieve_time

    def get_propagation_time(self):
        return self.RSACM_propagation_time, self.half_RSACM_propagation_time

    def get_error_rate(self):
        return self.RSACM_error_rate, self.half_RSACM_error_rate
