# 🧪 Test API Project

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![Pytest](https://img.shields.io/badge/Pytest-7.4.0-green?logo=pytest)
![Allure](https://img.shields.io/badge/Allure-2.24.0-red?logo=allure)
![Requests](https://img.shields.io/badge/Requests-2.31.0-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 О проекте

**Test API Project** — это демонстрационный фреймворк для автоматизированного тестирования REST API. Проект создан с целью показать мой подход к организации тестовой инфраструктуры, написанию чистого и поддерживаемого кода, а также использованию современных практик тестирования.

### ✨ Ключевые возможности

- ✅ Полноценный API клиент с поддержкой сессий
- ✅ Модульная структура для легкого расширения
- ✅ Набор готовых тестов для различных сценариев
- ✅ Генерация тестовых данных с помощью Faker
- ✅ Поддержка переменных окружения через .env
- ✅ Интеграция с Allure Reports для наглядных отчетов

## 🛠 Технологический стек

| Компонент | Назначение |
|-----------|------------|
| **Python 3.9+** | Основной язык программирования |
| **Pytest** | Фреймворк для тестирования |
| **Requests** | HTTP клиент для работы с API |
| **Allure** | Система отчетности |
| **python-dotenv** | Управление конфигурацией |
| **Faker** | Генерация тестовых данных |

## 📁 Структура проекта
```
test_api_project/
├── 📂 src/ # Исходный код фреймворка
│ ├── 📂 api/ # Работа с API
│ │ ├── client.py # Базовый API клиент
│ │ └── endpoints.py # Константы эндпоинтов
│ ├── 📂 core/ # Ядро фреймворка
│ │ ├── config.py # Конфигурация
│ │ └── assertions.py # Кастомные проверки
│ └── 📂 utils/ # Вспомогательные модули
│ ├── data_generator.py # Генерация данных
│ └── helpers.py # Утилиты
├── 📂 tests/ # Автоматические тесты
│ ├── conftest.py # Pytest фикстуры
│ ├── test_authentication.py # Тесты авторизации
│ └── 📂 test_accounts/ # Тесты аккаунтов
├── 📄 .env.example # Пример конфигурации
├── 📄 .gitignore # Игнорируемые файлы
├── 📄 requirements.txt # Зависимости
├── 📄 README.md # Документация
└── 📄 pytest.ini # Настройки pytest
```
## 🚀 Быстрый старт

```bash
# Клонирование репозитория
git clone https://github.com/Hold-My-Tea/test_api_project
cd test_api_project

# Создание виртуального окружения
python -m venv venv
source venv/bin/activate      # для Linux/Mac
# venv\Scripts\activate       # для Windows

# Установка зависимостей
pip install -r requirements.txt

# Настройка окружения
cp .env.example .env           # создайте свой .env файл
```
⚙️ Важно о конфигурации
Файл .env не хранится в репозитории — это best practice для безопасности. Токены, пароли и URL тестовых стендов добавляются локально.

### 🧪 Запуск тестов
```
# Базовый запуск
pytest

# С подробным выводом
pytest -v

# Конкретный файл
pytest tests/test_authentication.py

# По маркерам
pytest -m smoke
pytest -m regression

# С генерацией Allure отчета
pytest --alluredir=allure-results
allure serve allure-results
```
## 📬 Контакты
- Автор: Oksana Maier 
- GitHub: [@Hold-My-Tea](https://github.com/Hold-My-Tea) 
- Проект: [Hold-My-Tea/test_api_project](https://github.com/Hold-My-Tea/test_api_project)
