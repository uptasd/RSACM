import os

import numpy as np
from matplotlib import pyplot as plt


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "已创建")

    else:
        print(path + "已存在")


class PltUtil:
    fontsize = 15
    font2 = {
        'weight': 'normal',
        'size': 15,
    }

    def __init__(self, file_path, noise_rate):
        self.file_path = file_path
        self.hit_rate_file_name = "命中率-" + str(noise_rate) + ".txt"
        self.res_retrieve_time_file_name = "检索资源时间-" + str(noise_rate) + ".txt"
        self.state_propagation_time_file_name = "状态传播时间-" + str(noise_rate) + ".txt"
        self.state_update_req_file_name = "状态更新次数-事件-" + str(noise_rate) + ".txt"
        self.state_update_event_file_name = "状态更新次数-需求-" + str(noise_rate) + ".txt"
        self.state_update_regular_file_name = "状态更新次数-周期性-" + str(noise_rate) + ".txt"
        # self.error_rate_wrong_file_name = "功能agent容量-正确.txt"
        # self.error_rate_right_file_name = "功能agent容量-错误.txt"
        mkdir(file_path + "output/")
        self.save_path = file_path
        # self.hit_rate_data = []
        self.plt_hit_rate()
        self.plt_update_num()
        self.plt_retrieve_time()
        self.plt_propagation_time()
        # self.plt_error_rate()

    def read_hit_rate_data(self):
        hit_rate_data = []
        cnt = 0
        with open(self.file_path + self.hit_rate_file_name, 'r') as e:
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

    def read_update_num_data(self):
        state_update_req = []
        state_update_event = []
        state_update_regular = []
        with open(self.file_path + self.state_update_req_file_name, 'r') as e:
            data = e.readlines()
            for d in data:
                x = str(d.split(":")[0])
                y = str(d.split(":")[1].replace("\n", ""))
                state_update_req.append(int(y))
        with open(self.file_path + self.state_update_event_file_name, 'r') as e:
            data = e.readlines()
            for d in data:
                x = str(d.split(":")[0])
                y = str(d.split(":")[1].replace("\n", ""))
                state_update_event.append(int(y))
        with open(self.file_path + self.state_update_regular_file_name, 'r') as e:
            data = e.readlines()
            for d in data:
                x = str(d.split(":")[0])
                y = str(d.split(":")[1].replace("\n", ""))
                state_update_regular.append(int(y))
        # return [state_update_req[i] + state_update_event[i] + state_update_regular[i] for i in
        #         range(min(len(state_update_req), len(state_update_event)))]
        return state_update_regular

    def read_propagation_time_data(self):
        state_propagation_time = []
        with open(self.file_path + self.state_propagation_time_file_name, 'r') as e:
            data = e.readlines()
            for d in data:
                x = str(d.split(":")[0])
                y = str(d.split(":")[1].replace("\n", ""))
                state_propagation_time.append(int(y))
        return state_propagation_time

    def read_retrieve_time_data(self):
        res_retrieve_time = []
        with open(self.file_path + self.res_retrieve_time_file_name, 'r') as e:
            data = e.readlines()
            for d in data:
                x = str(d.split(":")[0])
                y = str(d.split(":")[1].replace("\n", ""))
                res_retrieve_time.append(int(y))
        return res_retrieve_time

    def read_error_rate_data(self):
        right_data = dict()
        wrong_data = dict()
        with open(self.file_path + self.error_rate_right_file_name, 'r') as e:
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
        with open(self.file_path + self.error_rate_wrong_file_name, 'r') as e:
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
        for p, r_data in right_data.items():
            w_data = wrong_data[p]
            error_num = 0
            for agent_name, r_status in r_data.items():
                if agent_name not in w_data:
                    continue
                w_status = w_data[agent_name]
                if r_status != w_status:
                    error_num += 1
            e_rate = error_num / len(w_data)
            error_rate.append(e_rate)
        return error_rate

    def plt_hit_rate(self):
        hit_rate_data = self.read_hit_rate_data()
        period = range(1, len(hit_rate_data) + 1)
        hit_rate = hit_rate_data
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.plot(period, hit_rate, linewidth=1, color="black", marker="o", label="hit rate")
        plt.legend(["Hit Rate"], loc="upper left")
        plt.xlabel("period", self.font2)
        plt.ylabel("hit rate", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.savefig(self.save_path + "output/hit-rate.png")
        plt.close()

    def plt_update_num(self):
        update_num_data = self.read_update_num_data()
        period = range(1, len(update_num_data) + 1)
        update_num = update_num_data
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.plot(period, update_num, linewidth=1, color="black", marker="o", label="Number of state updates")
        plt.legend(["Number of state updates"], loc="upper left")
        plt.xlabel("period", self.font2)
        plt.ylabel("Number of state updates", self.font2)
        print(max(update_num))
        my_y_ticks = np.arange(0, max(update_num) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.savefig(self.save_path + "output/Number of state updates.png")
        plt.close()

    def plt_retrieve_time(self):
        retrieve_time_data = self.read_retrieve_time_data()
        period = range(1, len(retrieve_time_data) + 1)
        retrieve_time = retrieve_time_data
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.plot(period, retrieve_time, linewidth=1, color="black", marker="o", label="Resource retrieve time")
        plt.legend(["Resource retrieve time"], loc="upper left")
        plt.xlabel("period", self.font2)
        plt.ylabel("Resource retrieve time", self.font2)
        print(max(retrieve_time))
        my_y_ticks = np.arange(0, max(retrieve_time) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.savefig(self.save_path + "output/Resource retrieve time.png")
        plt.close()

    def plt_propagation_time(self):
        propagation_time_data = self.read_propagation_time_data()
        period = range(1, len(propagation_time_data) + 1)
        propagation_time = propagation_time_data
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.plot(period, propagation_time, linewidth=1, color="black", marker="o", label="State propagation time")
        plt.legend(["State propagation time"], loc="upper left")
        plt.xlabel("period", self.font2)
        plt.ylabel("State propagation time", self.font2)
        print(max(propagation_time))
        my_y_ticks = np.arange(0, max(propagation_time) + 10, 50)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(my_y_ticks)
        plt.savefig(self.save_path + "output/State propagation time.png")
        plt.close()
