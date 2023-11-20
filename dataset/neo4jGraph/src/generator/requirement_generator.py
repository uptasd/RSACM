# 挂号，导诊，就诊，治疗
import os
import shutil

import numpy as np
from py2neo import Graph

# 1 = 60分钟
from neo4jGraph.src.generator.agent_generator import save2json


def process_float(s: float) -> str:
    return str(s).split('.')[0] + '.' + str(s).split('.')[1][:2]


one_minute = 1 / 60
register_online_time = process_float(one_minute * 3)  # 3分钟
register_offline_time = process_float(one_minute * 5)  # 5分钟
guidance_online_time = process_float(one_minute * 2)  # 2分钟
guidance_offline_time = process_float(one_minute * 3)  # 3分钟
ask_doctor_time = process_float(one_minute * 10)  # 10分钟
check_time = process_float(one_minute * 120)  # 120分钟
diagnosis_time = process_float(one_minute * 15)  # 15分钟
get_medicine_time = process_float(one_minute * 10)  # 10分钟
healing_time = process_float(one_minute * 180)  # 180分钟
hospitalized_time = process_float(one_minute * 60 * 72)  # 3天


class RequireGenerator:
    def __init__(self, database, auth):
        self.requirements = list()
        self.graph = Graph(database, auth=auth)
        self.department = None

    def chain(self, requirement_type):
        requirement = list()
        if requirement_type == "多流程":
            cnt = 0
            com_num = np.random.randint(2, 5)
            register_requirement = self.register_step()
            requirement.append(register_requirement)
            cnt += 1
            guidance_requirement = self.guidance_step()
            while not guidance_requirement:
                guidance_requirement = self.guidance_step()
            requirement.append(guidance_requirement)
            cnt += 1
            if cnt < com_num:
                doctor_working = self.doctor_working_step(requirement_type)
                requirement.extend(doctor_working)
                cnt += 1
                if cnt < com_num:
                    healing = self.healing_step(requirement_type)
                    if healing:
                        requirement.extend(healing)
                        cnt += 1
        else:
            step = np.random.randint(0, 3)
            if step == 0:
                register_requirement = self.register_step()
                if register_requirement:
                    requirement.append(register_requirement)
            elif step == 1:
                doctor_working = self.doctor_working_step(requirement_type)
                requirement.extend(doctor_working)
            elif step == 2:
                healing = self.healing_step(requirement_type)
                while not healing:
                    healing = self.healing_step(requirement_type)
                requirement.extend(healing)

        qos = ["high-quality", "low-cost"]
        urgency_level = [1, 2, 3]
        qos = np.random.choice(qos, 1, p=[0.5, 0.5])[0]
        urgency_level = np.random.choice(urgency_level, 1)[0]
        rs = dict()
        rs["requirements"] = requirement
        rs["qos"] = qos
        rs["urgencyLevel"] = int(urgency_level)
        rs["type"] = requirement_type
        # requirement.append(f"服务质量:{qos}")
        # requirement.append(f"紧急程度:{urgency_level}")
        return rs

    def register_step(self):
        """
        :return: 50% return offline ,50% online
        """
        register = ["MATCH (n) WHERE n:`医院挂号_线上` AND n:`实例功能` RETURN n",
                    "MATCH (n) WHERE n:`医院挂号_线下` AND n:`实例功能` RETURN n"]
        flag = np.random.choice([0, 1], 1, p=[0.5, 0.5])[0]
        result_cypher = register[flag]
        rs = self.graph.run(result_cypher).data()[0]
        if flag == 0:
            return rs['n']['name'] + ":" + register_online_time
        else:
            return rs['n']['name'] + ":" + register_offline_time

    def guidance_step(self):
        """
        2/7 return guidance ,3/7 return nothing
        50% return offline ,50% online
        :return:
        """
        flag = np.random.choice([0, 1], 1, p=[2 / 7, 5 / 7])
        if flag == 0:
            return
        else:
            guidance = ["MATCH (n) WHERE n:`问诊引导_线上` AND n:`实例功能` return n",
                        "MATCH (n) WHERE n:`问诊引导_线下` AND n:`实例功能` return n"]
            flag = np.random.choice([0, 1], 1, p=[0.5, 0.5])[0]
            guidance_cypher = guidance[flag]
            rs = self.graph.run(guidance_cypher).data()[0]
            if flag == 0:
                return rs['n']['name'] + ":" + guidance_online_time
            else:
                return rs['n']['name'] + ":" + guidance_offline_time

    def doctor_working_step(self, requirement_type):
        """
        ask,check,diagnosis
        :return:
        """
        require_list = list()
        department_chose_cypher = "MATCH (n) WHERE n:`实例功能` AND n:`科室功能` RETURN n"
        department_function_list = list()
        department_functions = self.graph.run(department_chose_cypher).data()
        for department in department_functions:
            department_function_list.append(department['n']['name'])
        self.department = str(np.random.choice(department_function_list, 1)[0])
        self.department = self.department.split('-')[0]
        ask_doctor_cypher = ["MATCH (n:`科室问诊_线下`{name:'" + self.department + "-科室问诊_线下'}) RETURN n",
                             "MATCH (n:`科室问诊_线上`{name:'" + self.department + "-科室问诊_线上'}) RETURN n"]
        ask_doctor = np.random.choice(ask_doctor_cypher, 1, p=[0.5, 0.5])[0]
        ask_doctor_require = self.graph.run(ask_doctor).data()[0]['n']['name'] + ":" + ask_doctor_time
        require_list.append(ask_doctor_require)
        if requirement_type == "单流程":
            return require_list
        flag = np.random.choice([0, 1], 1, p=[6 / 10, 4 / 10])
        if flag == 1:
            check_cypher = "MATCH (n) WHERE n:`医疗检测_线下` AND n:`实例功能` RETURN n"
            check_requirements = self.graph.run(check_cypher).data()
            if check_requirements:
                check_requirement = np.random.choice(check_requirements, 1)[0]['n']['name'] + ':' + check_time
                require_list.append(check_requirement)
        flag = np.random.choice([0, 1], 1, p=[5 / 10, 5 / 10])
        if flag == 1:
            diagnosis_cypher = ["MATCH (n:`医疗诊断_线上`{name:'" + self.department + "-医疗诊断_线上'}) RETURN n",
                                "MATCH (n:`医疗诊断_线下`{name:'" + self.department + "-医疗诊断_线下'}) RETURN n"]
            diagnosis = np.random.choice(diagnosis_cypher, 1, p=[0.5, 0.5])[0]
            diagnosis_require = self.graph.run(diagnosis).data()[0]['n']['name'] + ":" + diagnosis_time
            require_list.append(diagnosis_require)
        return require_list

    def healing_step(self, requirement_type):
        """
        get medicine,healing,hospitalized
        :return:
        """
        if not self.department:
            department_chose_cypher = "MATCH (n) WHERE n:`实例功能` AND n:`科室功能` RETURN n"
            department_function_list = list()
            department_functions = self.graph.run(department_chose_cypher).data()
            for department in department_functions:
                department_function_list.append(department['n']['name'])
            self.department = str(np.random.choice(department_function_list, 1)[0])
            self.department = self.department.split('-')[0]
        require_list = list()
        flag = np.random.choice([0, 1], 1, p=[5 / 10, 5 / 10])
        if flag == 1:
            get_medicine_cypher = "MATCH (n) WHERE n:`药店取药` AND n:`实例功能` RETURN n"
            get_medicine_require = self.graph.run(get_medicine_cypher).data()[0]['n']['name'] + ":" + get_medicine_time
            require_list.append(get_medicine_require)
            if requirement_type == "单流程":
                return require_list
        flag = np.random.choice([0, 1], 1, p=[5 / 10, 5 / 10])
        if flag == 1:
            healing_cypher = "MATCH (n{name:'" + self.department + "-科室功能'}) -[r:`聚合医疗服务`]-> (m) return m"
            healing_require = self.graph.run(healing_cypher).data()
            if healing_require:
                healing_require = np.random.choice(healing_require, 1)[0]
                healing_require = healing_require['m']['name'] + ":" + healing_time
                require_list.append(healing_require)
                if requirement_type == "单流程":
                    return require_list
        flag = np.random.choice([0, 1], 1, p=[5 / 10, 5 / 10])
        if flag == 1:
            hospitalized_cypher = "MATCH (n{name:'" + self.department + "-病房-病房住宿'})return n"
            hospitalized_require = self.graph.run(hospitalized_cypher).data()
            if hospitalized_require:
                hospitalized_require = hospitalized_require[0]['n']['name'] + ":" + hospitalized_time
                require_list.append(hospitalized_require)
        return require_list


def del_file(filepath):
    del_list = os.listdir(filepath)
    for f in del_list:
        file_path = os.path.join(filepath, f)
        if os.path.isfile(file_path):
            os.remove(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


if __name__ == '__main__':

    database = ''
    auth = ("", "")
    output_dir = "../../asset/requirements/output/"
    requirements = RequireGenerator(database, auth)
    delimiter = ","
    period = 10 * 24
    requirements_list = dict()
    for p in range(period):
        requirementList = list()
        # requirementNum = np.random.randint(1, 4)
        requirementNum = 1
        for i in range(requirementNum):
            rq_type = np.random.choice(["多流程", "单流程"], 1)[0]
            rq_type = "单流程"
            x = requirements.chain(rq_type)
            requirementList.append(x)
        requirements_list[str(p + 1) + "周期"] = requirementList
    if rq_type == "单流程":
        save2json(requirements_list, output_dir + "requirementsSingle.json")
    else:
        save2json(requirements_list, output_dir + "requirementsMulti.json")
    # save2json(requirements_list, output_dir + "requirementsSingle.json")
    # with open(output_dir + "requirements.txt", 'w', encoding='utf-8') as f:
    #     f.write("")
    # for i in range(0, 10):
    #     with open(output_dir + "requirements.txt", 'a', encoding='utf-8') as f:
    #         f.write(delimiter.join(requirements.chain()))
    #         f.write("\n")
    # print(requirements.chain())
    print("here")
