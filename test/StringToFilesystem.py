from typing import Iterator, List, Dict, Tuple

from checker import WalkItem


def string_to_walk_iterator(string: str) -> Iterator[WalkItem]:
    return iter(string_to_filesystem(string))


def string_to_filesystem(string: str) -> List[WalkItem]:
    tree: Dict[str, Dict[str, List[str]]] = dict()
    for root, middle, leaf in _explode_filepaths(string):
        if leaf == '':
            tree.setdefault(root, {})
            tree[root].setdefault('dirs', [])
            tree[root]['dirs'].append(middle)

        subdir = f'{root}/{middle}'
        tree.setdefault(subdir, {})
        tree[subdir].setdefault('files', [])
        tree[subdir].setdefault('dirs', [])

        if leaf != '':
            tree[subdir]['files'].append(leaf)

    return _tree_to_list(tree)


def _explode_filepaths(string: str) -> List[Tuple[str, str, str]]:
    exploded = []
    for file_path in sorted(string.strip().splitlines()):
        rs = file_path.rsplit('/', 2)
        if len(rs) == 3:
            as_tuple = (rs[0], rs[1], rs[2])
            exploded.append(as_tuple)
    return exploded


def _tree_to_list(tree_dict) -> List[WalkItem]:
    nodes = []
    for key in tree_dict:
        files = sorted(tree_dict[key].get("files", []))
        dirs = sorted(tree_dict[key]["dirs"])
        node = (key, dirs, files)
        nodes.append(node)
    return nodes
