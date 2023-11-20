import os

import matplotlib.pyplot as plt

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

    def __init__(self, file_path, file_name, env_name):
        self.x_data = []
        self.y_data = []
        self.file_path = file_path
        self.file_name = file_name
        self.save_path = ""
        self.env_name = env_name

        self.noise_rate = 0
        if env_name == "Regular Environment":
            self.noise_rate = 0
        elif env_name == "Weak Noise Environment":
            self.noise_rate = 40
        elif env_name == "Strong Noise Environment":
            self.noise_rate = 80
        output_file_dir = self.file_name.split("-")[0] + "-" + self.file_name.split("-")[1]
        self.save_path = "../output/noise" + str(self.noise_rate) + "/" + output_file_dir+"/"
        mkdir(self.save_path)
        self.read_txt()
        self.plt_agent_availability()
        self.plt_agent_volume()

    def read_txt(self):
        with open(self.file_path + self.file_name, 'r') as e:
            data = e.readlines()
        for d in data:
            x = int(d.split(":")[0])
            y = int(d.split(":")[1].replace("\n", ""))
            self.x_data.append(x)
            self.y_data.append(y)
        return self.x_data, self.y_data

    def plt_agent_volume(self):
        period = self.x_data
        volume = self.y_data
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        plt.plot(period, volume, linewidth=1, color="black", marker="o", label="Service Capacity")
        plt.legend(["Service Capacity"], loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel(self.env_name+"\nService Capacity", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.title(self.env_name)
        plt.savefig(self.save_path + "capacity.png")
        plt.close()

    def plt_agent_availability(self):
        period = self.x_data
        availability = []
        fig = plt.figure(figsize=(900 / 72, 400 / 72))
        for y in self.y_data:
            if y > 0:
                availability.append(1)
            else:
                availability.append(0)
        plt.plot(period, availability, linewidth=1, color="black", marker="o", label="State Availability")
        plt.legend(["State Availability"], loc="upper left")
        plt.xlabel("Period (Hour)", self.font2)
        plt.ylabel(self.env_name+"\nState Availability", self.font2)
        plt.xticks(fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize)
        plt.title(self.env_name)
        plt.savefig(self.save_path + "availability.png")
        plt.close()
