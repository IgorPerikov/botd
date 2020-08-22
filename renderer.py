from graphviz import Graph

from scraper import BotdData


def render(botd_data: BotdData):
    graph = Graph('botd graph', engine='neato', format='png', graph_attr={'splines': 'curved', 'scale': '1.05'})

    for user in botd_data.get_users():
        graph.node(user, user)

    max_affinity = botd_data.get_max_affinity() + 2

    for edge_name, common_bands in botd_data.get_mapping().items():
        split = edge_name.split('|')
        graph.edge(split[0], split[1], len=str(max_affinity - common_bands))

    graph.render('botd.gv', format='png')
