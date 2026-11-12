import argparse

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="NuGet Dependency Graph Visualizer"
    )
    parser.add_argument(
        "-p", "--package", required=True, 
        help="Имя анализируемого пакета"
    )
    parser.add_argument(
        "-u", "--url", 
        help="URL-адрес репозитория или путь к тестовому файлу"
    )
    parser.add_argument(
        "-t", "--test-mode", action="store_true", 
        help="Режим работы с тестовым репозиторием"
    )
    parser.add_argument(
        "-v", "--version", 
        help="Версия пакета (например, 1.0.0)"
    )
    parser.add_argument(
        "-o", "--output", default="graph.png", 
        help="Имя сгенерированного файла с изображением"
    )
    parser.add_argument(
        "-d", "--depth", type=int, default=5, 
        help="Максимальная глубина анализа"
    )
    parser.add_argument(
        "-f", "--filter", default="", 
        help="Подстрока для фильтрации пакетов"
    )
    parser.add_argument(
        "--stage", type=int, choices=[1, 2, 3, 4, 5], default=5, 
        help="Этап выполнения"
    )
    return parser

def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки и проводит валидацию."""
    parser = _build_parser()
    args = parser.parse_args()
    
    if args.depth < 1:
        parser.error("Глубина должна быть больше 0")
    if not args.test_mode and not args.version:
        parser.error("В обычном режиме укажите версию (--version)")
    if not args.test_mode and not args.url:
        args.url = "https://api.nuget.org/v3/registration5-gz-semver2"

    return args

def print_config(args: argparse.Namespace) -> None:
    """Выводит параметры в формате ключ-значение."""
    print("--- Конфигурация ---")
    for key, value in vars(args).items():
        print(f"{key}: {value}")
    print("--------------------")