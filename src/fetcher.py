import json
import urllib.request
import gzip
import re
from typing import List, Dict, Any, Tuple

NETWORK_TIMEOUT = 10

def fetch_json(url: str) -> Dict[str, Any]:
    """Скачивает JSON с поддержкой gzip."""
    req = urllib.request.Request(
        url, headers={'Accept-Encoding': 'gzip'}
    )
    with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT) as resp:
        data = resp.read()
        if resp.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(data)
        return json.loads(data)

def _extract_version(dep_range: str) -> str:
    """Извлекает минимальную версию из диапазона NuGet."""
    match = re.search(r'[\[\(]([^,]+)', dep_range)
    return match.group(1).strip() if match else "1.0.0"

def _parse_dependency_groups(dep_groups: list) -> List[Tuple[str, str]]:
    """Вспомогательная функция для парсинга групп зависимостей."""
    dependencies = []
    for group in dep_groups:
        if not isinstance(group, dict):
            continue
        for dep in group.get("dependencies", []):
            if isinstance(dep, dict):
                dep_id = dep.get("id")
                if not dep_id or dep_id in [d[0] for d in dependencies]:
                    continue
                dep_ver = _extract_version(dep.get("range", ""))
                dependencies.append((dep_id, dep_ver))
    return dependencies

def fetch_from_nuget(
    base_url: str, package: str, version: str
) -> List[Tuple[str, str]]:
    """Возвращает список кортежей (имя_зависимости, её_версия)."""
    url = f"{base_url}/{package.lower()}/{version}.json"
    try:
        payload = fetch_json(url)
        catalog_entry = payload.get("catalogEntry", {})
        
        if isinstance(catalog_entry, str):
            catalog_entry = fetch_json(catalog_entry)
            
        dep_groups = catalog_entry.get("dependencyGroups", [])
        if not isinstance(dep_groups, list):
            return []
            
        return _parse_dependency_groups(dep_groups)
    except Exception as e:
        print(f"Ошибка получения данных {package} ({version}): {e}")
        return []

def fetch_from_test_file(
    filepath: str, package: str
) -> List[Tuple[str, str]]:
    """Возвращает список кортежей (имя_зависимости, "1.0.0")."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            deps = data.get(package, [])
            return [(d, "1.0.0") for d in deps]
    except Exception as e:
        print(f"Ошибка чтения тестового файла: {e}")
        return []