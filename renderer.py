from graphviz import Graph

from scraper import BotdData


def render(botd_data: BotdData):
    graph = Graph('botd graph', engine='neato', format='png',
                  graph_attr={'splines': 'curved', 'scale': '1'})

    for user in botd_data.users:
        graph.node(user, user)

    max_connection = botd_data.get_max_connection()

    for edge_name, connection in botd_data.mapping.items():
        (user1, user2) = edge_name.split('|')
        edge_len = str(max_connection - connection)
        if connection == BotdData.DEFAULT_CONNECTION:
            graph.edge(user1, user2, len=edge_len, color='transparent')
        else:
            graph.edge(user1, user2, len=edge_len)

    graph.render('botd.gv', format='png')
