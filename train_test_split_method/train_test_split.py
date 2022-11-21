import pandas as pd
import psycopg2
from collections import Counter, defaultdict
from graph_search_tools import bfs, components
from plotting_tools import get_histograms
import warnings

N_ROWS = 5_351_484
TRAIN_SIZE = 300_000
SMALL_COMPONENT_BORDER = 30
warnings.filterwarnings("ignore")


def get_data(_query, _config):
    """
    SQL query from local_db

    Each row contains two columns: array of paper ids and corresponding keyword_id.
    """
    conn = psycopg2.connect(_config)
    _keyword_links = pd.read_sql(_query, conn)
    conn.close()
    return _keyword_links


def graph_from_table(_table):
    """
    Make graph as list of sets.
    array index is a paper_id, array[paper_id] is a set of neighbours.

    """
    _graph = [set() for _ in range(N_ROWS)]
    for row in _table['links']:
        for i in range(len(row)):
            for j in range(i + 1, len(row)):
                _graph[row[i]].add(row[j])
                _graph[row[j]].add(row[i])
    return _graph


def train_test_split(_initial_graph, _connected_component):
    """
    Train test split via algorithm written in report.md

    """
    train_size = TRAIN_SIZE

    test_nums = set(bfs(graph, 2, _connected_component, lim=train_size))
    train_nums = _connected_component.difference(test_nums)

    print(f'Train sample size: {len(train_nums)}, test sample_size: {len(test_nums)}')

    all_data = []
    for _node in range(len(graph)):
        """
        Remove nodes from graph that are not in one component
        """
        if _node in _connected_component:
            all_data.append(len(graph[_node]))

    train_graph = defaultdict(list)
    test_graph = defaultdict(list)

    for i in train_nums:
        """
        Choose train
        """
        for _node in graph[i]:
            if _node in train_nums:
                train_graph[i].append(_node)

    for i in test_nums:
        """
        Choose test
        """
        for _node in graph[i]:
            if _node in test_nums:
                test_graph[i].append(_node)

    train_data_degrees = [len(train_graph[neighbours]) for neighbours in train_graph]
    test_data_degrees = [len(test_graph[neighbours]) for neighbours in test_graph]
    return {
        'train_data_degrees': train_data_degrees,
        'test_data_degrees': test_data_degrees,
        'all_data_degrees': all_data,
        'train_ids': train_graph.keys(),
        'test_ids': test_graph.keys()
    }


if __name__ == '__main__':
    with open('db_config.txt', 'r') as config_file:
        with open('sql_query.sql', 'r') as query_file:
            keyword_links = get_data(query_file.read(), config_file.read())

    graph = graph_from_table(keyword_links)
    graph_components = components(graph)
    main_color = 0
    main_amount = 0
    for color, amount in dict(Counter(graph_components)).items():
        if SMALL_COMPONENT_BORDER < amount:
            print(f'{color=}, amount of nodes of the color={amount}')
            if main_amount < amount:
                main_amount = amount
                main_color = color

    print(f"We see that most part of nodes are in one component. Color is {main_color}")

    connected_component = set()
    for node in graph_components:
        if graph_components[node] == main_color:
            connected_component.add(node)

    datasets = train_test_split(graph, connected_component)

    with open(r'outputs/train_paper_id.csv', 'w') as train_file:
        for paper_id in datasets['train_ids']:
            print(paper_id, file=train_file)

    with open(r'outputs/test_paper_id.csv', 'w') as test_file:
        for paper_id in datasets['test_ids']:
            print(paper_id, file=test_file)

    get_histograms(datasets['train_data_degrees'],
                   datasets['test_data_degrees'],
                   datasets['all_data_degrees'])
