import os


def list_files(startpath):
    # Папки, которые нужно пропустить
    exclude_dirs = {'migrations', '__pycache__', 'variants', 'additional', 'main', 'media'}
    # Файлы, которые нужно пропустить
    exclude_files = {'__init__.py'}

    for root, dirs, files in os.walk(startpath):
        # Удаляем исключенные папки из списка для обхода
        dirs[:] = [d for d in dirs if d not in exclude_dirs]

        # Пропускаем корневой каталог, если он в исключениях
        if os.path.basename(root) in exclude_dirs:
            continue

        # Вычисляем уровень вложенности
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        # Выводим текущую директорию
        print('{}{}/'.format(indent, os.path.basename(root)))

        subindent = ' ' * 4 * (level + 1)
        # Выводим файлы, пропуская исключенные
        for f in files:
            if f in exclude_files:
                continue
            print('{}{}'.format(subindent, f))


if __name__ == '__main__':
    list_files(os.getcwd())