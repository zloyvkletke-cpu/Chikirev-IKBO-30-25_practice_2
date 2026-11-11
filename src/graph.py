from collections import deque
from typing import Dict, List, Callable, Tuple

def build_graph(
    root_package: str, 
    root_version: str,
    fetch_func: Callable[[str, str], List[Tuple[str, str]]], 
    max_depth: int, 
    filter_substring: str
) -> Dict[str, List[str]]:
    """Строит граф зависимостей с помощью BFS без рекурсии."""
    graph = {}
    queue = deque([(root_package, root_version, 0)])
    visited = {root_package}

    while queue:
        current_pkg, current_ver, current_depth = queue.popleft()
        
        if current_depth >= max_depth:
            graph[current_pkg] = []
            continue

        raw_deps = fetch_func(current_pkg, current_ver)
        
        filtered_deps = []
        for dep_name, dep_ver in raw_deps:
            if filter_substring and filter_substring.lower() in dep_name.lower():
                continue
            if dep_name not in [d[0] for d in filtered_deps]:
                filtered_deps.append((dep_name, dep_ver))
                
        graph[current_pkg] = [d[0] for d in filtered_deps]

        for dep_name, dep_ver in filtered_deps:
            if dep_name not in visited:
                visited.add(dep_name)
                queue.append((dep_name, dep_ver, current_depth + 1))
                
    return graph

def get_load_order(graph: Dict[str, List[str]]) -> List[str]:
    """Топологическая сортировка (без изменений)."""
    in_degree = {node: 0 for node in graph}
    for node, deps in graph.items():
        for dep in deps:
            if dep not in in_degree:
                in_degree[dep] = 0
            in_degree[dep] += 1

    queue = deque([node for node, degree in in_degree.items() if degree == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        
        for dep in graph.get(node, []):
            in_degree[dep] -= 1
            if in_degree[dep] == 0:
                queue.append(dep)

    return list(reversed(order))