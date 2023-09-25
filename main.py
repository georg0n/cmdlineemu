from zipfile import ZipFile
import sys


def delete_symbol(path):
    '''Обрезает абсолютный путь'''
    for letter in path:
        if letter == "/":
            path = path[1:]
        else:
            break
    return path


def ls(path, files):
    """Функция ls как в bash Linux"""
    path = delete_symbol(path)
    for file in files:
        if path in file.filename:
            file_names = file.filename[len(path):].split("/")  # разбиение имен которые идут после
            # пути, в котором мы находимся
            file_names = list(filter(None, file_names))  # удаление пустых строк из списка
            if len(file_names) > 1 or not file_names:  # пропускаем повторы
                continue
            print("\033[33m{}\033[0m".format(file_names[0]))


def cd(path, extension_path, files):
    """Функция cd как в bash Linux"""

    if "root:" in extension_path:
        '''Обработка случая если введен абсолютный путь до файла'''
        path = extension_path[len("root:"):]
    else:
        path += "/" + extension_path
    path = delete_symbol(path)

    global local_path

    if path == "":
        local_path = ""
        return True

    if "../" in path:
        local_path = local_path[:len(local_path) - len(local_path.split("/")[-1]) - 1]
        return True

    for file in files:
        if path in file.filename:
            local_path = "/" + path
            return True
    return False


def cat(path, ext_path, zip_file):
    """Функция cat как в bash Linux"""

    if "root:" in ext_path:
        '''Обработка случая если введен абсолютный путь до файла'''
        path = ext_path[len("root:"):]
    else:
        path += "/" + ext_path
    path = delete_symbol(path)

    flag = False
    for file in ZipFile(zip_file).filelist:
        if path in file.filename:
            flag = True
            with ZipFile(zip_file) as files:
                with files.open(path, 'r') as file:
                    for line in file.readlines():
                        print(line.decode('utf8').strip())
    if not flag:
        print("\033[31m{}\033[0m".format("Can`t open this file"))


if __name__ == '__main__':
    try:
        sys.argv[1]
    except IndexError:
        exit(0)
    zipfile = ZipFile(sys.argv[1])
    ROOT_PATH = "root:"
    local_path = ""
    command = input(ROOT_PATH + "/> ")
    all_files = zipfile.filelist
    while command != "exit":
        command = command.split(" ")

        if command[0] == "pwd":
            # ("/" if not local_path else local_path) проверка пуст ли local_path
            print("\033[32m{}\033[0m".format("  " + ROOT_PATH + ("/" if not local_path else local_path)))

        elif command[0] == "ls":
            ls(local_path, all_files)

        elif command[0] == "cd":
            try:
                command[1]
            except IndexError:
                print("\033[31m{}\033[0m".format("Don`t know this command"))
            if cd(local_path, command[1], all_files):
                pass
            else:
                print("\033[31m{}\033[0m".format("The path does not exist"))

        elif command[0] == "cat":
            cat(local_path, command[1], sys.argv[1])

        else:
            print("\033[31m{}\033[0m".format("Don`t know this command"))

        command = input(ROOT_PATH + ("/" if not local_path else local_path) + "> ")