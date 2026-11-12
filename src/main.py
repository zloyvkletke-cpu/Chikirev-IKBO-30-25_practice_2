import argparse
from cli import parse_args, print_config
from fetcher import fetch_from_nuget, fetch_from_test_file
from graph import build_graph, get_load_order
from visualizer import generate_mermaid, save_to_png

# Константы для этапов (избавляемся от магических чисел 1-5)
STAGE_1 = 1
STAGE_2 = 2
STAGE_3 = 3
STAGE_4 = 4
STAGE_5 = 5

def run_stage_1(args: argparse.Namespace) -> None:
    print_config(args)

def run_stage_2(args: argparse.Namespace, fetch_func) -> None:
    deps = fetch_func(args.package, args.version)
    print(f"Прямые зависимости {args.package}:")
    for dep_name, dep_ver in deps:
        print(f"- {dep_name} (версия: {dep_ver})")

def run_stage_3_and_4(args: argparse.Namespace, graph: dict) -> None:
    if args.stage == STAGE_3:
        print("Построенный граф (Список смежности):")
        for node, deps in graph.items():
            print(f"{node} -> {deps}")
    elif args.stage == STAGE_4:
        order = get_load_order(graph)
        if len(order) != len(graph):
            print("Внимание: в графе обнаружены циклы!")
        print("Порядок загрузки (от листьев к корню):")
        print(" -> ".join(order))

def run_stage_5(args: argparse.Namespace, graph: dict) -> None:
    mermaid_code = generate_mermaid(graph)
    print("\nСгенерированный Mermaid код:")
    print(mermaid_code)
    save_to_png(mermaid_code, args.output)

def main() -> None:
    args = parse_args()

    if args.stage == STAGE_1:
        run_stage_1(args)
        return

    if args.test_mode:
        fetch_func = lambda pkg, ver: fetch_from_test_file(args.url, pkg)
    else:
        fetch_func = lambda pkg, ver: fetch_from_nuget(args.url, pkg, ver)

    if args.stage == STAGE_2:
        run_stage_2(args, fetch_func)
        return

    graph = build_graph(
        args.package, args.version, fetch_func, args.depth, args.filter
    )
    
    if args.stage in (STAGE_3, STAGE_4):
        run_stage_3_and_4(args, graph)
    elif args.stage == STAGE_5:
        run_stage_5(args, graph)

if __name__ == "__main__":
    main()