import json

from py2neo import Graph


def save2json(json_data, json_name):
    with open(json_name, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


def save_json(json_data, json_name):
    json_str = json_data
    if isinstance(json_data, dict):
        json_str = json.dumps(json_data, indent=4, ensure_ascii=False).encode('utf8')
    with open(json_name, 'w', encoding='utf-8') as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


class Generator:

    def __init__(self, graph_database, authorization):
        self.graph_database = graph_database
        self.authorization = authorization
        self.hospital_graph = Graph(self.graph_database, auth=self.authorization)
        self.function_agents = dict()
        self.resource_agents = dict()

    def connect_db(self):
        self.hospital_graph = Graph(self.graph_database, auth=self.authorization)

    def bfs(self):
        hospital_function_cypher = "MATCH (m{name:'中山大学第三附属医院-医院功能'}) RETURN m"
        hospital_function_agent = self.hospital_graph.run(hospital_function_cypher).data()[0]
        # node_matcher = NodeMatcher(self.hospital_graph)
        # hospital_function_agent = node_matcher.match(name="中山大学第三附属医院").first()
        agents_stack = list()
        agents_stack.append(hospital_function_agent)
        while agents_stack:
            agent = agents_stack.pop()
            agent_name = agent['m']['name']
            if agent_name in self.function_agents:
                continue
            self.function_agents[agent_name] = dict()
            dep_agents, agg_agents, res_agents = self.get_nei(agent_name)
            dep_agent_names = self.add_nei2agent(agent_name, dep_agents, "dep_agents")
            agg_agent_names = self.add_nei2agent(agent_name, agg_agents, "agg_agents")
            res_agent_names = self.add_nei2agent(agent_name, res_agents, "res_agents")
            agents_stack.extend(dep_agents)
            agents_stack.extend(agg_agents)
            if "医生值班" in agent_name:
                i = 0
                working_time = "8-18"
                for res_agent in res_agents:
                    name = res_agent['m']['name']
                    if name in self.resource_agents:
                        continue
                    self.resource_agents[name] = dict()
                    if i >= len(res_agents) / 2 and ("ICU" in agent_name or "急诊" in agent_name):
                        working_time = "0-7,19-23"
                    doctor_title = res_agent['m']['title']
                    if "主任" in doctor_title:
                        resource_type = "high-quality"
                    resource_qos = res_agent['m']['resource_qos']
                    self.resource_agents[name]['serviceNum'] = 1
                    self.resource_agents[name]["working_time"] = working_time
                    self.resource_agents[name]['resourceType'] = resource_qos
                    i += 1
            else:
                working_time = "0-23"
                for res_agent in res_agents:
                    name = res_agent['m']['name']
                    if name in self.resource_agents:
                        continue

                    res_type = ""
                    if "resType" in res_agent['m']:
                        res_type = res_agent['m']['resType']
                    self.resource_agents[name] = dict()
                    resource_type = "low-cost"
                    if "医生" in name:
                        pass
                        # doctor_title = res_agent['m']['title']
                        # if "主任" in doctor_title:
                        #     resource_type = "high-quality"
                        # self.resource_agents[name]['serviceNum'] = 1
                    elif res_type == "医疗技术":
                        self.resource_agents[name]['serviceNum'] = 999
                    else:
                        self.resource_agents[name]['serviceNum'] = 10
                    resource_qos = res_agent['m']['resource_qos']
                    self.resource_agents[name]['resourceType'] = resource_qos
                    self.resource_agents[name]["working_time"] = working_time
        assert_cypher = """MATCH (m{type:"agent"}) return m"""
        datas = self.hospital_graph.run(assert_cypher).data()
        for data in datas:
            agent_name = data['m']['name']
            if agent_name not in self.function_agents and agent_name not in self.resource_agents:
                print(agent_name)
        return self.function_agents, self.resource_agents

    def get_nei(self, node_name):
        search_dep_agents_cypher = "MATCH(p{name:'" + node_name + "'}) -[r]->(m{type:'agent'}) " \
                                                                  "where type(r)=~'依赖.*' return m"
        search_agg_agents_cypher = "MATCH(p{name:'" + node_name + "'}) -[r]->(m{type:'agent'})" \
                                                                  "where type(r)=~'聚合.*' return m"
        search_res_agents_cypher = "MATCH(p{name:'" + node_name + "'}) <-[r:`拥有功能`]-(m{type:'agent'}) return m"
        dep_agents = self.hospital_graph.run(search_dep_agents_cypher).data()
        agg_agents = self.hospital_graph.run(search_agg_agents_cypher).data()
        res_agents = self.hospital_graph.run(search_res_agents_cypher).data()
        return dep_agents, agg_agents, res_agents

    def add_nei2agent(self, agent_name, neighbors, neighbors_type):
        neighbor_list = list()
        for neighbor in neighbors:
            neighbor_list.append(neighbor['m']['name'])
        self.function_agents[agent_name][neighbors_type] = neighbor_list
        return neighbor_list


if __name__ == '__main__':
    database = ''
    auth = ("", "")
    x = Generator(database, auth)
    fun, res = x.bfs()
    agent_dir = "../../asset/agents/output/"
    save2json(fun, agent_dir + "function_agents.json")
    save2json(res, agent_dir + "resource_agents.json")
    # x = {"a": "一"}
    # save2json(x, "data.json")
