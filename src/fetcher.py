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
    with urllib.request.urlopen(req, timeout=NETWORK_TIMEOUT) as response:
        data = response.read()
        if response.info().get('Content-Encoding') == 'gzip':
            data = gzip.decompress(data)
        return json.loads(data)

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
            
        dependencies = []
        dep_groups = catalog_entry.get("dependencyGroups", [])
        
        if isinstance(dep_groups, list):
            for group in dep_groups:
                if isinstance(group, dict):
                    for dep in group.get("dependencies", []):
                        if isinstance(dep, dict):
                            dep_id = dep.get("id")
                            dep_range = dep.get("range", "")
                            
                            if not dep_id or dep_id in [d[0] for d in dependencies]:
                                continue
                            
                            match = re.search(r'[\[\(]([^,]+)', dep_range)
                            dep_ver = match.group(1).strip() if match else "1.0.0"
                            
                            dependencies.append((dep_id, dep_ver))
        return dependencies
    except Exception as e:
        print(f"Ошибка получения данных для {package} ({version}): {e}")
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