## FBS PARSER

### Условие

Вам дана fb-схема для хранения некой структуры данных, а также есть класс, представляющий эту структуру в питоне. От вас требуется написать сериализацию / десериализацию в бинарный формат. (методы `loadb` и `dumpb`)

Что вам может пригодиться:
* [документация по flatbuffers](https://google.github.io/flatbuffers/flatbuffers_guide_use_python.html)
* бинарная утилита для кодогенерации - [flatc](https://stackoverflow.com/questions/55394537/how-to-install-flatc-and-flatbuffers-on-linux-ubuntu)

Некоторые подводные камни, на которых могут быть проблемы:
* Обращайте внимание на **порядок** записи / чтения данных. Например, в тестах предполагается, что имя вершины графа пишется в буфер перед списком ее ребер
* Учтите, что в схеме содержатся, например, `Struct` и `Table`. Работа с ними несколько отличается
* Помните, что запись во flatbuf-ы производится по принципу "сначала конструируем все поля, а только  потом сам объект" (перечитайте это, если получите `NestedError` или что-то подобное)

### Отправка на сервер

Для сдачи задания на сервере достаточно в коммит добавить изменения в файле `schema_parser.py`. Добавлять в коммит папку с результатами кодогенерации `fbs_scheme` не нужно.