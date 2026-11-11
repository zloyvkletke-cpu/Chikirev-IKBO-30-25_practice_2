import argparse
from cli import parse_args, print_config
from fetcher import fetch_from_nuget, fetch_from_test_file
from graph import build_graph, get_load_order
from visualizer import generate_mermaid, save_to_png

def run_stage_1(args: argparse.Namespace) -> None:
    """Запускает Этап 1 (Вывод конфигурации)."""
    print_config(args)

def run_stage_2(args: argparse.Namespace, fetch_func) -> None:
    """Запускает Этап 2 (Вывод прямых зависимостей)."""
    deps = fetch_func(args.package, args.version)
    print(f"Прямые зависимости {args.package}:")
    for dep_name, dep_ver in deps:
        print(f"- {dep_name} (версия: {dep_ver})")

def run_stage_3_and_4(args: argparse.Namespace, graph: dict) -> None:
    """Запускает Этапы 3 и 4 (Вывод графа и порядка загрузки)."""
    if args.stage == 3:
        print("Построенный граф (Список смежности):")
        for node, deps in graph.items():
            print(f"{node} -> {deps}")
    elif args.stage == 4:
        order = get_load_order(graph)
        if len(order) != len(graph):
            print("Внимание: в графе обнаружены циклические зависимости!")
        print("Порядок загрузки зависимостей (от листьев к корню):")
        print(" -> ".join(order))

def run_stage_5(args: argparse.Namespace, graph: dict) -> None:
    """Запускает Этап 5 (Генерация Mermaid и PNG)."""
    mermaid_code = generate_mermaid(graph)
    print("\nСгенерированный Mermaid код:")
    print(mermaid_code)
    save_to_png(mermaid_code, args.output)

def main() -> None:
    """Главная точка входа в приложение."""
    args = parse_args()

    if args.stage == 1:
        run_stage_1(args)
        return

    if args.test_mode:
        fetch_func = lambda pkg, ver: fetch_from_test_file(args.url, pkg)
    else:
        fetch_func = lambda pkg, ver: fetch_from_nuget(args.url, pkg, ver)

    if args.stage == 2:
        run_stage_2(args, fetch_func)
        return

    graph = build_graph(
        args.package, args.version, fetch_func, args.depth, args.filter
    )
    
    if args.stage in (3, 4):
        run_stage_3_and_4(args, graph)
    elif args.stage == 5:
        run_stage_5(args, graph)

if __name__ == "__main__":
    main()