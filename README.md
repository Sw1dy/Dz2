# Задание 2
 Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.

Зависимости определяются для *git-репозитория*. Для описания графа
зависимостей используется представление *PlantUML*. Визуализатор должен
выводить результат на экран в виде кода.

Построить граф зависимостей для коммитов, в узлах которого находятся
списки файлов и папок. Граф необходимо строить только для коммитов позже
заданной даты.
Ключами командной строки задаются:

• Путь к программе для визуализации графов.

• Путь к анализируемому репозиторию.

• Путь к файлу-результату в виде кода.

• Дата коммитов в репозитории.

Все функции визуализатора зависимостей должны быть покрыты тестами.
## Команда для клонирования репозитория
```python
git clone https://github.com/Sw1dy/Dz2
```
## Использование
Для запуска инструмента используйте следующую команду:
```python
python graph.py <Путь к PlantUML.jar> <URL репозитория> <Путь к выходной директории> <Количество дней для порога коммитов (30 по умолчанию)>
```
## Пример команды
```python
python graph.py "C:\Users\Sw1dy\Dz2\PlantUML\plantuml-1.2024.8.jar" "https://github.com/Sw1dy/Dz2.git" "C:\Users\Sw1dy\Dz2\output" --days 30
```
## Тестирование
Для запуска тестов используйте следующую команду:
```python
python -m unittest Test_graph.py
```
![Скриншот тестов](https://github.com/Sw1dy/Dz2/blob/main/ResultsTests.png)


