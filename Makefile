.PHONY: install test run help demo-real demo-test clean

help:
	@echo "Доступные команды:"
	@echo "  make install    - Установить зависимости"
	@echo "  make test       - Запустить тесты"
	@echo "  make demo-real  - Демо: реальный запрос к NuGet API (Newtonsoft.Json)"
	@echo "  make demo-test  - Демо: тестовый режим (BFS, фильтрация, цикл)"
	@echo "  make clean      - Удалить сгенерированные файлы (PNG, MMD)"
	@echo ""
	@echo "Ручной запуск: python src/main.py -p <пакет> -v <версия> --stage <1-5>"

run: help

install:
	pip install -r requirements.txt

test:
	python -m unittest discover -s tests -v

demo-real-neb:
	python src/main.py --package Newtonsoft.Json --version 13.0.1 --stage 2
	python src/main.py --package Newtonsoft.Json --version 13.0.1 --depth 1 --stage 5 -o newtonsoft_depth1.png

demo-real:
	python src/main.py --package Newtonsoft.Json --version 13.0.1 --stage 2
	python src/main.py --package Newtonsoft.Json --version 13.0.1 --depth 2 --stage 5 -o newtonsoft_depth2.png

demo-test:
	python src/main.py -p A -u tests/test_data.json -t -d 2 -f "G" --stage 4
	python src/main.py -p A -u tests/test_data.json -t -d 2 -f "G" --stage 5 -o test_graph.png

clean:
	python -c "import os, glob; [os.remove(f) for f in glob.glob('*.png') + glob.glob('*.mmd')]"