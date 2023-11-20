import json


def load_json(file_path):
    with open(file_path, encoding='UTF-8', errors='ignore') as json_file:
        json_data = json.load(json_file)
    return json_data


def save2json(json_data, json_name):
    with open(json_name, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


if __name__ == '__main__':
    replacementsMap_dir = "../../asset/replacements/"
    save_dir = replacementsMap_dir+"output/"
    department_replace = load_json(replacementsMap_dir+"department_replaceMap.json")
    replaceMap = dict()
    for department_name, replaces in department_replace.items():
        if len(replaces) == 0:
            continue
        department_doctor_work = [department_name + "-医生值班", "-医生值班"]
        department_doctor_nurse_work = [department_name + "-护士值班", "-护士值班"]
        department_clinc = [department_name + "-问诊场所功能", "-问诊场所功能"]
        department_ask_online = [department_name + "-科室问诊_线上", "-科室问诊_线上"]
        department_ask_offline = [department_name + "-科室问诊_线下", "-科室问诊_线下"]
        department_operating_room = [department_name + "-手术室-场所功能", "-手术室-场所功能"]
        department_sick_room = [department_name + "-病房-病房住宿", "-病房-病房住宿"]
        functions = [department_doctor_work, department_doctor_nurse_work, department_clinc,
                     department_ask_online, department_ask_offline, department_operating_room,
                     department_sick_room]
        for fun in functions:
            replaceMap[fun[0]] = list()
            for rep in replaces:
                replaceMap[fun[0]].append(rep + fun[1])
    save2json(replaceMap, save_dir+"replaceMap.json")
    print("here")
