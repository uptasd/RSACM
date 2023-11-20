import html
import json
import re
from urllib import parse

import requests

GOOGLE_TRANSLATE_URL = 'http://translate.google.com/m?q=%s&tl=%s&sl=%s'


def translate(text, to_language="auto", text_language="auto"):
    text = parse.quote(text)
    url = GOOGLE_TRANSLATE_URL % (text, to_language, text_language)
    response = requests.get(url)
    data = response.text
    expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
    result = re.findall(expr, data)
    if len(result) == 0:
        return ""

    return html.unescape(result[0])


def load_json(file_path="../asset/SYS-3rd.json"):
    with open(file_path, encoding='UTF-8', errors='ignore') as json_file:
        data = json.load(json_file)
    return data


# print(translate("产后护理", "en", "zh-CN"))  # 汉语转英语
equip_tec_translate = dict()
json_data = load_json("../../asset/equipment_technology/equip_tec-small.json")
for department_name, fun_equip_tec in json_data.items():
    department_name_en = translate(department_name, "en", "zh-CN")
    equip_tec_translate[department_name_en] = list()
    for equipment_tec in fun_equip_tec:
        e_t = dict()
        (function_name, equip_and_tec), = equipment_tec.items()
        function_name_en = translate(function_name, "en", "zh-CN")
        e_t[function_name_en] = list()
        equip_names_en = list()
        tec_names_en = list()
        for equip_name in equip_and_tec[0]:
            equip_name_en = translate(equip_name, "en", "zh-CN")
            equip_names_en.append(equip_name_en)
        for tec_name in equip_and_tec[1]:
            tec_name_en = translate(tec_name, "en", "zh-CN")
            tec_names_en.append(tec_name_en)
        e_t[function_name_en].append(equip_names_en)
        e_t[function_name_en].append(tec_names_en)
        equip_tec_translate[department_name_en].append(e_t)
    print(department_name+" done")
print("here")
with open("../../asset/equip_tec-en.json", 'w', encoding='utf-8') as json_file:
    json.dump(equip_tec_translate, json_file, ensure_ascii=False)
