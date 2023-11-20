from PIL import Image
from matplotlib import pyplot as plt

from pltUTL import PltUtil


def show_one_picture(path1, path2, path3):
    plt.subplot(2, 3, 1)
    plt.title("noise0")
    plt.imshow(Image.open(path1))
    plt.subplot(2, 3, 2)
    plt.title("noise20")
    plt.imshow(Image.open(path2))
    plt.subplot(2, 3, 3)
    plt.title("noise80")
    plt.imshow(Image.open(path3))
    plt.savefig("compare.png")


if __name__ == '__main__':
    noise0 = 0
    noise40 = 40
    noise80 = 80
    noise_path = "../asset/noise0/"

    res1_file_path = noise_path + "xxx-医生/"
    res1_filename = "xxx-医生-" + str(noise0) + ".txt"
    fun1_file_path = noise_path + "xxx-医生值班/"
    fun1_filename = "xxx-医生值班-" + str(noise0) + ".txt"
    env_name = "Regular Environment"
    res_plt_tool = PltUtil(res1_file_path, res1_filename, env_name)
    fun_plt_tool = PltUtil(fun1_file_path, fun1_filename, env_name)

    noise_path = "../asset/noise40/"
    res1_file_path = noise_path + "xxx-医生/"
    res1_filename = "xxx-医生-" + str(noise40) + ".txt"
    fun1_file_path = noise_path + "xxx-医生值班/"
    fun1_filename = "xxx-医生值班-" + str(noise40) + ".txt"
    env_name = "Weak Noise Environment"
    res_plt_tool = PltUtil(res1_file_path, res1_filename, env_name)
    fun_plt_tool = PltUtil(fun1_file_path, fun1_filename, env_name)

    noise_path = "../asset/noise80/"
    res1_file_path = noise_path + "xxx-医生/"
    res1_filename = "xxx-医生-" + str(noise80) + ".txt"
    fun1_file_path = noise_path + "xxx-医生值班/"
    fun1_filename = "xxx-医生值班-" + str(noise80) + ".txt"
    env_name = "Strong Noise Environment"
    res_plt_tool = PltUtil(res1_file_path, res1_filename, env_name)
    fun_plt_tool = PltUtil(fun1_file_path, fun1_filename, env_name)
