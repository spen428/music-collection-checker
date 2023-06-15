from typing import List, Dict, Tuple, Set, Iterable

from checker import WalkItem

MyTree = Dict[str, Dict[str, List[str]]]


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
    file_paths = _explode_filepaths(string, root_dir)

    tree = _create_empty_tree(file_paths)

    for root, middle, leaf in file_paths:
        leaf_is_directory = (leaf == '')
        if leaf_is_directory:
            tree[root]['dirs'].append(middle)
        else:
            tree[f'{root}/{middle}']['files'].append(leaf)

    _remove_items_above_root_dir(root_dir, tree)

    return _tree_to_list(tree)


def _create_empty_tree(exploded: List[Tuple[str, str, str]]) -> MyTree:
    tree: MyTree = dict()
    for root, middle, leaf in exploded:
        _make_subtrees(root, tree)
        _make_subtrees(f'{root}/{middle}', tree)
    return tree


def _remove_items_above_root_dir(root_dir: str, tree: MyTree):
    keys = list(tree.keys())
    for root in keys:
        if not root.startswith(root_dir[:-1]):
            del tree[root]


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


def _make_subtrees(root: str, tree: MyTree):
    tree.setdefault(root, {})
    tree[root].setdefault('files', [])
    tree[root].setdefault('dirs', [])


def _get_intermediate_dirs(lines: Iterable[str], root_dir: str) -> Set[str]:
    intermediate_dirs = set()
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
                intermediate_dirs.add(substr)
    return intermediate_dirs


def _tree_to_list(tree: MyTree) -> List[WalkItem]:
    nodes = []
    for key in tree:
        files = sorted(tree[key].get("files", []))
        dirs = sorted(tree[key]["dirs"])
        node = (key, dirs, files)
        nodes.append(node)
    return nodes
