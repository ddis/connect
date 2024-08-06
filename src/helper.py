def collect_tree_keys(tree_map, flat_map):
    if not type(tree_map) is dict:
        return
    for k in tree_map.keys():
        if k == 'units':
            continue
        unique_user_name = k + '_'.join(tree_map[k]['units'])
        flat_map[unique_user_name] = {}
        flat_map[unique_user_name]['user_name'] = k
        flat_map[unique_user_name]['units'] = tree_map[k]['units']
        collect_tree_keys(tree_map[k], flat_map)