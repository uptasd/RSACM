import random

from py2neo import Node, Relationship, Subgraph, NodeMatcher

prefix = "SYS-3rd-hospital"


# 检测功能独属于检验科，检验科的职能包含医疗检测，其他科室只包含医疗服务
# 要把1期临床研究中心去掉，它里面什么都没有
class HospitalKG:
    # 资源节点15个
    # hospital_resource = None
    # equipment_section_resource = None
    # personnel_section_resource = None
    # service_center_resource = None
    # department_resource = None
    # office_resource = None
    # maintenance_personnel_resource = None
    # operating_room_resource = None
    # examination_room_resource = None
    # outpatient_room_resource = None
    # sickbed_resource = None
    # doctor_resource = None
    # medical_equipment_resource = None
    # nurse_resource = None
    # sickroom_resource = None
    # 抽象功能节点18个
    hospital_treatment_function = None
    equipment_manage_function = None
    manpower_manage_function = None
    registration_function = None
    hospitalized_function = None
    clinic_function = None
    equipment_maintenance_function = None
    equipment_scrap_function = None
    equipment_purchase_function = None
    nurse_assist_function = None
    nurse_attendance_function = None
    nurse_daily_care_function = None
    doctor_attendance_function = None
    medical_test_function = None
    medical_technology_function = None
    sickroom_lodging_function = None
    medical_service_function = None

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
        self.init_graph()
        self.create_kg()

    def create_kg(self):
        for data in self.website_data:
            # data = self.website_data[4]
            department_name = data['Department_name']
            department_type = data["Department_type"]
            hospital_name = "SYS-3rd-hospital"
            # department_name = hospital_name+"-"+department_name
            # if department_name == "精神与神经疾病研究中心":
            #     # department_members = data['Department_member']
            #     # for member_name in department_members:
            #     #     if member_name not in self.nodes:
            #     #         member_node,_ = self.add_department2graph(hospital_name, department_name)
            #     #     else:
            #     #         member_node = self.nodes[department_name]
            #     #     self.add_relation2graph(department_node, "包含", member_node)
            #     continue
            # if department_name == "Ⅰ期临床研究中心":
            #     continue
            # if department_name == "骨科":
            #     continue
            # if department_name == "高血压达标中心":
            #     continue
            if len(data["Department_member"]) == 0:
                continue
            self.departmentCnt += 1
            working_time = "8-18"
            max_volume = len(data['Member_introduction'])
            service_capacity = max_volume
            average_service_time = random.randint(0, 10) + 11
            if "ICU" in department_name or "Emergency" in department_name:
                working_time = "0-7,19-23"
            resource_qos = "low-cost"
            if department_name in ["胃肠手术功能保护研究中心", "脊柱侧弯中心", "心脏康复中心", "产科", "肝胆外科", "Blood Transfusion", "Gynecology",
                                   "肝脏外科暨肝移植中心",
                                   "脑血管外科", "神经外科", "甲状腺、乳腺外科", "变态反应（过敏）学科", "胸痛中心", "卒中中心",
                                   "血管外科", "内科ICU", "外科ICU", "急诊医学科"]:
                resource_qos = "high-quality"
            department_node, department_function_node = self.add_department2graph(hospital_name, department_name,
                                                                                  working_time, resource_qos,
                                                                                  max_volume, service_capacity,
                                                                                  average_service_time)
            # department_function_node = self.add_function2resource(department_node, department_name + "-科室功能", "科室功能",
            #                                                       type="功能")
            self.add_relation2graph(self.nodes[prefix + "-hosp func"], "agg", department_function_node)
            # 门诊室资源和功能

            outpatient_department_node = self.add_resource2graph(department_name, department_name + "-Clinic", "Clinic",
                                                                 type="agent", working_time=working_time,
                                                                 complete_name="Clinic",
                                                                 resource_qos=resource_qos, max_volume=20,
                                                                 service_capacity=10, busy_degree="idle",
                                                                 average_service_time=average_service_time,
                                                                 availability="Available")
            outpatient_department_function = self.add_function2resource(outpatient_department_node,
                                                                        department_name + "-MCP func", "MCP func",
                                                                        type="agent", working_time=working_time,
                                                                        complete_name="medical consultation place "
                                                                                      "function",
                                                                        max_volume=20, service_capacity=10,
                                                                        busy_degree="idle",
                                                                        average_service_time=average_service_time,
                                                                        availability="Available")
            self.add_relation2graph(department_function_node, "agg", outpatient_department_function)
            self.add_relation2graph(self.nodes[department_name + "-cons offline"], "dep",
                                    outpatient_department_function)
            # 护士资源和功能
            ranint = random.randint(5, 10)
            nurse_node = self.add_resource2graph(department_name, department_name + "-nurse", "nurse",
                                                 type="agent", working_time=working_time, resource_qos=resource_qos,
                                                 complete_name="nurse",
                                                 max_volume=15, service_capacity=ranint,
                                                 average_service_time=average_service_time,
                                                 busy_degree="idle", availability="Available")
            nurse_function = self.add_function2resource(nurse_node, department_name + "-RN work", "RN work",
                                                        type="agent",
                                                        complete_name="nurse working",
                                                        working_time=working_time, max_volume=15,
                                                        service_capacity=ranint,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available")
            self.add_relation2graph(department_function_node, "agg", nurse_function)
            doctors_function = self.add_function2graph(department_name + "-Dept func", department_name + "-Dr work",
                                                       "Dr work", type="agent", complete_name="doctor working",
                                                       working_time=working_time,
                                                       max_volume=max_volume,
                                                       service_capacity=service_capacity,
                                                       average_service_time=average_service_time,
                                                       busy_degree="idle", availability="Available"
                                                       )
            if department_type == "Medical Technology Department" or department_type == "Special diagnosis and treatment platform":
                # 创建手术室资源与对应功能
                operating_room_node = self.add_resource2graph(department_name, department_name + "-O.R", "O.R",
                                                              complete_name="operating room",
                                                              type="agent", working_time="0-23",
                                                              resource_qos=resource_qos,
                                                              max_volume=10, service_capacity=10,
                                                              average_service_time=average_service_time,
                                                              busy_degree="idle", availability="Available")
                operating_room_function = self.add_function2resource(operating_room_node,
                                                                     department_name + "-MSP func", "MSP func",
                                                                     complete_name="Medical service place function",
                                                                     type="agent", working_time="0-23",
                                                                     max_volume=10, service_capacity=10,
                                                                     average_service_time=average_service_time,
                                                                     busy_degree="idle", availability="Available"
                                                                     )
                self.add_relation2graph(department_function_node, "聚合", operating_room_function)
                # 创建病房资源与对应功能
                nums = random.randint(20, 50)
                sickroom_node = self.add_resource2graph(department_name, department_name + "-sickroom", "sickroom",
                                                        complete_name="sickroom",
                                                        working_time="0-23", resource_qos=resource_qos,
                                                        max_volume=nums, service_capacity=nums,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available"
                                                        )
                sickroom_function = self.add_function2resource(sickroom_node, department_name + "-Ward accom",
                                                               "Ward accom",
                                                               type="agent", complete_name="Ward accommodation",
                                                               max_volume=nums, service_capacity=nums,
                                                               average_service_time=average_service_time,
                                                               busy_degree="idle", availability="Available"
                                                               )
                self.add_relation2graph(sickroom_function, "dep", nurse_function)
                self.add_relation2graph(department_function_node, "agg", sickroom_function)
                self.add_relation2graph(sickroom_function, "dep", self.nodes[prefix + "-hosp REG"])
                # 创建床位资源与对应功能

                sick_bed_node = self.add_resource2graph(department_name + "-sickroom",
                                                        department_name + "-sickroom" + "-sickbed", "sickbed",
                                                        type="agent", working_time="0-23", resource_qos=resource_qos,
                                                        max_volume=nums, service_capacity=nums,
                                                        average_service_time=average_service_time,
                                                        busy_degree="idle", availability="Available"
                                                        )
                sick_bed_function = self.add_function2resource(sick_bed_node,
                                                               department_name + "-sickroom" + "-sickbed" + "-bed supplys",
                                                               "bed supply", type="agent",
                                                               max_volume=nums, service_capacity=nums,
                                                               average_service_time=average_service_time,
                                                               busy_degree="idle", availability="Available"
                                                               )
                # 《病房住宿》依赖《提供床位》
                self.add_relation2graph(sickroom_function, "dep", sick_bed_function)
                medical_technology, medical_equipments = self.add_equipment_and_technology2department(department_name,
                                                                                                      "O.R")

            elif department_type == "clinical specialty":
                examination_room_node = self.add_resource2graph(department_name, department_name + "-exam room",
                                                                "exam room",
                                                                type="agent", working_time=working_time,
                                                                resource_qos=resource_qos,
                                                                max_volume=5, service_capacity=5,
                                                                average_service_time="120",
                                                                busy_degree="idle", availability="Available"
                                                                )
                examination_room_function = self.add_function2resource(examination_room_node,
                                                                       department_name + "MCP func",
                                                                       "MCP func", type="agent",
                                                                       max_volume=5, service_capacity=5,
                                                                       average_service_time="120",
                                                                       busy_degree="idle", availability="Available"
                                                                       )
                self.add_relation2graph(department_function_node, "agg", examination_room_function)
                medical_technology, medical_equipments = self.add_equipment_and_technology2department(department_name,
                                                                                                      "exam room")
            self.add_relation2graph(self.nodes[department_name + "-DX online"], "dep",
                                    self.nodes[department_name + "-Dr work"])
            self.add_relation2graph(self.nodes[department_name + "-DX online"], "dep",
                                    self.nodes[prefix + "-NET service"])

            self.add_relation2graph(self.nodes[department_name + "-DX offline"], "dep",
                                    self.nodes[department_name + "-Dr work"])
            self.add_relation2graph(self.nodes[department_name + "-DX offline"], "dep",
                                    self.nodes[department_name + "-MCP func"])

            self.add_relation2graph(self.nodes[department_name + "-cons online"], "dep",
                                    self.nodes[department_name + "-Dr work"])
            self.add_relation2graph(self.nodes[department_name + "-cons online"], "dep",
                                    self.nodes[prefix + "-NET service"])

            self.add_relation2graph(self.nodes[department_name + "-cons offline"], "dep",
                                    self.nodes[department_name + "-Dr work"])
            self.add_relation2graph(self.nodes[department_name + "-cons offline"], "dep",
                                    self.nodes[department_name + "-MCP func"])
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
                    doctors_title = "physician"
                if "导师资格" in doctors:
                    doctors_qualification = doctors["导师资格"]
                else:
                    doctors_qualification = "无"
                resource_qos = "low-cost"
                if "chief" in doctors_title:
                    resource_qos = "high-quality"
                if i >= len(member_introduction) / 2 and ("ICU" in department_name or "Emergency" in department_name):
                    working_time = "0-7,19-23"
                doctor_node = self.add_resource2graph(department_name, doctors_name + "-doctor", "doctor",
                                                      title=doctors_title,
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
                self.add_relation2graph(doctor_node, "has_func", self.nodes[department_name + "-Dr work"])

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
        hospital_node = self.add_node2graph(prefix, "hospital", "instance_res", resource_qos="high-quality",
                                            working_time="0-23",
                                            max_volume=1000, service_capacity=1000,
                                            average_service_time="60",
                                            busy_degree="idle", availability="Available"
                                            )
        equipment_section_node = self.add_resource2graph(prefix, prefix + "-ES department", "ES department",
                                                         working_time="8-18",
                                                         comeplete_name="Equipment Section department",
                                                         resource_qos="high-quality",
                                                         max_volume=20, service_capacity=15,
                                                         average_service_time="120",
                                                         busy_degree="idle", availability="Available"
                                                         )
        personnel_section_node = self.add_resource2graph(prefix, prefix + "-HR department", "HR department",
                                                         working_time="8-18",
                                                         complete_name="human resource department",
                                                         resource_qos="high-quality",
                                                         max_volume=20, service_capacity=15,
                                                         average_service_time="60",
                                                         busy_degree="idle", availability="Available"
                                                         )
        service_center_node = self.add_resource2graph(prefix, prefix + "-Service Hall", "Service Hall", type="agent",
                                                      working_time="0-23", resource_qos="high-quality",
                                                      average_service_time="5",
                                                      max_volume=500, service_capacity=500,
                                                      busy_degree="idle", availability="Available"
                                                      )
        pharmacy_node = self.add_resource2graph(prefix, prefix + "-pharmacy", "pharmacy", type="agent",
                                                working_time="0-23", resource_qos="high-quality",
                                                average_service_time="5",
                                                max_volume=500, service_capacity=500,
                                                busy_degree="idle", availability="Available"
                                                )
        server_node = self.add_resource2graph(prefix, prefix + "-server", "server", type="agent",
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
        hospital_func = self.add_function2resource(hospital_node, prefix + "-hosp func", "hosp func", type="agent",
                                                   complete_name="hospital function",
                                                   working_time="0-23",
                                                   max_volume=1000, service_capacity=1000,
                                                   average_service_time="60",
                                                   busy_degree="idle", availability="Available"
                                                   )
        registration_offline_func = self.add_function2resource(service_center_node, prefix + "-REG_offline",
                                                               "REG offline",
                                                               complete_name="hospital Registration offline",
                                                               type="agent", working_time="8-18",
                                                               max_volume=1000, service_capacity=1000,
                                                               average_service_time="5",
                                                               busy_degree="idle", availability="Available"
                                                               )
        registration_online_func = self.add_function2resource(service_center_node, prefix + "-REG online", "REG online",
                                                              complete_name="hospital Registration offline",
                                                              type="agent", working_time="0-23",
                                                              max_volume=1000, service_capacity=1000,
                                                              average_service_time="3",
                                                              busy_degree="idle", availability="Available")
        pharmacy_func = self.add_function2resource(pharmacy_node, prefix + "-sell medicine", "sell medicine",
                                                   type="agent", working_time="8-18",
                                                   max_volume=1000, service_capacity=1000,
                                                   average_service_time="5",
                                                   busy_degree="idle", availability="Available"
                                                   )
        network_func = self.add_function2resource(server_node, prefix + "-NET service", "NET service", type="agent",
                                                  complete_name="network service",
                                                  working_time="0-23",
                                                  max_volume=500, service_capacity=500,
                                                  average_service_time="1",
                                                  busy_degree="idle", availability="Available")
        # pass

        inquiry_guide_offline_func = self.add_function2resource(service_center_node, prefix + "-guide offline",
                                                                "guide offline",
                                                                type="agent", working_time="8-18",
                                                                max_volume=1000, service_capacity=1000,
                                                                average_service_time="5",
                                                                busy_degree="idle", availability="Available")
        inquiry_guide_online_func = self.add_function2resource(service_center_node, prefix + "-guide online",
                                                               "guide online",
                                                               type="agent", working_time="0-23",
                                                               average_service_time="2",
                                                               max_volume=1000, service_capacity=1000,
                                                               busy_degree="idle", availability="Available")
        hospitalized_func = self.add_function2resource(service_center_node, prefix + "-hosp REG", "hosp REG",
                                                       type="agent",
                                                       complete_name="hospitalization registration",
                                                       working_time="0-23",
                                                       average_service_time="3",
                                                       max_volume=1000, service_capacity=1000,
                                                       busy_degree="idle", availability="Available")

        # 添加关系
        self.add_relation2graph(hospital_func, "comb", registration_offline_func)
        self.add_relation2graph(hospital_func, "comb", registration_online_func)
        self.add_relation2graph(hospital_func, "comb", inquiry_guide_offline_func)
        self.add_relation2graph(hospital_func, "comb", inquiry_guide_online_func)
        self.add_relation2graph(hospital_func, "comb", hospitalized_func)
        self.add_relation2graph(hospital_func, "agg", pharmacy_func)
        self.add_relation2graph(registration_online_func, "dep", network_func)
        self.add_relation2graph(inquiry_guide_online_func, "dep", network_func)
        manpower_manage_func = self.add_function2resource(personnel_section_node, prefix + "-MP sched", "MP sched",
                                                          complete_name="Manpower scheduling",
                                                          working_time="0-23",
                                                          max_volume=200, service_capacity=200,
                                                          busy_degree="idle", availability="Available"
                                                          )
        equipment_manage_func = self.add_function2resource(equipment_section_node, prefix + "-Eqpt sched", "Eqpt sched",
                                                           complete_name="Equipment scheduling",
                                                           service_capacity=200,
                                                           busy_degree="idle", availability="Available")
        equipment_purchase_func = self.add_function2resource(equipment_section_node, prefix + "-Eqpt Purchase",
                                                             "Eqpt Purchase",
                                                             complete_name="Equipment Purchase",
                                                             service_capacity=200,
                                                             busy_degree="idle", availability="Available"
                                                             )
        equipment_scrap_func = self.add_function2resource(equipment_section_node, prefix + "-Eqpt scrap", "Eqpt scrap",
                                                          complete_name="Equipment scrapped",
                                                          service_capacity=200,
                                                          busy_degree="idle", availability="Available"
                                                          )

    def init_abstract_graph(self):
        cypher_create_resources = """CREATE (Clinic:`abs-resource`:Clinic {name: "Clinic"})<-[:work_in]-(nurse:`abs-resource`:nurse {name: "nurse"})<-[:Include]-(department:`abs-resource`:department {name: "department"})-[:Include]->(doctor:`abs-resource`:doctor {name: "doctor"})<-[:assist]-(nurse)-[:work]->(sickroom:`abs-resource`:sickroom {name: "sickroom"})<-[:manage]-(department)-[:Include]->(Clinic)<-[:work_in]-(doctor)-[:work_in]->(`exam room`:`abs-resource`:`exam room` {name: "exam room"})<-[:work_in]-(nurse)-[:work_in]->(`O.R`:`abs-resource`:`O.R` {name: "O.R"}),
(nurse)<-[:manage]-(`HR department`:`abs-resource`:`HR department` {name: "HR department"})<-[:Include]-(hospital:`abs-resource`:Hospital {name: "hospital"})-[:Include]->(`ES department`:`abs-resource`:`ES department` {name: "ES department"})-[:Include]->(office:`abs-resource`:office {name: "office"})<-[:Include]-(department)-[:Include]->(`medical equip`:`abs-resource`:`medical equip` {name: "medical equip"})<-[:operate]-(doctor)-[:work_in]->(`O.R`),
(`ES department`)-[:Include]->(`MT staff`:`abs-resource`:`MT staff` {name: "MT staff"})-[:maintain]->(`medical equip`)<-[:采购]-(`ES department`),
(`MT staff`)<-[:manage]-(`HR department`)-[:manage]->(doctor)-[:work_in]->(sickroom)-[:include]->(:`abs-resource`:sickbed {name: "sickbed"}),
(:`abs-resource`:`Service Hall` {name: "Service Hall"})<-[:Include]-(hospital)-[:Include]->(department)-[:Include]->(`O.R`),
(department)-[:Include]->(`exam room`),
(`HR department`)-[:include]->(office),
(doctor)-[:master]->(:`abs-resource`:`medical tech` {name: "medical tech"}),
(:`abs-resource`:pharmacy {name: "pharmacy"})<-[:Include]-(hospital)-[:Include]->(:`abs-resource`:server {name: "server"})"""

        cypher_create_functions = """CREATE (:`abs-function`:`bed supply` {name: "bed supply"})<-[:comb]-(`Ward accom`:`abs-function`:`Ward accom` {name: "Ward accom"})-[:comb]->(:`abs-function`:`hosp REG` {name: "hosp REG"})-[:dep]->(consultation:`abs-function`:consultation {name: "consultation"})<-[:agg]-(`Med check`:`abs-function`:`Med check` {name: "Med check"})-[:comb]->(`Eqpt work`:`abs-function`:`Eqpt work` {name: "Eqpt work"})<-[:comb]-(`Med service`:`abs-function`:`Med service` {name: "Med service"})-[:dep]->(:`abs-function`:`MSP func` {name: "MSP func"}),
(`Eqpt scrap`:`abs-function`:`devs scrap` {name: "Eqpt scrap"})<-[:rep]-(`Eqpt maintain`:`abs-function`:`Eqpt maintain` {name: "Eqpt maintain"})<-[:exc]-(`Eqpt work`)-[:dep]->(:`abs-function`:`Eqpt sched` {name: "Eqpt sched"}),
(`Eqpt work`)-[:exc]->(`Eqpt scrap`),
(`Eqpt maintain`)-[:rep]->(:`abs-function`:`Eqpt Purchase` {name: "Eqpt Purchase"}),
(registration:`abs-function`:registration {name: "registration"})-[:agg]->(:`abs-function`:`REG offline` {name: "REG offline"})-[:rep]->(`REG online`:`abs-function`:`REG online` {name: "REG online"})<-[:agg]-(registration)<-[:agg]-(`hosp func`:`abs-function`:`hosp func` {name: "hosp func"})-[:agg]->(:`abs-function`:`sell medicine` {name: "sell medicine"}),
(registration)<-[:dep]-(guide:`abs-function`:guide {name: "guide"})<-[:agg]-(:`abs-function`:`guide offline` {name: "guide offline"})-[:rep]->(:`abs-function`:guide_online {name: "guide online"})-[:agg]->(guide)<-[:agg]-(`hosp func`),
(`cons offline`:`abs-function`:`cons offline` {name: "cons offline"})-[:rep]->(:`abs-function`:`cons online` {name: "cons online"})-[:agg]->(consultation)<-[:agg]-(`cons offline`),
(consultation)<-[:agg]-(`Dept func`:`abs-function`:`Dept func` {name: "Dept func"})-[:comb]->(`DX offline`:`abs-function`:`DX offline` {name: "DX offline"})-[:rep]->(:`abs-function`:`DX online` {name: "DX online"})<-[:comb]-(`Dept func`)-[:agg]->(check_offline:`abs-function`:check_offline {name: "check_offline"}),
(`cons offline`)-[:dep]->(:`abs-function`:`MCP func` {name: "MCP func"})<-[:dep]-(`DX offline`),
(`Med service`)<-[:agg]-(`Dept func`)-[:agg]->(`Ward accom`)-[:dep]->(`RN work`:`abs-function`:`RN work` {name: "RN work"})<-[:dep]-(`Med service`)-[:dep]->(`Dr work`:`abs-function`:`Dr work` {name: "Dr work"})<-[:dep]-(`Med check`)-[:agg]->(check_offline)-[:dep]->(:`abs-function`:`MCP func` {name: "MCP func"}),
(consultation)-[:dep]->(`Dr work`)<-[:comb]-(`Dept func`)-[:agg]->(`RN work`),
(:`abs-function`:`MP sched` {name: "MP sched"})<-[:agg]-(`hosp func`)-[:agg]->(`Dept func`)-[:agg]->(`Med check`),
(`Med service`)-[:dep]->(:`abs-function`:`MT fun` {name: "MT fun"}),
(`REG online`)-[:dep]->(:`abs-function`:`NET service` {name: "NET service"})"""

        self.graph.run(cypher_create_resources)
        self.graph.run(cypher_create_functions)
        # self.resource_dict[]
        node_matcher = NodeMatcher(self.graph)
        resources = list(node_matcher.match("abs-resource"))
        functions = list(node_matcher.match("abs-function"))
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
        maintenance_personnel_name = "MT staff-" + str(self.maintenance_personnel_id)
        maintenance_personnel_node = self.add_resource2graph(prefix + "-ES department", maintenance_personnel_name,
                                                             "MT staff",
                                                             working_time="8-18", resource_qos="high-quality",
                                                             busy_degree="idle", availability="Available"
                                                             )
        # 添加功能：设备维护
        equipment_maintenance_function = self.add_function2resource(maintenance_personnel_node,
                                                                    maintenance_personnel_name + "-Eqpt maintain",
                                                                    "Eqpt maintain",
                                                                    working_time="8-18", resource_qos="high-quality",
                                                                    busy_degree="idle", availability="Available"
                                                                    )
        doctors_function = self.nodes[department_name + "-Dr work"]
        nurse_function = self.nodes[department_name + "-RN work"]
        place_fun = "MSP func"
        if sub_department_type == "O.R":
            function_type = "Med service"
        else:
            function_type = "check_offline"
            place_fun = "MCP func"

        medical_equipments = set()
        medical_technology = set()
        for equipment_tec in self.equipment_tec_data[department_name]:
            (function_name, equip_and_tec), = equipment_tec.items()
            # 创建医疗服务/医疗检测节点
            function_node = self.add_node2graph(department_name + "-" + function_name + "-" + function_type,
                                                function_type, "instance_res",
                                                type="agent", working_time="0-23",
                                                busy_degree="idle", availability="Available")
            # 实例化
            self.add_relation2graph(self.functions[function_type], "Instantiate", function_node)
            # 将功能连接到资源
            # self.add_relation2graph(self.nodes[department_name], "拥有功能", function_node)
            # 科室功能包含医疗服务
            self.add_relation2graph(self.nodes[department_name + "-Dept func"], "agg" + function_type, function_node)
            # 添加具体组合，医疗服务（检测）依赖医疗服务（检测）场所
            self.add_relation2graph(function_node, "dep", self.nodes[department_name + "-" + place_fun])
            self.add_relation2graph(function_node, "dep", doctors_function)
            self.add_relation2graph(function_node, "dep", nurse_function, type="agent")

            for equip_name in equip_and_tec[0]:
                # 创建设备资源与功能节点
                equipment_node = self.add_node2graph(department_name + "-" + equip_name, "medical equip",
                                                     "instance_res",
                                                     type="agent", resource_qos="high-quality",
                                                     max_volume=10, service_capacity=10,
                                                     busy_degree="idle", availability="Available"
                                                     )
                equipment_function_node = self.add_node2graph(department_name + "-" + equip_name + "-working",
                                                              "Eqpt work",
                                                              "instance_res", type="agent",
                                                              max_volume=10, service_capacity=10,
                                                              average_service_time="30",
                                                              busy_degree="idle", availability="Available"
                                                              )
                # 连接资源节点到父节点
                self.add_relation2graph(self.nodes[department_name], "has_equip", equipment_node)
                # 连接资源节点和功能节点
                self.add_relation2graph(equipment_node, "has_func", equipment_function_node)
                # 实例化
                self.add_relation2graph(self.resources["medical equip"], "instance_res", equipment_node)
                self.add_relation2graph(self.functions["Eqpt work"], "instance_res", equipment_function_node)
                # 添加具体的的依赖关系
                self.add_relation2graph(function_node, "dep", equipment_function_node)
                # 维护人员维护设备
                self.add_relation2graph(maintenance_personnel_node, "maintain", equipment_node)
                medical_equipments.add(equipment_node)

            for tec_name in equip_and_tec[1]:
                technology_node = self.add_node2graph(tec_name, "medical tech", "instance_res", type="agent",
                                                      resource_qos="high-quality",
                                                      max_volume=10, service_capacity=10,
                                                      busy_degree="idle", availability="Available")
                technology_function_node = self.add_node2graph(department_name + "-" + tec_name + "-working", "MT fun",
                                                               "instance_res", type="agent",
                                                               complete_name="medical tech function",
                                                               average_service_time="30",
                                                               max_volume=10, service_capacity=10,
                                                               busy_degree="idle", availability="Available"
                                                               )
                # 连接资源节点到父节点
                self.add_relation2graph(self.nodes[department_name], "has_tec", technology_node)
                # 连接资源节点和功能节点
                self.add_relation2graph(technology_node, "has_func", technology_function_node)

                # 实例化
                self.add_relation2graph(self.resources["medical tech"], "Instantiate", technology_node)
                self.add_relation2graph(self.functions["MT fun"], "Instantiate", technology_function_node)

                # 添加具体依赖关系
                self.add_relation2graph(function_node, "dep", technology_function_node)
                medical_technology.add(technology_node)

            # equipment_node = self.add_node2graph(equipment, "设备", amount=1)
            # self.add_relation2graph(self.nodes[department_name], "拥有设备", equipment_node)
            # self.add_relation2graph(maintenance_personnel_node, '维护', equipment_node)

        return medical_technology, medical_equipments

    def add_technology2doctors(self, doctor_node, doctor_title, medical_technology):
        # 全部添加
        for tech in medical_technology:
            self.add_relation2graph(doctor_node, "master", tech)

    def add_equipment2doctors(self, doctor_node, doctor_title, medical_equipments):
        # 全部添加
        for equip in medical_equipments:
            self.add_relation2graph(doctor_node, "operate", equip)

    # 实例功能节点的名称和概念功能节点不一样，但label一样
    def add_department2graph(self, hospital_name, department_name, working_time, resource_qos,
                             max_volume, service_capacity, average_service_time):
        department_node = self.add_resource2graph(hospital_name, department_name, "department",
                                                  working_time=working_time,
                                                  resource_qos=resource_qos, max_volume=max_volume,
                                                  service_capacity=service_capacity,
                                                  busy_degree="idle", average_service_time=average_service_time,
                                                  availability="Available")
        department_function_node = self.add_function2resource(department_node, department_name + "-Dept func",
                                                              "Dept func", Complete_name="department function",
                                                              type="agent", working_time=working_time,
                                                              resource_qos=resource_qos, max_volume=max_volume,
                                                              service_capacity=service_capacity,
                                                              busy_degree="idle",
                                                              average_service_time=average_service_time,
                                                              availability="Available")
        self.add_function2graph(department_name + "-Dept func", department_name + "-cons offline", "cons offline",
                                type="agent", Complete_name="consultation offline function", working_time=working_time,
                                resource_qos=resource_qos, max_volume=max_volume,
                                service_capacity=service_capacity,
                                busy_degree="idle",
                                average_service_time=average_service_time,
                                availability="Available"
                                )
        self.add_function2graph(department_name + "-Dept func", department_name + "-cons online", "cons online",
                                type="agent", Complete_name="consultation online function",
                                resource_qos=resource_qos, max_volume=max_volume,
                                service_capacity=service_capacity,
                                busy_degree="idle",
                                average_service_time=average_service_time,
                                availability="Available"
                                )
        self.add_function2graph(department_name + "-Dept func", department_name + "-DX offline", "DX offline",
                                type="agent", Complete_name="diagnosis offline function",
                                resource_qos=resource_qos, max_volume=max_volume,
                                service_capacity=service_capacity,
                                busy_degree="idle",
                                average_service_time=average_service_time,
                                availability="Available")
        self.add_function2graph(department_name + "-Dept func", department_name + "-DX online", "DX online",
                                type="agent", Complete_name="diagnosis online function",
                                resource_qos=resource_qos, max_volume=max_volume,
                                service_capacity=service_capacity,
                                busy_degree="idle",
                                average_service_time=average_service_time,
                                availability="Available")
        return department_node, department_function_node

    def add_resource2graph(self, parent_node_name, resource_name, resource_type, **node_property):
        """
        该函数用于将资源节点添加到实例图谱，并连接到概念图谱
        """
        # 创建资源节点
        resource_node = self.add_node2graph(resource_name, resource_type, "instance_res", **node_property)
        # 将资源连接到概念图谱
        self.add_relation2graph(self.resources[resource_type], "Instantiate", resource_node)
        if parent_node_name != "None":
            p_node = self.nodes[parent_node_name]
            # 连接资源与父资源
            self.add_relation2graph(p_node, "include" + resource_type, resource_node)
        return resource_node

    def add_function2graph(self, parent_node_name, function_name, function_type, **node_property):
        function_node = self.add_node2graph(function_name, function_type, "instance_func", **node_property)
        self.add_relation2graph(self.functions[function_type], "Instantiate", function_node)
        if parent_node_name != "None":
            p_node = self.nodes[parent_node_name]
            # 连接子功能与功能
            self.add_relation2graph(p_node, "agg" + function_type, function_node)
        return function_node

    def add_function2resource(self, resource_node, function_name, function_type, **function_property):
        # 创建功能节点
        resource_function = self.add_node2graph(function_name, function_type, "instance_func", **function_property)
        # 将功能连接到资源
        self.add_relation2graph(resource_node, "has_func", resource_function)
        # 实例化功能
        self.add_relation2graph(self.functions[function_type], "Instantiate", resource_function)
        return resource_function
