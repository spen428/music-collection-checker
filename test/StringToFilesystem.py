from typing import Iterator, List

from checker import WalkItem


def string_to_walk_iterator(string: str) -> Iterator[WalkItem]:
    return iter(string_to_walk_list(string))


def string_to_walk_list(string: str) -> List[WalkItem]:
    tree = [x.rsplit('/', 2) for x in sorted(string.strip().splitlines())]
    tree_dict = {}
    for item in tree:
        root = item[0]
        middle = item[1]

        tree_dict.setdefault(root, {})
        tree_dict[root].setdefault('files', [])
        tree_dict[root].setdefault('dirs', [])

        if len(item) == 2 and middle == '':
            continue

        leaf = item[2]
        if leaf == '':
            tree_dict[root].setdefault('dirs', [])
            tree_dict[root]['dirs'].append(middle)

        root += f'/{middle}'
        tree_dict.setdefault(root, {})
        tree_dict[root].setdefault('files', [])
        tree_dict[root].setdefault('dirs', [])
        if leaf != '':
            tree_dict[root]['files'].append(leaf)

    nodes: List[WalkItem] = []
    for key in tree_dict:
        files = sorted(tree_dict[key]["files"])
        dirs = sorted(tree_dict[key]["dirs"])
        node = (key, dirs, files)
        nodes.append(node)

    print('OUTPUT:')
    print('[')
    for node in nodes:
        print(f'  {node}')
    print(']')

    return nodes


def remove_from_tree(tree, node):
    (root, dirs, files) = node
    for x in dirs:
        tree.remove([root, x, ''])
    for x in files:
        tree.remove([root, *x])


def recurse(file, children):
    dirs = []
    files = []
    for x in children:
        if x[2] == '':
            dirs.append(x[1])
        elif len(x) == 2:
            files.append(x[1:])

    return file[0], dirs, files
