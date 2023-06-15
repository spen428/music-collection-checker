from typing import List, Dict, Tuple

from checker import WalkItem


def ensure_single_trailing_slash(s: str):
    return s.rstrip('/') + '/'


def string_to_filesystem(string: str, root_dir: str) -> List[WalkItem]:
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
    :param root_dir: the top of the directory tree, e.g. ``root/``
    :return: a list of 3-tuples of the form (dirpath, dirnames, filenames)
    """
    root_dir = ensure_single_trailing_slash(root_dir)
    tree: Dict[str, Dict[str, List[str]]] = dict()
    for root, middle, leaf in _explode_filepaths(string, root_dir):
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


def _explode_filepaths(string: str, root_dir: str) -> List[Tuple[str, str, str]]:
    lines = string.strip().splitlines()
    intermediate_dirs = _get_intermediate_dirs(lines, root_dir)

    file_paths = sorted(list({*lines, *intermediate_dirs}))
    exploded = []
    for file_path in file_paths:
        rs = file_path.rsplit('/', 2)
        if len(rs) == 3:
            as_tuple = (rs[0], rs[1], rs[2])
            exploded.append(as_tuple)
    return exploded


def _get_intermediate_dirs(lines: List[str], root_dir: str) -> List[str]:
    intermediate_dirs = []
    for line in lines:
        index = 0
        while True:
            index = line.find('/', index) + 1
            if index == 0:
                break
            substr = line[0:index]
            if substr == root_dir:
                continue
            if substr.startswith(root_dir):
                intermediate_dirs.append(substr)
    return intermediate_dirs


def _tree_to_list(tree_dict) -> List[WalkItem]:
    nodes = []
    for key in tree_dict:
        files = sorted(tree_dict[key].get("files", []))
        dirs = sorted(tree_dict[key]["dirs"])
        node = (key, dirs, files)
        nodes.append(node)
    return nodes
