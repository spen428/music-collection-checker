import os
from typing import List, Dict, Tuple

from checker import WalkItem


def string_to_filesystem(string: str) -> List[WalkItem]:
    """
    Transform a textual representation of a directory structure into a list of tuples, emulating what ``os.walk()``
    would return. Directories **must** end with a slash, else they will be treated as files.

    |
    | **Example input:**
    |
    | ``root/``
    | ``root/file.txt``
    | ``root/subdir/``
    | ``root/subdir/emptydir/``
    | ``root/subdir/file.txt``
    |
    | **Example output:**
    |
    | ``[ ( 'root', [ 'subdir' ], [ 'file.txt' ] ), ( 'root/subdir', [ 'emptydir' ], [ 'file.txt' ] ) ]``

    .. seealso:: `os.walk() <https://docs.python.org/3/library/os.html#os.walk>`_

    :param string: a textual representation of a filesystem
    :return: a list of 3-tuples of the form (dirpath, dirnames, filenames)
    """
    tree: Dict[str, Dict[str, List[str]]] = dict()
    for root, middle, leaf in _explode_filepaths(string):
        if leaf == '':
            _make_subtree(root, tree)
            tree[root]['dirs'].append(middle)

        subdir = f'{root}/{middle}'
        _make_subtree(subdir, tree)

        if leaf != '':
            tree[subdir]['files'].append(leaf)

    return _tree_to_list(tree)


def _make_subtree(root, tree):
    tree.setdefault(root, {})
    tree[root].setdefault('files', [])
    tree[root].setdefault('dirs', [])


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
