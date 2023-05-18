from random import randint

NODE_NUM = 5
CONNECT_PERCENT = 20

STEP_PRINTS = True


def generate_nodes(node_num, connect_percent, to_print=False):
    addresses = set(['.'.join([str(randint(0, 255)),
                               str(randint(0, 255)),
                               str(randint(0, 255)),
                               str(randint(0, 255))]) for _ in range(node_num)])

    generated_nodes = {address: {} for address in addresses}
    for address in addresses:
        for another_address in addresses:
            if address != another_address and randint(0, 99) < connect_percent:
                generated_nodes[address][another_address] = (another_address, 1)
                generated_nodes[another_address][address] = (address, 1)

    if to_print:
        print('Start table of connections:')
        print(f'{"[Source IP]":20} {"[Connections]"}')
        for address in addresses:
            print(f'{address:20} [{", ".join(generated_nodes[address])}]')
        print()

    return generated_nodes


def console_print(string, nodes):
    for node in nodes:
        print(string, node, 'table:')
        print(f'{"[Source IP]":20} {"[Destination IP]":20} {"[Next Hop]":20} {"[Metric]"}')
        if len(nodes[node]) == 0:
            print(f'{"-":20} {"-":20} {"-":20} {"-"}')
        for connection in nodes[node]:
            print(f'{node:20} {connection:20} {nodes[node][connection][0]:20} {nodes[node][connection][1]}')
        print()


nodes = generate_nodes(NODE_NUM, CONNECT_PERCENT, STEP_PRINTS)

modified = True
step = 0

while modified:
    if STEP_PRINTS:
        step_string = f'Simulation step {step} of router' if step != 0 else 'Start state (step 0) of router'
        console_print(step_string, nodes)
        step += 1

    modified = False
    for node in nodes:
        for neighbour_node in nodes[node]:
            if nodes[node][neighbour_node][1] != 1:
                continue
            for connection in nodes[node]:
                if neighbour_node != connection and \
                        (connection not in nodes[neighbour_node] or
                         nodes[node][connection][1] + 1 < nodes[neighbour_node][connection][1]):
                    nodes[neighbour_node][connection] = (node, nodes[node][connection][1] + 1)
                    modified = True

step_string = f'(step {step}) ' if STEP_PRINTS else ''
console_print(f'Final state {step_string}of router', nodes)
