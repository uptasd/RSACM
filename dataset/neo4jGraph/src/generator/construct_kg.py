import random

from py2neo import Node, Relationship, Subgraph, NodeMatcher

prefix = "中山大学第三附属医院"


class HospitalKG:
    nodes = dict()
    relations = list()
    resources = dict()
    functions = dict()
    process = dict()
    maintenance_personnel_id = 0
    nurse_id = 0
    departmentNum = 2
    departmentCnt = 0

    def __init__(self, website_data, equipment_tec_data, graph):
        self.website_data = website_data
        self.equipment_tec_data = equipment_tec_data
        self.graph = graph
        self.error_department = {
            "中山大学第三附属医院",
            "Ⅰ期临床研究中心",
            "骨科",
            "高血压达标中心"
        }
        self.init_graph()
        self.create_kg()


    def create_kg(self):
        for data in self.website_data:
            # data = self.website_data[4]
            department_name = data['Department_name']
            department_type = data["Department_type"]
            hospital_name = "中山大学第三附属医院"
            # department_name = hospital_name+"-"+department_name
            if department_name in self.error_department:
                continue
            if len(data["Department_member"]) == 0:
                continue
            # if self.departmentCnt == self.departmentNum:
            #     break
            self.departmentCnt += 1
            working_time = "8-18"
            max_volume = len(data['Member_introduction'])
            service_capacity = max_volume
            busy_degree = "idle"
            availability = "Available"
            average_service_time = random.randint(0, 10) + 11
            if "ICU" in department_name or "急诊" in department_name:
                working_time = "0-7,19-23"
            resource_qos = "low-cost"
            if department_name in ["胃肠手术功能保护研究中心", "脊柱侧弯中心", "心脏康复中心", "产科", "肝胆外科", "输血科", "妇科", "肝脏外科暨肝移植中心",
                                   "脑血管外科", "神经外科", "甲状腺、乳腺外科", "变态反应（过敏）学科", "胸痛中心", "卒中中心",
                                   "血管外科", "内科ICU", "外科ICU", "急诊医学科"]:
                resource_qos = "high-quality"
            department_node, department_function_node = self.add_department2graph(hospital_name, department_name,
                                                                                  working_time, resource_qos,
                                                                                  max_volume, service_capacity,
                                                                                  average_service_time)
            # department_function_node = self.add_function2resource(department_node, department_name + "-科室功能", "科室功能",
            #                                                       type="功能")
            self.add_relation2graph(self.nodes[prefix + "-医院功能"], "聚合", department_function_node)
            # 门诊室资源和功能

            outpatient_department_node = self.add_resource2graph(department_name, department_name + "-门诊室", "门诊室",
                                                                 type="agent", working_time=working_time,
                                                                 resource_qos=resource_qos, max_volume=20,
                                                                 service_capacity=10, busy_degree="idle",
                                                                 average_service_time=average_service_time,
                                                                 availability="Available")
            outpatient_department_function = self.add_function2resource(outpatient_department_node,
                                                                        department_name + "-问诊场所功能", "问诊场所功能",
                                                                        type="agent", working_time=working_time,
                                                                        max_volume=20, service_capacity=10,
                                                                        busy_degree="idle",
                                                                        average_service_time=average_service_time,
                                                                        availability="Available")
            self.add_relation2graph(department_function_node, "聚合", outpatient_department_function)
            self.add_relation2graph(self.nodes[department_name + "-科室问诊_线下"], "依赖", outpatient_department_function)
            # 护士资源和功能
            ranint = random.randint(5, 10)
            nurse_node = self.add_resource2graph(department_name, department_name + "-护士", "护士",
                                                 type="agent", working_time=working_time, resource_qos=resource_qos,
                                                 max_volume=15, service_capacity=ranint,
                                                 average_service_time=average_service_time,
                                                 busy_degree="idle", availability="Available")
            nurse_function = self.add_function2resource(nurse_node, department_name + "-护士值班", "护士值班", type="agent",
                                                        working_time=working_time, max_volume=15,
                                                        service_capacity=ranint,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available")
            self.add_relation2graph(department_function_node, "聚合", nurse_function)
            doctors_function = self.add_function2graph(department_name + "-科室功能", department_name + "-医生值班",
                                                       "医生值班", type="agent")
            if department_type == "临床专科" or department_type == "特色诊疗平台":
                # 创建手术室资源与对应功能
                operating_room_node = self.add_resource2graph(department_name, department_name + "-手术室", "手术室",
                                                              type="agent", working_time="0-23",
                                                              resource_qos=resource_qos,
                                                              max_volume=10, service_capacity=10,
                                                              average_service_time=average_service_time,
                                                              busy_degree="idle", availability="Available")
                operating_room_function = self.add_function2resource(operating_room_node,
                                                                     department_name + "-手术室" + "-场所功能", "医疗服务场所功能",
                                                                     type="agent", working_time="0-23",
                                                                     max_volume=10, service_capacity=10,
                                                                     average_service_time=average_service_time,
                                                                     busy_degree="idle", availability="Available"
                                                                     )
                self.add_relation2graph(department_function_node, "聚合", operating_room_function)
                # 创建病房资源与对应功能
                nums = random.randint(20, 50)
                sickroom_node = self.add_resource2graph(department_name, department_name + "-病房", "病房",
                                                        working_time="0-23", resource_qos=resource_qos,
                                                        max_volume=nums, service_capacity=nums,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available"
                                                        )
                sickroom_function = self.add_function2resource(sickroom_node, department_name + "-病房" + "-病房住宿", "病房住宿",
                                                               type="agent",
                                                               max_volume=nums, service_capacity=nums,
                                                               average_service_time=average_service_time,
                                                               busy_degree="idle", availability="Available"
                                                               )
                self.add_relation2graph(sickroom_function, "依赖", nurse_function)
                self.add_relation2graph(department_function_node, "聚合", sickroom_function)
                self.add_relation2graph(sickroom_function, "依赖", self.nodes[prefix + "-住院登记"])
                # 创建床位资源与对应功能

                sick_bed_node = self.add_resource2graph(department_name + "-病房", department_name + "-病房" + "-床位", "床位",
                                                        type="agent", working_time="0-23", resource_qos=resource_qos,
                                                        max_volume=nums, service_capacity=nums,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available"
                                                        )
                sick_bed_function = self.add_function2resource(sick_bed_node, department_name + "-病房" + "-床位" + "-提供床位",
                                                               "提供床位", type="agent",
                                                               max_volume=nums, service_capacity=nums,
                                                               average_service_time=average_service_time,
                                                               busy_degree="idle", availability="Available"
                                                               )
                # 《病房住宿》依赖《提供床位》
                self.add_relation2graph(sickroom_function, "依赖", sick_bed_function)
                medical_technology, medical_equipments = self.add_equipment_and_technology2department(department_name,
                                                                                                      "手术室")

            elif department_type == "医技科室":
                examination_room_node = self.add_resource2graph(department_name, department_name + "-检测室", "检测室",
                                                                type="agent", working_time=working_time,
                                                                resource_qos=resource_qos,
                                                                max_volume=5, service_capacity=5,
                                                                average_service_time="120",
                                                                busy_degree="idle", availability="Available"
                                                                )
                examination_room_function = self.add_function2resource(examination_room_node,
                                                                       department_name + "-检测室" + "-场所功能",
                                                                       "医疗检测场所功能", type="agent",
                                                                       max_volume=5, service_capacity=5,
                                                                       average_service_time="120",
                                                                       busy_degree="idle", availability="Available"
                                                                       )
                self.add_relation2graph(department_function_node, "聚合", examination_room_function)
                medical_technology, medical_equipments = self.add_equipment_and_technology2department(department_name,
                                                                                                      "检测室")
            self.add_relation2graph(self.nodes[department_name + "-医疗诊断_线上"], "依赖",
                                    self.nodes[department_name + "-医生值班"])
            self.add_relation2graph(self.nodes[department_name + "-医疗诊断_线上"], "依赖",
                                    self.nodes[prefix + "-网络服务"])

            self.add_relation2graph(self.nodes[department_name + "-医疗诊断_线下"], "依赖",
                                    self.nodes[department_name + "-医生值班"])
            self.add_relation2graph(self.nodes[department_name + "-医疗诊断_线下"], "依赖",
                                    self.nodes[department_name + "-问诊场所功能"])

            self.add_relation2graph(self.nodes[department_name + "-科室问诊_线上"], "依赖",
                                    self.nodes[department_name + "-医生值班"])
            self.add_relation2graph(self.nodes[department_name + "-科室问诊_线上"], "依赖",
                                    self.nodes[prefix + "-网络服务"])

            self.add_relation2graph(self.nodes[department_name + "-科室问诊_线下"], "依赖",
                                    self.nodes[department_name + "-医生值班"])
            self.add_relation2graph(self.nodes[department_name + "-科室问诊_线下"], "依赖",
                                    self.nodes[department_name + "-问诊场所功能"])
            member_introduction = dict()
            if 'Member_introduction' in data:
                member_introduction = data['Member_introduction']
            # 医生只有一个具体资源连接：医生->医疗设备，护士没有资源链接
            # 如果一个资源和另外所有资源都连接，比如人事部和所有医生，护士，维护人员连接，那么在实例图谱就不连接上了
            # 如果一个资源和其他资源的连接情况不明，比如护士协助医生这个连接，不能确定哪个护士协助哪个医生，那么在实例图谱就不连接上了
            i = 0
            for doctors in member_introduction:
                working_time = "8-18"
                doctors_name = doctors["姓名"]
                if "职称" in doctors:
                    doctors_title = doctors["职称"]
                else:
                    doctors_title = "医师"
                if "导师资格" in doctors:
                    doctors_qualification = doctors["导师资格"]
                else:
                    doctors_qualification = "无"
                resource_qos = "low-cost"
                if "主任" in doctors_title:
                    resource_qos = "high-quality"
                if i >= len(member_introduction) / 2 and ("ICU" in department_name or "急诊" in department_name):
                    working_time = "0-7,19-23"
                doctor_node = self.add_resource2graph(department_name, doctors_name + "-医生", "医生", title=doctors_title,
                                                      qualification=doctors_qualification, type="agent",
                                                      resource_qos=resource_qos, working_time=working_time,
                                                      average_service_time=average_service_time,
                                                      max_volume=1, service_capacity=1,
                                                      busy_degree="idle", availability="Available"
                                                      )
                # 添加关系：医生操作医疗设备,目前设置为一个医生能操作所有设备
                self.add_equipment2doctors(doctor_node, doctors_title, medical_equipments)
                # 添加功能:医生拥有医疗技术
                self.add_technology2doctors(doctor_node, doctors_title, medical_technology)
                # 添加功能:医生值班
                # doctor_function = self.add_function2resource(doctor_node, department_name + "-医生值班", "医生值班")
                # 添加医生资源到医生值班功能
                self.add_relation2graph(doctor_node, "拥有功能", self.nodes[department_name + "-医生值班"])

                # doctor_node = self.add_node2graph(doctors_name, "医生", "实例资源", title=doctors_title,
                #                                   qualification=doctors_qualification)
                # self.add_relation2graph(department_node, "拥有医生", doctor_node)
                # self.add_relation2graph(self.personnel_section_node, "管理医生", doctor_node)

            # self.add_function2resource(nurse_node, nurse_name + "-护士护理", "护士护理")
            # self.add_function2resource(nurse_node, nurse_name + "-护士协助", "护士协助")
            # if self.departmentCnt >= self.departmentNum:
            #     break
        subgraph = Subgraph(list(self.nodes.values()), self.relations)
        tx = self.graph.begin()
        tx.create(subgraph)
        self.graph.commit(tx)

    def init_graph(self):
        self.graph.delete_all()
        # 概念图谱的初始化
        self.init_abstract_graph()
        # 初始化第三附属医院的图谱

        # 创建资源节点
        hospital_node = self.add_node2graph(prefix, "医院", "实例资源", resource_qos="high-quality", working_time="0-23",
                                            max_volume=1000, service_capacity=1000,
                                            average_service_time=30,
                                            busy_degree="idle", availability="Available"
                                            )
        equipment_section_node = self.add_resource2graph(prefix, prefix + "-设备科", "设备科", working_time="8-18",
                                                         resource_qos="high-quality",
                                                         max_volume=20, service_capacity=15,
                                                         average_service_time="60",
                                                         busy_degree="idle", availability="Available"
                                                         )
        personnel_section_node = self.add_resource2graph(prefix, prefix + "-人事部", "人事部", working_time="8-18",
                                                         resource_qos="high-quality",
                                                         max_volume=20, service_capacity=15,
                                                         average_service_time="60",
                                                         busy_degree="idle", availability="Available"
                                                         )
        service_center_node = self.add_resource2graph(prefix, prefix + "-服务大厅", "服务大厅", type="agent",
                                                      working_time="0-23", resource_qos="high-quality",
                                                      average_service_time="5",
                                                      max_volume=500, service_capacity=500,
                                                      busy_degree="idle", availability="Available"
                                                      )
        pharmacy_node = self.add_resource2graph(prefix, prefix + "-药店", "药店", type="agent",
                                                working_time="0-23", resource_qos="high-quality",
                                                average_service_time="5",
                                                max_volume=500, service_capacity=500,
                                                busy_degree="idle", availability="Available"
                                                )
        server_node = self.add_resource2graph(prefix, prefix + "-服务器", "服务器", type="agent",
                                              working_time="0-23", resource_qos="high-quality",
                                              average_service_time="1",
                                              max_volume=500, service_capacity=500,
                                              busy_degree="idle", availability="Available"
                                              )
        # 实例资源节点间的关系
        # self.add_relation2graph(hospital_node, "包含", equipment_section_node)
        # self.add_relation2graph(hospital_node, "包含", personnel_section_node)
        # self.add_relation2graph(hospital_node, "包含", service_center_node)

        # 实例功能节点
        hospital_func = self.add_function2resource(hospital_node, prefix + "-医院功能", "医院功能", type="agent",
                                                   working_time="0-23",
                                                   max_volume=1000, service_capacity=1000,
                                                   average_service_time="60",
                                                   busy_degree="idle", availability="Available"
                                                   )
        registration_offline_func = self.add_function2resource(hospital_node, prefix + "-医院挂号_线下", "医院挂号_线下",
                                                               type="agent", working_time="8-18",
                                                               max_volume=1000, service_capacity=1000,
                                                               average_service_time="5",
                                                               busy_degree="idle", availability="Available"
                                                               )
        registration_online_func = self.add_function2resource(hospital_node, prefix + "-医院挂号_线上", "医院挂号_线上",
                                                              type="agent", working_time="0-23",
                                                              max_volume=1000, service_capacity=1000,
                                                              average_service_time="3",
                                                              busy_degree="idle", availability="Available")
        pharmacy_func = self.add_function2resource(pharmacy_node, prefix + "-药店取药", "药店取药", type="agent",
                                                   working_time="8-18",
                                                   max_volume=1000, service_capacity=1000,
                                                   average_service_time="5",
                                                   busy_degree="idle", availability="Available"
                                                   )
        network_func = self.add_function2resource(server_node, prefix + "-网络服务", "网络服务", type="agent",
                                                  working_time="0-23",
                                                  max_volume=500, service_capacity=500,
                                                  average_service_time="1",
                                                  busy_degree="idle", availability="Available")
        serviceHall_func = self.add_function2resource(service_center_node, prefix + "-服务大厅功能", "服务大厅功能", type="agent",
                                                      working_time="0-23",
                                                      max_volume=500, service_capacity=500,
                                                      average_service_time="1",
                                                      busy_degree="idle", availability="Available")

        inquiry_guide_offline_func = self.add_function2resource(hospital_node, prefix + "-问诊引导_线下", "问诊引导_线下",
                                                                type="agent", working_time="8-18",
                                                                max_volume=1000, service_capacity=1000,
                                                                average_service_time="5",
                                                                busy_degree="idle", availability="Available")
        inquiry_guide_online_func = self.add_function2resource(hospital_node, prefix + "-问诊引导_线上", "问诊引导_线上",
                                                               type="agent", working_time="0-23",
                                                               average_service_time="2",
                                                               max_volume=1000, service_capacity=1000,
                                                               busy_degree="idle", availability="Available")
        hospitalized_func = self.add_function2resource(hospital_node, prefix + "-住院登记", "住院登记", type="agent",
                                                       working_time="0-23",
                                                       average_service_time="3",
                                                       max_volume=1000, service_capacity=1000,
                                                       busy_degree="idle", availability="Available")

        # 添加关系
        self.add_relation2graph(hospital_func, "聚合", registration_offline_func)
        self.add_relation2graph(hospital_func, "聚合", registration_online_func)
        self.add_relation2graph(hospital_func, "聚合", inquiry_guide_offline_func)
        self.add_relation2graph(hospital_func, "聚合", inquiry_guide_online_func)
        self.add_relation2graph(hospital_func, "聚合", hospitalized_func)
        self.add_relation2graph(hospital_func, "聚合", pharmacy_func)
        self.add_relation2graph(hospital_func, "聚合", serviceHall_func)
        self.add_relation2graph(registration_online_func, "依赖", network_func)
        self.add_relation2graph(inquiry_guide_online_func, "依赖", network_func)

        self.add_relation2graph(registration_online_func, "依赖", serviceHall_func)
        self.add_relation2graph(registration_offline_func, "依赖", serviceHall_func)

        self.add_relation2graph(inquiry_guide_online_func, "依赖", serviceHall_func)
        self.add_relation2graph(inquiry_guide_offline_func, "依赖", serviceHall_func)

        self.add_relation2graph(hospitalized_func, "依赖", serviceHall_func)

        manpower_manage_func = self.add_function2resource(personnel_section_node, prefix + "-人事部" + "-人力调度", "人力调度")
        equipment_manage_func = self.add_function2resource(equipment_section_node, prefix + "-设备调度", "设备调度")
        equipment_purchase_func = self.add_function2resource(equipment_section_node, prefix + "-设备采购", "设备采购")
        equipment_scrap_func = self.add_function2resource(equipment_section_node, prefix + "-设备废弃", "设备废弃")

    def init_abstract_graph(self):
        cypher_create_resources = """CREATE (`手术室`:`概念资源`:`手术室` {name: "手术室"})<-[:概念工作]-(`护士`:`概念资源`:`护士` {name: 
        "护士"})-[:概念工作]->(`检测室`:`概念资源`:`检测室` {name: "检测室"})<-[:概念工作]-(`医生`:`概念资源`:`医生` {name: "医生"})-[:概念工作]->(
        `门诊室`:`概念资源`:`门诊室` {name: "门诊室"})<-[:概念包含]-(`科室`:`概念资源`:`科室` {name: "科室"})-[:概念管理]->(`病房`:`概念资源`:`病房` {name: 
        "病房"})<-[:概念工作]-(`护士`)<-[:概念包含]-(`科室`)-[:概念包含]->(`医生`)<-[:概念协助]-(`护士`)-[:概念办公]->(`办公室`:`概念资源`:`办公室` {name: 
        "办公室"})<-[:概念包含]-(`设备科`:`概念资源`:`设备科` {name: "设备科"})<-[:概念包含]-(`医院`:`概念资源`:`医院` {name: "医院"})-[:概念包含]->(
        `人事部`:`概念资源`:`人事部` {name: "人事部"})-[:概念管理]->(`护士`), (`办公室`)<-[:概念包含]-(`科室`)-[:概念拥有]->(`医疗设备`:`概念资源`:`医疗设备` {
        name: "医疗设备"})<-[:概念操作]-(`医生`)-[:概念办公]->(`办公室`)<-[:概念包含]-(`人事部`)-[:概念管理]->(`医生`)-[:概念掌握]->(:`概念资源`:`医疗技术` {
        name: "医疗技术"}), (`设备科`)-[:概念包含]->(`维护人员`:`概念资源`:`维护人员` {name: "维护人员"})-[:概念维护]->(`医疗设备`)<-[:概念采购]-(`设备科`), 
        (`医生`)-[:概念工作]->(`病房`)-[:概念包含]->(:`概念资源`:`床位` {name: "床位"}), (:`概念资源`:`服务大厅` {name: "服务大厅"})<-[:概念包含]-(
        `医院`)-[:概念包含]->(`科室`)-[:概念包含]->(`手术室`)<-[:概念工作]-(`医生`), (`科室`)-[:概念包含]->(`检测室`), (`护士`)-[:概念工作]->(`门诊室`), 
        (`人事部`)-[:概念管理]->(`维护人员`), (:`概念资源`:`药店` {name: "药店"})<-[:概念包含]-(`医院`)-[:概念包含]->(:`概念资源`:`服务器` {name: "服务器"}) 
        """

        cypher_create_functions = """CREATE (:`概念功能`:`提供床位` {name: "提供床位"})<-[:概念组合]-(`病房住宿`:`概念功能`:`病房住宿` {name: "病房住宿"})-[:概念组合]->(:`概念功能`:`住院登记` {name: "住院登记"})-[:概念依赖]->(`科室问诊`:`局部功能`:`科室问诊` {name: "科室问诊"})<-[:概念聚合]-(`医疗检测`:`局部功能`:`医疗检测` {name: "医疗检测"})-[:概念组合]->(`设备使用`:`概念功能`:`设备使用` {name: "设备使用"})<-[:概念组合]-(`医疗服务`:`概念功能`:`医疗服务` {name: "医疗服务"})-[:概念依赖]->(:`概念功能`:`医疗服务场所功能` {name: "医疗服务场所功能"}),
(`设备废弃`:`概念功能`:`设备废弃` {name: "设备废弃"})<-[:概念替换]-(`设备维护`:`概念功能`:`设备维护` {name: "设备维护"})<-[:概念互斥]-(`设备使用`)-[:概念依赖]->(:`概念功能`:`设备调度` {name: "设备调度"}),
(`设备使用`)-[:概念互斥]->(`设备废弃`),
(`设备维护`)-[:概念替换]->(:`概念功能`:`设备采购` {name: "设备采购"}),
(`医院挂号挂号`:`局部功能` {name: "挂号", process_type: "必选"})-[:概念聚合]->(`医院挂号_线下`:`概念功能`:`医院挂号_线下` {name: "医院挂号_线下"})-[:概念替代]->(`医院挂号_线上`:`概念功能`:`医院挂号_线上` {name: "医院挂号_线上"})<-[:概念聚合]-(`医院挂号挂号`)<-[:概念功能]-(`医院功能`:`概念功能`:`医院功能` {name: "医院功能"}),
(`医院挂号挂号`)<-[:依赖]-(`问诊引导`:`局部功能` {name: "问诊引导", process_type: "可选"})<-[:概念聚合]-(:`概念功能`:`问诊引导_线下` {name: "问诊引导_线下"})-[:概念替换]->(:`概念功能`:`问诊引导_线上` {name: "问诊引导_线上"})-[:概念聚合]->(`问诊引导`)<-[:概念聚合]-(`医院功能`),
(`科室问诊_线下`:`概念功能`:`科室问诊_线下` {name: "科室问诊_线下"})-[:概念替换]->(:`概念功能`:`科室问诊_线上` {name: "科室问诊_线上"})-[:概念聚合]->(`科室问诊`)<-[:概念聚合]-(`科室问诊_线下`),
(`科室问诊`)<-[:概念聚合]-(`科室功能`:`概念功能`:`科室功能` {name: "科室功能"})-[:概念聚合]->(:`概念功能`:`医疗诊断_线下` {name: "医疗诊断_线下"})-[:概念替换]->(:`概念功能`:`医疗诊断_线上` {name: "医疗诊断_线上"})<-[:概念聚合]-(`科室功能`)-[:概念聚合]->(`医疗检测_线下`:`概念功能`:`医疗检测_线下` {name: "医疗检测_线下"}),
(`科室问诊_线下`)-[:概念依赖]->(:`概念功能`:`问诊场所功能` {name: "问诊场所功能"}),
(`科室功能`)-[:概念聚合]->(`病房住宿`)-[:依赖]->(`护士值班`:`概念功能`:`护士值班` {name: "护士值班"})<-[:概念依赖]-(`医疗服务`)-[:概念依赖]->(`医生值班`:`概念功能`:`医生值班` {name: "医生值班"})<-[:概念依赖]-(`医疗检测`)-[:概念聚合]->(`医疗检测_线下`)-[:概念依赖]->(:`概念功能`:`医疗检测场所功能` {name: "医疗检测场所功能"}),
(`科室问诊`)-[:概念依赖]->(`医生值班`)<-[:概念聚合]-(`科室功能`)-[:概念聚合]->(`护士值班`),
(:`概念功能`:`人力调度` {name: "人力调度"})<-[:概念聚合]-(`医院功能`)-[:概念聚合]->(`科室功能`)-[:概念聚合]->(`医疗检测`),
(`医疗服务`)-[:概念依赖]->(:`概念功能`:`医疗技术使用` {name: "医疗技术使用"}),
(`医院挂号_线下`)-[:概念依赖]->(:`概念功能`:`服务大厅功能` {name: "服务大厅功能"})<-[:概念依赖]-(`医院挂号_线上`)-[:概念依赖]->(:`概念功能`:`网络服务` {name: "网络服务"}),
(:`概念功能`:`药店取药` {name: "药店取药"})"""

        self.graph.run(cypher_create_resources)
        self.graph.run(cypher_create_functions)
        # self.resource_dict[]
        node_matcher = NodeMatcher(self.graph)
        resources = list(node_matcher.match("概念资源"))
        functions = list(node_matcher.match("概念功能"))
        for res in resources:
            resource_name = res["name"]
            self.resources[resource_name] = res
        for fun in functions:
            function_name = fun["name"]
            self.functions[function_name] = fun
        print("break")

    def add_node2graph(self, node_name, *node_label, **node_property):
        if node_name not in self.nodes:
            node = Node(*node_label, name=node_name, **node_property)
            self.nodes[node_name] = node
        else:
            node = self.nodes[node_name]
        return node

    def add_relation2graph(self, source_node, relation_type, target_node, **relation_property):
        relation = Relationship(source_node, relation_type, target_node, **relation_property)
        self.relations.append(relation)
        return relation

    #
    def add_equipment_and_technology2department(self, department_name, sub_department_type):
        """
        :param department_name: 科室名称
        :param sub_department_type: 子部门名称，手术室，检测室两种
        :return: 医疗设备的集合，医学技术的集合
        """
        # 添加资源:维护人员
        self.maintenance_personnel_id += 1
        maintenance_personnel_name = "维护人员-" + str(self.maintenance_personnel_id)
        maintenance_personnel_node = self.add_resource2graph(prefix + "-设备科", maintenance_personnel_name, "维护人员",
                                                             working_time="8-18", resource_qos="high-quality")
        # 添加功能：设备维护
        equipment_maintenance_function = self.add_function2resource(maintenance_personnel_node,
                                                                    maintenance_personnel_name + "-设备维护", "设备维护")
        doctors_function = self.nodes[department_name + "-医生值班"]
        nurse_function = self.nodes[department_name + "-护士值班"]
        if sub_department_type == "手术室":
            function_type = "医疗服务"
        else:
            function_type = "医疗检测_线下"

        medical_equipments = set()
        medical_technology = set()
        for equipment_tec in self.equipment_tec_data[department_name]:
            (function_name, equip_and_tec), = equipment_tec.items()
            use_time = random.randint(20, 121)
            # 创建医疗服务/医疗检测节点
            function_node = self.add_node2graph(department_name + "-" + function_name + "-" + function_type,
                                                function_type, "实例功能",
                                                type="agent", working_time="0-23",
                                                max_volume=5, service_capacity=5,
                                                average_service_time=use_time,
                                                busy_degree="idle", availability="Available"
                                                )
            # 实例化
            self.add_relation2graph(self.functions[function_type], "实例化", function_node)
            # 将功能连接到资源
            # self.add_relation2graph(self.nodes[department_name], "拥有功能", function_node)
            # 科室功能包含医疗服务
            self.add_relation2graph(self.nodes[department_name + "-科室功能"], "聚合" + function_type, function_node)
            # 添加具体组合，医疗服务（检测）依赖医疗服务（检测）场所
            self.add_relation2graph(function_node, "依賴",
                                    self.nodes[department_name + "-" + sub_department_type + "-场所功能"],
                                    type="agent")
            self.add_relation2graph(function_node, "依赖",
                                    doctors_function,
                                    type="agent")
            self.add_relation2graph(function_node, "依赖",
                                    nurse_function,
                                    type="agent")

            for equip_name in equip_and_tec[0]:
                # 创建设备资源与功能节点
                equipment_node = self.add_node2graph(department_name + "-" + equip_name, "医疗设备", "实例资源",
                                                     type="agent", resource_qos="high-quality",
                                                     max_volume=5, service_capacity=5,
                                                     average_service_time=use_time,
                                                     busy_degree="idle", availability="Available"
                                                     )
                equipment_function_node = self.add_node2graph(department_name + "-" + equip_name + "-使用", "设备使用",
                                                              "实例功能", type="agent",
                                                              max_volume=5, service_capacity=5,
                                                              average_service_time=use_time,
                                                              busy_degree="idle", availability="Available"
                                                              )
                # 连接资源节点到父节点
                self.add_relation2graph(self.nodes[department_name], "拥有设备", equipment_node)
                # 连接资源节点和功能节点
                self.add_relation2graph(equipment_node, "拥有功能", equipment_function_node)
                # 实例化
                self.add_relation2graph(self.resources["医疗设备"], "实例化", equipment_node)
                self.add_relation2graph(self.functions["设备使用"], "实例化", equipment_function_node)
                # 添加具体的的依赖关系
                self.add_relation2graph(function_node, "依赖", equipment_function_node)
                # 维护人员维护设备
                self.add_relation2graph(maintenance_personnel_node, "维护设备", equipment_node)
                medical_equipments.add(equipment_node)

            for tec_name in equip_and_tec[1]:
                technology_node = self.add_node2graph(tec_name, "医疗技术", "实例资源", type="agent", resType="医疗技术",
                                                      working_time="0-23", resource_qos="high-quality",
                                                      max_volume=5, service_capacity=5,
                                                      average_service_time=use_time,
                                                      busy_degree="idle", availability="Available"
                                                      )
                technology_function_node = self.add_node2graph(department_name + "-" + tec_name + "-使用", "医疗技术使用",
                                                               "实例功能", type="agent",
                                                               max_volume=5, service_capacity=5,
                                                               average_service_time=use_time,
                                                               busy_degree="idle", availability="Available"
                                                               )
                # 连接资源节点到父节点
                self.add_relation2graph(self.nodes[department_name], "拥有技术", technology_node)
                # 连接资源节点和功能节点
                self.add_relation2graph(technology_node, "拥有功能", technology_function_node)

                # 实例化
                self.add_relation2graph(self.resources["医疗技术"], "实例化", technology_node)
                self.add_relation2graph(self.functions["医疗技术使用"], "实例化", technology_function_node)

                # 添加具体依赖关系
                self.add_relation2graph(function_node, "依赖", technology_function_node)
                medical_technology.add(technology_node)

            # equipment_node = self.add_node2graph(equipment, "设备", amount=1)
            # self.add_relation2graph(self.nodes[department_name], "拥有设备", equipment_node)
            # self.add_relation2graph(maintenance_personnel_node, '维护', equipment_node)

        return medical_technology, medical_equipments

    def add_technology2doctors(self, doctor_node, doctor_title, medical_technology):
        # 全部添加
        for tech in medical_technology:
            self.add_relation2graph(doctor_node, "掌握", tech)

    def add_equipment2doctors(self, doctor_node, doctor_title, medical_equipments):
        # 全部添加
        for equip in medical_equipments:
            self.add_relation2graph(doctor_node, "操作", equip)

    # 实例功能节点的名称和概念功能节点不一样，但label一样
    def add_department2graph(self, hospital_name, department_name, working_time, resource_qos,
                             max_volume, service_capacity, average_service_time):
        department_node = self.add_resource2graph(hospital_name, department_name, "科室", working_time=working_time,
                                                  resource_qos=resource_qos, max_volume=max_volume,
                                                  service_capacity=service_capacity,
                                                  busy_degree="idle", average_service_time=average_service_time,
                                                  availability="Available")
        department_function_node = self.add_function2resource(department_node, department_name + "-科室功能", "科室功能",
                                                              type="agent", working_time=working_time,
                                                              resource_qos=resource_qos, max_volume=max_volume,
                                                              service_capacity=service_capacity,
                                                              busy_degree="idle",
                                                              average_service_time=average_service_time,
                                                              availability="Available")
        self.add_function2graph(department_name + "-科室功能", department_name + "-科室问诊_线下", "科室问诊_线下", type="agent")
        self.add_function2graph(department_name + "-科室功能", department_name + "-科室问诊_线上", "科室问诊_线上", type="agent")
        self.add_function2graph(department_name + "-科室功能", department_name + "-医疗诊断_线下", "医疗诊断_线下", type="agent")
        self.add_function2graph(department_name + "-科室功能", department_name + "-医疗诊断_线上", "医疗诊断_线上", type="agent")
        return department_node, department_function_node

    def add_resource2graph(self, parent_node_name, resource_name, resource_type, **node_property):
        """
        该函数用于将资源节点添加到实例图谱，并连接到概念图谱
        """
        # 创建资源节点
        resource_node = self.add_node2graph(resource_name, resource_type, "实例资源", **node_property)
        # 将资源连接到概念图谱
        self.add_relation2graph(self.resources[resource_type], "实例化", resource_node)
        if parent_node_name != "None":
            p_node = self.nodes[parent_node_name]
            # 连接资源与父资源
            self.add_relation2graph(p_node, "包含" + resource_type, resource_node)
        return resource_node

    def add_function2graph(self, parent_node_name, function_name, function_type, **node_property):
        function_node = self.add_node2graph(function_name, function_type, "实例功能", **node_property)
        self.add_relation2graph(self.functions[function_type], "实例化", function_node)
        if parent_node_name != "None":
            p_node = self.nodes[parent_node_name]
            # 连接子功能与功能
            self.add_relation2graph(p_node, "聚合" + function_type, function_node)
        return function_node

    def add_function2resource(self, resource_node, function_name, function_type, **function_property):
        # 创建功能节点
        resource_function = self.add_node2graph(function_name, function_type, "实例功能", **function_property)
        # 将功能连接到资源
        self.add_relation2graph(resource_node, "拥有功能", resource_function)
        # 实例化功能
        self.add_relation2graph(self.functions[function_type], "实例化", resource_function)
        return resource_function
