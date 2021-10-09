# Домашнее задание к лекции «Docker»

## Задание 2

Создайте контейнер для REST API сервера любого вашего проекта из курса по Django (например, [CRUD: Склады и запасы](https://github.com/netology-code/dj-homeworks/tree/drf/3.2-crud/stocks_products)).

- Приложите в репозиторий Dockerfile и файлы приложения.
- В README.md описать типовые команды для запуска контейнера c backend-сервером.

Команда для создания docker'а:
- Необходимо созранитиь проект в локальной папке под названием products
- Создание image: sudo docker build --tag crud .
- Для запуска контейнера: sudo docker run -d --name crud -p 8000:8000 crud
