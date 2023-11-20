import json

from py2neo import Graph

from neo4jGraph.src.en.construct_kg_en import HospitalKG


# from neo4jGraph.src.construct_kg2 import HospitalKG

def load_json(file_path="../asset/SYS-3rd.json"):
    with open(file_path, encoding='UTF-8', errors='ignore') as json_file:
        data = json.load(json_file)
    return data


def connect_db():
    hospital_graph = Graph('http://localhost:7474/db/data/hospital', auth=("neo4j", "epc401100"))
    return hospital_graph


if __name__ == '__main__':
    website_data = load_json("../../asset/hospital_raw/SYS-3rd-en.json")
    # equipment_data = load_json("../../asset/equipment.json")
    equipment_tec_data = load_json("../../asset/equip_tec-en.json")
    graph = connect_db()
    # init_graph(graph)
    # create_department_doctors(json_data, graph)
    kg = HospitalKG(website_data, equipment_tec_data, graph)
