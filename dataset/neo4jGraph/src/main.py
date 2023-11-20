import json

from py2neo import Graph

from neo4jGraph.src.generator.construct_kg import HospitalKG


# from neo4jGraph.src.construct_kg2 import HospitalKG

def load_json(file_path):
    with open(file_path, encoding='UTF-8', errors='ignore') as json_file:
        data = json.load(json_file)
    return data


def connect_db():
    hospital_graph = Graph('', auth=("", ""))
    return hospital_graph


if __name__ == '__main__':
    website_data = load_json("../asset/hospital_raw/SYS-3rd.json")
    # equipment_data = load_json("../asset/equipment.json")
    equipment_tec_data = load_json("../asset/equipment_technology/equip_tec.json")
    graph = connect_db()
    # init_graph(graph)
    # create_department_doctors(json_data, graph)
    kg = HospitalKG(website_data, equipment_tec_data, graph)
