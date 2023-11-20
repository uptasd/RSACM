import os

from matpolt.e2.src.pltUTL import PltUtil


def mkdir(path):
    folder = os.path.exists(path)

    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print(path + "已创建")

    else:
        print(path + "已存在")


if __name__ == '__main__':
    single0_path = "../asset/single/history2023-10-12/2023-10-12-23-21/single0/"
    single20_path = "../asset/single/single20/"
    single40_path = "../asset/single/history2023-10-12/2023-10-12-23-21/single40/"
    single80_path = "../asset/single/history2023-10-12/2023-10-12-23-21/single80/"
    mutil0_path = "../asset/mutil/history/r2/mutil0/"
    mutil20_path = "../asset/mutil/history/r4/mutil20/"
    mutil40_path = "../asset/mutil/history/r2/mutil40/"
    mutil80_path = "../asset/mutil/history/r2/mutil80/"
    single0_output_path = single0_path + "output/"
    single20_output_path = single20_path + "output/"
    single80_output_path = single80_path + "output/"
    x = PltUtil(single0_path, 0)
    x = PltUtil(single40_path, 40)
    x = PltUtil(single80_path, 80)
    x = PltUtil(mutil0_path, 0)
    x = PltUtil(mutil40_path, 40)
    x = PltUtil(mutil80_path, 80)

