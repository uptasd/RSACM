import copy
import json

import requests


def load_json(file_path="../asset/SYS-3rd.json"):
    with open(file_path, encoding='UTF-8', errors='ignore') as json_file:
        json_data = json.load(json_file)
    return json_data


url = "https://openai.api2d.net/v1/chat/completions"

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer fk211567-cliEzBHayft6eLbi9yr66vvq7IMC7OG9'
    # <-- 把 fkxxxxx 替换成你自己的 Forward Key，注意前面的 Bearer 要保留，并且和 Key 中间有一个空格。
}
return_format = '\n只返回结果，并使用json格式，如：{{"{}":[\"相似科室1\"，\"相似科室2\",...]}}\n如果不匹配任何一个就返回{{"{}":[]}}'
requestMSG = """在大多数医院中，与{}类似的科室通常是哪几个？在提供的医疗服务等方面类似即可，尝试在以下给出的科室中查找：{}\n """

dep_list = ["胃肠手术功能保护研究中心", "临床营养科", "脊柱侧弯中心", "心脏康复中心", "产科", "肝胆外科", "输血科", "妇科", "肝脏外科暨肝移植中心", "脑血管外科", "神经外科",
            "甲状腺、乳腺外科", "化妆品评价中心", "酒精性肝病中心", "变态反应（过敏）学科", "胸痛中心", "卒中中心", "药剂科", "血管外科", "放射科", "核医学科", "病理科", "检验科",
            "生物治疗中心", "肿瘤放射治疗科", "生殖医学中心", "眼科", "中医科", "感染性疾病科", "皮肤性病科", "口腔科", "耳鼻咽喉科", "介入科", "内科ICU", "儿科",
            "不育与性医学科", "风湿免疫科", "内分泌与代谢病学科", "全科医学科", "急诊医学科", "手术麻醉中心", "肾脏内科", "精神与神经疾病研究中心", "肿瘤内科", "胃肠外科", "血液内科",
            "心血管内科", "消化内科", "呼吸与危重症医学科", "纳米医学中心", "整形烧伤科", "精神（心理）科", "心胸外科", "神经内科", "康复医学科", "外科ICU", "儿童行为发育中心",
            "泌尿外科", "超声科"]


def ask_replaceable_dep(dep_name, dep_list, requestMSG, return_format):
    dep_list_ = copy.deepcopy(dep_list)
    dep_list_.remove(dep_name)
    MSG = requestMSG.format(dep_name, str(",".join(dep_list_)))
    MSG += return_format.format(dep_name,dep_name)
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user",
                      "content": MSG}]
    }
    response = requests.post(url, headers=headers, json=data)
    print("ask ", dep_name)
    print("JSON Response ", response.json())
    return response




if __name__ == '__main__':
    ans = list()
    num = 2
    cnt = 1
    for dep_name in dep_list:
        j = ask_replaceable_dep(dep_name, dep_list, requestMSG, return_format).json()
        content = j['choices'][0]['message']['content']
        content = content.replace('\\', "")
        content = content.replace('\n', "")
        d = json.loads(content)
        ans.append(d)
        if cnt > num:
            break
        cnt += 1
    json_mp = dict()
    for data in ans:
        json_mp.update(data)
    with open("dep_replacement.json", 'w', encoding='utf-8') as f:
        json.dump(json_mp, fp=f, ensure_ascii=False)
# dep_list_ = copy.deepcopy(dep_list)
# dep_list_.remove("胃肠手术功能保护研究中心")
# requestMSG = requestMSG.format("胃肠手术功能保护研究中心", str(",".join(dep_list_)))
# requestMSG += return_format
# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user",
#                   "content": requestMSG}]
# }
# #
# response = requests.post(url, headers=headers, json=data)
#
# print("Status Code", response.status_code)
# print("JSON Response ", response.json())
# j = response.json()
# content = j['choices'][0]['message']['content']
# content = content.replace('\\', "")
# d = json.loads(content)
# with open("answerTest.json", 'w', encoding='utf-8') as f:
#     json.dump(d, fp=f, ensure_ascii=False)
