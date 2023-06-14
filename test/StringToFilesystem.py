from typing import Iterator, List, Dict

from checker import WalkItem


def string_to_walk_iterator(string: str) -> Iterator[WalkItem]:
    return iter(string_to_filesystem(string))


def string_to_filesystem(string: str) -> List[WalkItem]:
    exploded_filepaths = [x.rsplit('/', 2) for x in sorted(string.strip().splitlines())]
    tree: Dict[str, Dict[str, List[str]]] = dict()
    for filepath_segments in exploded_filepaths:
        root = filepath_segments[0]
        middle = filepath_segments[1]

        if len(filepath_segments) == 2 and middle == '':
            continue

        leaf = filepath_segments[2]
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


def _tree_to_list(tree_dict) -> List[WalkItem]:
    nodes = []
    for key in tree_dict:
        files = sorted(tree_dict[key].get("files", []))
        dirs = sorted(tree_dict[key]["dirs"])
        node = (key, dirs, files)
        nodes.append(node)
    return nodes
