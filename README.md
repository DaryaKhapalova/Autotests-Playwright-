# Autotests-Playwright 
!Важно: автотесты предназначены для выполнения в локальной сети компании.
Запуск проекта "из коробки" во внешней среде невозможен
Архитектура и тесты предназначены для понимания структуры, как шаблон для адаптации под свои нужды
## Структура проекта
Репозиторий содержит автотесты, написанные с использованием [Playwright](https://playwright.dev/python/) на языке Python. Проект предназначен для автоматизации тестирования веб-приложений.
Также для написания кода необходима установка IDE-системы. Например, [Visual Studio Code](https://code.visualstudio.com/Download)
 tests/ # Тестовые сценарии
 pages/ # Page Object модели
 config/ # Конфигурационные файлы
 conftest.py # Фикстуры Pytest
 requirements.txt # Зависимости
 pytest.ini # Настройки Pytest
 README.md # Документация проекта
## Начало работы 
### Установка 
1. Установите python
2. Установите IDE-систему
3. Клонируйте репозиторий:
   ```bash
git clone https://github.com/DaryaKhapalova/Autotests-Playwright-.git
cd Autotests-Playwright(название-репозитория)

4. Установите зависимости:
pip install -r requirements.txt
5. Установите Playwright:
pip install playwright
6. Установите браузеры для Playwright:
playwright install
#### Запуск тестов
Все тесты:
```bash
pytest
Конкретный тест:
```bash
pytest tests/test_example.py
