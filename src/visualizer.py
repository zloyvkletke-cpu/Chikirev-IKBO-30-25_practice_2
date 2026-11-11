import subprocess

def generate_mermaid(graph: dict) -> str:
    """Формирует текстовое представление на языке Mermaid."""
    lines = ["graph TD"]
    for node, deps in graph.items():
        if not deps:
            lines.append(f"    {node}")
        for dep in deps:
            lines.append(f"    {node} --> {dep}")
    return "\n".join(lines)

def save_to_png(mermaid_text: str, output_filename: str) -> None:
    """Сохраняет граф в PNG (вызов через npx с конфигом)."""
    mmd_file = output_filename.replace(".png", ".mmd")
    config_file = "mermaid_config.json"
    
    with open(mmd_file, "w", encoding="utf-8") as f:
        f.write(mermaid_text)
    
    try:
        cmd = [
            "npx", "-y", "@mermaid-js/mermaid-cli", 
            "-i", mmd_file, 
            "-o", output_filename, 
            "-c", config_file
        ]
        subprocess.run(
            cmd, 
            check=True, 
            capture_output=True,
            text=True,
            shell=True
        )
        print(f"Изображение успешно сохранено: {output_filename}")
    except subprocess.CalledProcessError as e:
        print("Ошибка при генерации PNG.")
        print(f"Детали: {e.stderr}")
        print(f"Синтаксис Mermaid сохранен в файл: {mmd_file}")