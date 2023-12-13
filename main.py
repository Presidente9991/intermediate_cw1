"""
Приложение заметки (Python)

Реализовать консольное приложение заметки, с сохранением, чтением, добавлением, редактированием и удалением заметок.
Заметка должна содержать идентификатор, заголовок, Тело заметки и дату/время создания или последнего изменения заметки.
Сохранение заметок необходимо сделать в формате json или csv формат (разделение полей рекомендуется делать через
точку с запятой). Реализацию пользовательского интерфейса студент может делать как ему удобнее, можно делать как
параметры запуска программы (команда, данные), можно делать как запрос команды с консоли и последующим вводом данных,
как-то ещё, на усмотрение студента.
"""

import os
import json
import datetime


def del_notes(notes: list) -> dict:
    show_on_screen(notes)
    print('Какую заметку желаете удалить?')
    found = find_notes(notes)
    if found:
        show_on_screen(found)
        value = input('Подтвердите операцию удаления: Да/Нет\n>>>')
        if value.lower() == 'да':
            notes.remove(found[0])
            print('Удаление завершено.')
            return {}
        elif value.lower() == 'нет':
            print('Команда удаления отменена.')
            return {}
        else:
            print('Введена неверная команда.')
            return {}
    else:
        print('Ничего не нашли ;(')
        return {}


def save_change_notes(notes: list) -> dict:
    found = find_notes(notes)
    if found:
        show_on_screen(found)
        print("Что желаете изменить: название, содержание?")
        value = input('Введите параметр для изменения:\n>>>').lower()
        if value == 'название':
            found[0]['heading'] = input('Введите название заметки:\n>>> ').upper()
            found[0]['data'] = f"внесены изменения: {datetime.datetime.now().replace(microsecond=0)}"
        elif value == 'содержание':
            found[0]['body'] = input('Введите текст заметки:\n>>> ').upper()
            found[0]['data'] = f"внесены изменения: {datetime.datetime.now().replace(microsecond=0)}"
    else:
        print('Ничего не нашли ;(')
        return {}


def find_notes(notes: list) -> dict:
    heading = input('Введите название заметки:\n>>> ').upper()
    found = list(filter(lambda el: heading in el['heading'], notes))
    if found:
        show_on_screen(found)
        return found
    else:
        print('Ничего не найдено!')
        return {}


def file_path(file_name='list_of_notes'):
    return os.path.join(os.path.dirname(__file__), f'{file_name}.json')


def load_from_file():
    path = file_path()
    if os.stat(path).st_size:

        with open(path, 'r', encoding='UTF-8') as file:
            data = json.load(file)

        return data
    else:
        return []


def save_to_file(contact: list) -> None:
    path = file_path()

    with open(path, 'w', encoding='UTF-8') as file:
        json.dump(contact, file, ensure_ascii=False)


def show_on_screen(contacts: list) -> None:
    decode_keys = dict(
        heading='Название заметки:',
        body='Текст заметки:',
        data='Дата создания заметки',
    )
    pretty_text = str()
    for num, elem in enumerate(contacts, 1):
        pretty_text += f'Заметка №{num}:\n'
        pretty_text += '\n'.join(f'{decode_keys[k]} {v}' for k, v in elem.items())
        pretty_text += '\n________\n'
    print(pretty_text)


def new_notes(notes: list) -> None:
    notes.append(
        dict(
            heading=input('Введите название заметки:\n>>> ').upper(),
            body=input('Введите текст заметки:\n>>> ').upper(),
            data=str(datetime.datetime.now().replace(microsecond=0)),
        )
    )


def menu():
    commands = [
        'Показать все заметки',
        'Найти заметку',
        'Создать заметку',
        'Изменить заметку',
        'Удалить заметку'
    ]
    print('Укажите номер команды:')
    print('\n'.join(f'{n}. {v}' for n, v in enumerate(commands, 1)))
    choice = input('>>> ')

    try:
        choice = int(choice)
        if choice < 0 or len(commands) < choice:
            raise Exception('Команды с таким номером нет! Попробуйте ещё раз!')
        choice -= 1
    except ValueError as ex:
        print(ex, '\n''Некорректный номер команды, попробуйте ещё раз!')
        menu()
    except Exception as ex:
        print(ex)
        menu()
    else:
        return choice


def main() -> None:
    print('Программа запущена...')
    data = load_from_file()

    command = menu()
    if command == 0:
        show_on_screen(data)
    elif command == 1:
        find_notes(data)
    elif command == 2:
        new_notes(data)
    elif command == 3:
        save_change_notes(data)
    elif command == 4:
        del_notes(data)
    save_to_file(data)
    print('Конец программы!')


if __name__ == '__main__':
    main()
